# _*_ coding: utf-8 _*_
"""run with python3"""
import json
import common_utils as cu

# python参数校验模式
IS_PYTHON_SCHEMA = False
# 添加cookie字段到header中
COOKIE_IN_HEADER_MODEL = {
    "default": "",
    "description": "",
    "in": "header",
    "name": "Cookie",
    "required": False,
    "type": "string"
}


def prompt():
    """提示信息"""
    print('示例: python3 apidoc2swagger.py -s ./api_data.json -d '
          './swagger.json')
    print('-s apidoc生成的api_data.json文件，必填')
    print('-d 转换后的swagger.json文件，可选')
    print('-p 转换为python schema可以用的简约字段,不加该参数表示转yapi格式参数')
    print('-h 帮助')
    print('\n********************************************')


def api_data_to_swagger(api_data):
    """解析apidoc的json数据

    :param api_data: 请求数据
    :return: swagger格式json
    """
    # 所有的分组
    tags = []
    # 所有的请求路径
    paths = {}
    # 遍历每个请求
    for item in api_data:
        # 请求方法
        request_type = item["type"]
        # 请求路径
        url = item["url"]
        # 如果不存在该url则新建
        paths[url] = {} if url not in paths else paths[url]
        # 创建请求类型
        if request_type in paths[url]:
            raise Exception(item["filename"] + ":" + url + ":有两个相同的请求")
        else:
            paths[url][request_type] = {}
        # 该api分组
        if {"name": item["group"], "description": item["groupTitle"]} \
                not in tags:
            tags.append({
                "name": item["group"],
                "description": item["groupTitle"]
            })
        # 接口名称
        summary = item["title"]
        api_description = item[
            "description"] if 'description' in item else None
        # 获取apidoc的头部数据
        api_data_header = item['header']['fields']['Header'] if \
            (('header' in item) and (item['header'] != {}) and (
                    'Header' in item['header']['fields'])) else []
        # Header参数解析
        yapi_request_header = api_data_to_swagger_header_path_query(
            api_data_header, "Header")
        # 添加cookie字段到header中，方便自动化测试
        yapi_request_header.append(COOKIE_IN_HEADER_MODEL)
        # 获取apidoc的Body请求参数
        api_data_parameter = item['parameter'] if 'parameter' in item else {}
        # 获取apidoc的Query请求参数
        api_data_query_parameter = api_data_parameter['fields']['Query'] if \
            ((api_data_parameter != {} and 'fields' in api_data_parameter) and
             ('Query' in api_data_parameter['fields'])) else []
        # 获取apidoc的Path请求参数
        api_data_path_parameter = api_data_parameter['fields']['Path'] if \
            ((api_data_parameter != {} and 'fields' in api_data_parameter)
             and ('Path' in api_data_parameter['fields'])) else []
        # Query参数解析
        yapi_request_query_parameter = api_data_to_swagger_header_path_query(
            api_data_query_parameter, 'Query')
        # Path参数解析
        yapi_request_path_parameter = api_data_to_swagger_header_path_query(
            api_data_path_parameter, 'Path')
        # Body参数解析
        yapi_request_body_parameters = api_data_to_swagger_request_response(
            api_data_parameter, "Parameter", "url: " + url + " name: " +
                                             summary + " 请求参数错误")
        # 汇总header query path body数据
        parameters = [yapi_request_body_parameters] if \
            yapi_request_body_parameters != {} else []
        for header in yapi_request_header:
            if header != {}:
                parameters.append(header)
        for query in yapi_request_query_parameter:
            if query != {}:
                parameters.append(query)
        for path in yapi_request_path_parameter:
            if path != {}:
                parameters.append(path)
        # 获取apidoc的返回参数
        api_data_success = item["success"] if 'success' \
                                              in item else {}
        # 解析返回参数
        responses = api_data_to_swagger_request_response(
            api_data_success, "Success 200",
            "url: " + url + " name: " + summary + " 返回参数错误")
        # 请求示例
        api_data_request_example = api_data_parameter[
            'examples'] if 'examples' in api_data_parameter else {}
        # 返回示例
        api_data_response_example = api_data_success[
            'examples'] if 'examples' in api_data_success else {}
        # 请求示例字符串
        yapi_request_example = api_data_to_swagger_example(
            "* 请求示例", api_data_request_example)
        # 相应示例字符串
        yapi_response_example = api_data_to_swagger_example(
            "* 返回示例", api_data_response_example)
        if api_description is None:
            description = yapi_request_example + "\n\n" + yapi_response_example
        else:
            # 组合成一个字符串添加yapi备注中
            description = "* 说明\n" + api_description + "\n\n" + \
                          yapi_request_example + "\n\n" + yapi_response_example
        # 生成一个请求
        paths[url][request_type] = {
            "tags": [item["group"]],
            "summary": summary,
            "description": description,
            "consumes": [
                "application/json"
            ],
            "parameters": parameters,
            "responses": responses
        }

    swagger_json = {
        "swagger": "2.0",
        "schemes": [
            "http"
        ],
        "tags": tags,
        "paths": paths
    }
    return swagger_json


