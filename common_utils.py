# _*_ coding: utf-8 _*_
import sys
import re


def check_argv(func):
    """检查参数"""

    if len(sys.argv) > 1:
        argv_map = {}
        # 遍历外部传参
        for argv in sys.argv:
            index = sys.argv.index(argv)
            # 如果是以-开头的参数
            if argv[0] == '-':
                if index + 1 == len(sys.argv):
                    argv_map[argv[1::]] = None
                else:
                    # 取后一位参数
                    try:
                        argv_value = sys.argv[index + 1]
                        if argv_value[0] != '-':
                            argv_map[argv[1::]] = argv_value
                        elif argv_value[0] == '-':
                            argv_map[argv[1::]] = None
                    except Exception:
                        return func()

            # 如果连续两个非-开头的参数
            elif argv[0] != '-' and index != 0:
                last_argv = sys.argv[index - 1]
                if last_argv[0] != '-':
                    return func()
        # {参数1：值1，参数2：值2...}
        return argv_map


def noqa_conversion(desc):
    """去掉多余的标签

    :param desc: 备注内容
    :return: 返回的备注
    """
    # 如果字段过长，可以通过"  # noqa"方式进行标识，可以通过pep8字段超79检测
    description = desc.replace("  # noqa", "") if "  # noqa" in desc else desc
    # 如果单独标识  # noqa，apidoc会解析为<h1>noqa</h1>
    description = description.replace("<h1>noqa</h1>", "") if \
        "<h1>noqa</h1>" in description else description
    description = re.sub(r'<p>|</p>', '', description)
    description = re.sub(r'<pre>|</pre>', '', description)
    description = re.sub(r'<code>|</code>', '', description)
    description = description.strip()
    return description


def yapi_swagger_param_template(param_type, description, field):
    """解析apidoc为yapi或在swagger格式的参数模板

    :param param_type: 请求类型
    :param description: 描述
    :param field: 参数
    :return:
    """
    if '[]' in param_type:
        # 数组类型模板
        object_item = {
            "type": "array",
            "items": {
                "type": param_type[:-2],
                "description": "",
            },
            "description": description
        }
        if 'object' == param_type[:-2]:
            # 对象数组模板
            object_item["items"]["properties"] = {}
    else:
        # 非数组模板
        object_item = {
            "type": param_type,
            "description": description,
        }
        if 'object' == param_type:
            # 对象类型模板
            object_item["properties"] = {}
        # 是否包含默认值
        if 'defaultValue' in field.keys():
            object_item["default"] = field['defaultValue']
        # 允许的值
        if 'allowedValues' in field.keys():
            object_item['enum'] = field['allowedValues']
        if 'size' in field.keys():
            # 数字范围
            if field['type'].lower() in ['number', 'integer']:

                # filed['size'] -> re.findall() -> result
                # -3--1 -> -3,-1 -> -3,-1
                # -1-1 -> -1,-1 -> -1,1
                # 1-3 -> 1,-3 -> 1,3
                # 匹配正负整数和小数
                sizes = re.findall(r'-?\d+\.\d+|-?\d+', field['size'])
                sizes[0] = float(sizes[0]) if '.' in sizes[0] else int(
                    sizes[0])
                sizes[1] = float(sizes[1]) if '.' in sizes[1] else int(
                    sizes[1])
                func = {
                    # 1-3
                    '1': lambda x: -x,
                    # -1-1
                    '2': lambda x: -x,
                    # -3--1
                    '3': lambda x: x
                }
                # 根据-推算符号的位置
                sizes[1] = func[str(field['size'].count('-'))](sizes[1])
                object_item['minimum'] = sizes[0]
                object_item['maximum'] = sizes[1]
                object_item['exclusiveMinimum'] = "true"
                object_item['exclusiveMaximum'] = "true"
            # 字符串长度范围
            elif 'string' == field['type'].lower():
                sizes = field['size'].split('..')
                if sizes[0] != '':
                    object_item['minLength'] = sizes[0]
                object_item['maxLength'] = sizes[1]
    return object_item


def python_json_schema(param_type, field):
    """解析apidoc为yapi或在swagger格式的参数模板

    :param param_type: 请求类型
    :param field: 参数
    :return:
    """
    if '[]' in param_type:
        # 数组类型模板
        object_item = {
            "type": "array",
            "items": {
                "type": param_type[:-2]
            }
        }
        if 'object' == param_type[:-2]:
            # 对象数组模板
            object_item["items"]["properties"] = {}
    else:
        # 非数组模板
        object_item = {
            "type": param_type
        }
        if 'object' == param_type:
            # 对象类型模板
            object_item["properties"] = {}
        # 允许的值
        if 'allowedValues' in field.keys():
            object_item['enum'] = field['allowedValues']
        if 'size' in field.keys():
            # 数字范围
            if field['type'].lower() in ['number', 'integer']:
                # filed['size'] -> re.findall() -> result
                # -3--1 -> -3,-1 -> -3,-1
                # -1-1 -> -1,-1 -> -1,1
                # 1-3 -> 1,-3 -> 1,3
                # 匹配正负整数和小数
                sizes = re.findall(r'-?\d+\.\d+|-?\d+', field['size'])
                sizes[0] = float(sizes[0]) if '.' in sizes[0] else int(
                    sizes[0])
                sizes[1] = float(sizes[1]) if '.' in sizes[1] else int(
                    sizes[1])
                func = {
                    # 1-3
                    '1': lambda x: -x,
                    # -1-1
                    '2': lambda x: -x,
                    # -3--1
                    '3': lambda x: x
                }
                # 根据-推算符号的位置
                sizes[1] = func[str(field['size'].count('-'))](sizes[1])
                object_item['minimum'] = sizes[0]
                object_item['maximum'] = sizes[1]
            # 字符串长度范围
            elif 'string' == field['type'].lower():
                sizes = field['size'].split('..')
                if sizes[0] != '':
                    object_item['minLength'] = sizes[0]
                object_item['maxLength'] = sizes[1]
    return object_item
