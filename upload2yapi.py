# _*_ coding: utf-8 _*_
"""run with python3"""
import json
import requests
import sys


def prompt():
    """提示信息"""
    print('示例：python3 upload2yapi.py -s swagger.json -t '
          'ece1eded936607a6c09e66d63b4d152af861258d6'
          '813fd4d2cb5427b1e634a2f -i 192.168.108.123\n\n')
    print('-s swagger.json apidoc2swagger.py转换后的json文件')
    print('-t token yapi上项目的token')
    print('-i yapi url yapi的项目地址')
    print('-h help 帮助\n\n')
    print('********************************************')


def check_argv():
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
                        return prompt()

            # 如果连续两个非-开头的参数
            elif argv[0] != '-' and index != 0:
                last_argv = sys.argv[index - 1]
                if last_argv[0] != '-':
                    return prompt()
        # {参数1：值1，参数2：值2...}
        return argv_map


def upload2yapi(url, request_str):
    request_data = request_str
    request_data = json.dumps(request_data)
    headers = {'content-type': 'application/json'}

    res = requests.post(url=url, data=request_data, headers=headers)
    target = res.json()
    return target


if __name__ == '__main__':
    argvs = check_argv()
    try:
        if 'h' in argvs:
            print('所有参数都需要输入')
            prompt()
        else:
            s_file = argvs['s'] if 's' in argvs else None
            token = argvs['t'] if 't' in argvs else None
            ip = argvs['i'] if 'i' in argvs else None
            data = open(s_file, 'r', encoding='utf-8')
            json_str = json.dumps(json.load(data))
            a = {
                "type": "swagger",
                "json": json_str,
                "merge": "merge",
                "token": token
            }
            request_url = 'http://' + ip + '/api/open/import_data'
            response = upload2yapi(request_url, a)
            print(response)
            # yapi解析失败
            if response['errcode'] != 0:
                exit(1)
    except Exception as e:
        print('输入参数有误，所有参数都需要输入')
        prompt()
        raise e