def api_data_to_swagger_request_response(request_param, api_data_type, msg):
    """解析body请求参数和返回参数

    :param request_param: 参数
    :param api_data_type: 参数类型
    :param msg: 错误说明
    :return: swagger格式的json数据
    """
    properties = {}
    required = []
    # 判断是否有数据
    if request_param == {} or 'fields' not in request_param:
        return {}
    # 判断该字段下是否有数据
    if api_data_type not in request_param['fields']:
        return {}
    for field in request_param['fields'][api_data_type]:
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
        if not IS_PYTHON_SCHEMA:
            object_item = cu.yapi_swagger_param_template(param_type,
                                                         description, field)
        else:
            object_item = cu.python_json_schema(param_type, field)
        parent_location[key] = object_item
    if api_data_type == "Parameter":
        # 请求参数格式
        yapi_body = {
            "name": "root",
            "in": "body",
            "schema": {
                "$schema": "http://json-schema.org/draft-04/schema#",
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
    else:
        # 返回参数格式
        yapi_body = {
            "200": {
                "description": "successful operation",
                "schema": {
                    "$schema": "http://json-schema.org/draft-04/schema#",
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }

    return yapi_body


def api_data_to_swagger_header_path_query(requests, param_type):
    """解析header path参数 query参数

    :param requests: 请求参数
    :param param_type: 参数类型
    :return: swagger json格式数据
    """
    parameters = []
    for request in requests:
        parameter = {
            "name": request["field"],
            "in": param_type.lower(),
            "required": bool(1 - request["optional"]),
            "type": 'string' if param_type == 'Header' else request["type"],
            "description": cu.noqa_conversion(request["description"])
        }
        if param_type == "Header":
            parameter["default"] = request["defaultValue"]
            parameter["description"] = ""
        parameters.append(parameter)
    return parameters


def api_data_to_swagger_example(param_type, api_data_example):
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


if __name__ == '__main__':
    argvs = cu.check_argv(prompt)
    try:
        if 'h' in argvs:
            prompt()
        else:
            # 接收输入输出文件路径
            s_file = argvs['s'] if 's' in argvs else None
            d_file = argvs['d'] if 'd' in argvs else './swagger.json'
            IS_PYTHON_SCHEMA = True if 'p' in argvs else False
            # 读取apidoc
            data = open(s_file, 'r', encoding='utf-8')
            # 格式转换
            moudel0 = api_data_to_swagger(json.load(data))
            api_yapi_data = json.dumps(moudel0, ensure_ascii=False, indent=4,
                                       sort_keys=True)
            # 输出新文件
            f = open(d_file, 'w', encoding='utf-8')
            f.write(api_yapi_data)
    except Exception as e:
        print('参数有误')
        prompt()
        raise e
