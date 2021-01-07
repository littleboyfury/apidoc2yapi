# _*_ coding: utf-8 _*_
# 暂不维护该转换方式
import json
import common_utils as cu
import time


def prompt():
    """提示信息"""
    print('示例: python3 apidoc2yapi.py -s ./api_data.json -d '
          './yapi_api_data.json')
    print('-s apidoc生成的api_data.json文件，必填')
    print('-d 转换后的yapi_api_data.json文件，可选')
    print('-h 帮助')
    print('\n********************************************')


def api_data_path_query_parameter_to_yapi(api_data_parameter, param_type=None):
    """解析path和query参数

    :param api_data_parameter: apidoc参数
    :param param_type: 参数类型
    :return: yapi参数形势
    """
    request_data = []
    for item in api_data_parameter:
        tmp = {
            "name": item['field'],
            "example": item['defaultValue'] if 'defaultValue' in item else '',
            "desc": cu.noqa_conversion(item['description'])
        }
        # 如果参数为query类型，涉及到可选和必须
        if param_type == 'Query':
            tmp["required"] = "0" if item['optional'] else "1"
        request_data.append(tmp)
    return request_data


def api_data_request_response_to_yapi(api_data, api_data_type, msg):
    """解析请求参数和相应参数

    :param msg: 错误提示信息
    :param api_data: 参数数据
    :param api_data_type: Parameter或者Success 200
    :return: yapi格式数据
    """
    properties = {}
    required = []

    if api_data == {} or 'fields' not in api_data:
        return {}
    if api_data_type not in api_data['fields']:
        return {}

    for field in api_data['fields'][api_data_type]:
        param_type = field['type'].lower()
        description = cu.noqa_conversion(field['description'])
        key = field['field']
        parent_location = properties
        """处理逻辑
        1.field是否有"."
        │
        ├───是:2.找父节点
        │   │
        │   └───3.去到4
        │
        └───否:4.type是否含有"[]"
            │
            ├───是:5.type是否为object
            │   │
            │   ├───是:6.数组对象模板
            │   │
            │   └───否:7.数组非对象模板
            │
            └───否:8.type是否为object
                │
                ├───是:9.对象模板
                │
                └───否:10.非对象模板
        """
        if '.' in key:
            # 有父节点情况
            field_items = key.split(".")
            parent_location_required = None
            # 查找父节点
            for field_item in field_items:
                try:
                    if field_item not in parent_location:
                        break
                    # 数据类型
                    if parent_location[field_item]["type"] == "array":
                        parent_location_required = parent_location[field_item][
                            'items']
                        parent_location = parent_location[field_item]['items'][
                            'properties']
                    # 对象类型
                    else:
                        parent_location_required = parent_location[field_item]
                        parent_location = parent_location[field_item][
                            'properties']
                except KeyError:
                    # 大致可以检查格式是否正确
                    raise Exception(msg)
            # 去掉前缀，如果根节点为data，子节点写的data.a.b这种形式，没有a
            # 这种识别不了错误，会直接忽略a
            key = field_items[-1]
            # 该节点是否可选 True为可选，False为必须，required中添加必须参数
            if field['optional'] is False:
                try:
                    if 'required' in parent_location_required:
                        parent_location_required['required'].append(key)
                    else:
                        parent_location_required['required'] = [key]
                except TypeError:
                    # 大致可以检查格式是否正确
                    raise Exception(msg)
        else:
            # 根节点是否可选
            if field['optional'] is False:
                required.append(key)
        object_item = cu.yapi_swagger_param_template(param_type, description,
                                                     field)
        parent_location[key] = object_item

    yapi_request_body = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": properties,
        "required": required
    }
    return yapi_request_body


def api_data_example_to_yapi(param_type, api_data_example):
    """将example转为字符串形式，并且保持格式不变

    :param param_type: 请求示例 or 响应示例
    :param api_data_example: 示例数据
    :return:
    """
    if api_data_example == {}:
        return ""
    if len(api_data_example) > 0:
        # content 是一个json字符串
        yapi_example = "<p>" + param_type + "：<br>" + api_data_example[0][
            'content'].replace(
            '\n', '<br>\n').replace(' ', '&nbsp;') + "</p>\n"
        return yapi_example
    else:
        return ""


def api_data_to_yapi(api_data):
    """将apidoc json文件转为yapi json文件"""
    # 初始化一个yapi_api分组
    yapi_api_group = []
    moudel0 = []
    for data1 in api_data:
        # 提取接口下的字段,每个接口下有11个字段
        """
          {
            "type": "get",
            "url": "/zhzl/person/aidsDeatil",
            "title": "描述明细",
            "description": "<p>描述明细</p>",
            "name": "aidsDeatil",
            "group": "aids",
            "parameter": {},
            "success": {},
            "version": "0.0.0",
            "filename": "myapi/person.js",
            "groupTitle": "aids"
          },
        """
        api_data_type = data1['type']
        # 兼容非标准格式method的写法，如post/get
        method = api_data_type.upper()
        api_data_url = data1['url'] if data1['url'][0] == '/' else "/" + data1[
            'url']
        api_data_title = data1['title']
        api_data_group = data1['group']
        api_data_groupTitle = data1['groupTitle']
        # 请求参数
        api_data_parameter = data1['parameter'] if 'parameter' in data1 else {}
        # Query请求参数
        api_data_query_parameter = api_data_parameter['fields']['Query'] if \
            ((api_data_parameter != {}) and (
                    'Query' in api_data_parameter['fields'])) else []
        # Path请求参数
        api_data_path_parameter = api_data_parameter['fields']['Path'] if \
            ((api_data_parameter != {}) and (
                    'Path' in api_data_parameter['fields'])) else []
        # 响应参数
        api_data_success = data1['success'] if 'success' in data1 else {}
        # 请求示例
        api_data_request_example = api_data_parameter[
            'examples'] if 'examples' in api_data_parameter else {}
        # 返回示例
        api_data_response_example = api_data_success[
            'examples'] if 'examples' in api_data_success else {}
        # Body请求参数解析
        yapi_request_body = api_data_request_response_to_yapi(
            api_data_parameter, 'Parameter', api_data_title + "：请求参数格式不正确")
        # Query参数解析
        yapi_request_query_parameter = api_data_path_query_parameter_to_yapi(
            api_data_query_parameter, 'Query')
        # Path参数解析
        yapi_request_path_parameter = api_data_path_query_parameter_to_yapi(
            api_data_path_parameter)
        # 相应参数解析
        yapi_response_body = api_data_request_response_to_yapi(
            api_data_success, 'Success 200', api_data_title + "：返回参数格式不正确")
        # 请求示例字符串
        yapi_request_example = api_data_example_to_yapi(
            "请求示例", api_data_request_example)
        # 相应示例字符串
        yapi_response_example = api_data_example_to_yapi(
            "返回示例", api_data_response_example)
        # 组合成一个字符串添加yapi备注中
        yapi_example = yapi_request_example + "\n\n" + yapi_response_example

        # 分组模板moudle1
        moudle1 = {
            "index": 0,
            "name": api_data_groupTitle,
            "desc": api_data_groupTitle,
            "add_time": int(time.time()),
            "up_time": int(time.time()),
            "list": []
        }
        # 接口模板moudel2
        # moudel2：同一个分组下的接口，放到moudle1的list中
        moudel2 = {
            "query_path": {
                "path": api_data_url,
                "params": []
            },
            "edit_uid": 0,
            "status": "undone",
            "type": "static",
            "req_body_is_json_schema": True,
            "res_body_is_json_schema": True,
            "api_opened": False,
            "index": 0,
            "__v": 0,
            "tag": [],
            "_id": 11,
            "project_id": 11,
            "catid": 11,
            "uid": 11,
            "add_time": int(time.time()),
            "up_time": int(time.time()),
            "title": api_data_title,
            "path": api_data_url,
            "method": method,
            "req_query": yapi_request_query_parameter,
            "req_params": yapi_request_path_parameter,
            "req_headers": [],
            "req_body_other": json.dumps(yapi_request_body, ensure_ascii=False,
                                         sort_keys=True),
            "req_body_type": "json",
            "req_body_form": [],
            "res_body": "" if yapi_response_body == {} else json.dumps(
                yapi_response_body, ensure_ascii=False, sort_keys=True),
            "res_body_type": "json",
            "desc": yapi_example,
            "markdown": yapi_example
        }
        # 根据api_data构造yapi_data
        # moudel2(yapi接口)===>moudle1(yapi分组)===>moudle0(装yapi分组的list)
        if api_data_group not in yapi_api_group:
            # 创建分组，将接口加入分组
            yapi_api_group.append(api_data_group)
            moudle1["list"].append(moudel2)
            moudel0.append(moudle1)
        else:
            # 找到已存在的分组
            for moudel in moudel0:
                if moudel["name"] == api_data_group:
                    moudel["list"].append(moudel2)
                else:
                    pass
    return moudel0


if __name__ == '__main__':
    argvs = cu.check_argv(prompt)
    try:
        if 'h' in argvs:
            prompt()
        else:
            # 接收输入输出文件路径
            s_file = argvs['s'] if 's' in argvs else None
            d_file = argvs['d'] if 'd' in argvs else './yapi_api_data.json'
            # 读取apidoc
            data = open(s_file, 'r', encoding='utf-8')
            # 格式转换
            moudel0 = api_data_to_yapi(json.load(data))
            api_yapi_data = json.dumps(moudel0, ensure_ascii=False, indent=4,
                                       sort_keys=True)
            # 输出新文件
            f = open(d_file, 'w', encoding='utf-8')
            f.write(api_yapi_data)
    except Exception as e:
        prompt()
        raise e
