# _*_ coding: utf-8 _*_
# @Time: 2020/9/21 09:36
# @Author: Zhang Xingjun
# @Version: V 0.1
# @File: example2.py.py


class Examples2:
    """API for Examples2"""

    def get(self):
        """get request

        @api {get} /api/examples2 获取example2列表
        @apiName ListExample2
        @apiGroup example2
        @apiDescription api简单描述
        @apiParam (Query) {Number} limit 分页操作
        @apiParam (Query) {Number} offset 分页操作

        @apiSuccess {Object[]} data 根对象数组
        @apiSuccess {String} data.id id
        @apiSuccess {String} data.a 字符串a
        @apiSuccess {String[]} data.a1 字符数组a1
        @apiSuccess {Boolean} data.b 布尔b
        @apiSuccess {Number} data.c 数字c
        @apiSuccess {Object} data.d 对象d
        @apiSuccess {String} data.d.a 对象d的a字段
        @apiSuccess {Number} data.d.b 对象d的b字段
        @apiSuccessExample {JSON} 响应示例
        1. 说明写这里1
        2. 说明写这里2
        curl http://localhost/api/examples2?limit=5&offset=5
        {
          "data": [
            {
              "id": "uuid",
              "a": "",
              "a1": [],
              "b": true,
              "c": 1,
              "d": {
                "a": "A",
                "b": 1
              }
            }
          ]
        }
        """
        pass

    def post(self):
        """post request

        @api {post} /api/examples2 创建example2
        @apiName CreateExample2
        @apiGroup example2
        @apiDescription api简单描述
        @apiHeader Content-Type=application/json

        @apiParam {String} a 字符串a
        @apiParam {String[]} a1 字符数组a1
        @apiParam {Boolean} b 布尔b
        @apiParam {Number} c 数字c
        @apiParam {Object} d 对象d
        @apiParam {String=A,B,C} d.a="A" 对象d的a字段，默认值为A，可选为A,B,C
        @apiParam {Number} d.b 对象d的b字段
        @apiParamExample {JSON} 请求示例
        1. 说明写这里1，可以不写
        2. 说明写这里2，可以不写
        {
          "a": "",
          "a1": [],
          "b": true,
          "c": 1,
          "d": {
            "a": "A",
            "b": 1
          }
        }

        @apiSuccess {String} id id
        @apiSuccess {String} a 字符串a
        @apiSuccess {String[]} a1 字符数组a1
        @apiSuccess {Boolean} b 布尔b
        @apiSuccess {Number} c 数字c
        @apiSuccess {Object} d 对象d
        @apiSuccess {String} d.a 对象d的a字段
        @apiSuccess {Number} d.b 对象d的b字段
        @apiSuccessExample {JSON} 响应示例
        1. 说明写这里1，可以不写
        2. 说明写这里2，可以不写
        {
          "id": "uuid",
          "a": "",
          "a1": [],
          "b": true,
          "c": 1,
          "d": {
            "a": "A",
            "b": 1
          }
        }
        """
        pass


class Example2:
    """API for Example2"""

    def get(self):
        """get request

        @api {get} /api/example2/:id 获取example2详细信息
        @apiName GetExample2Details
        @apiGroup example2
        @apiDescription api简单描述
        @apiParam (Path) {String} id example2 id

        @apiSuccess {String} id id
        @apiSuccess {String} a 字符串a
        @apiSuccess {String[]} a1 字符数组a1
        @apiSuccess {Boolean} b 布尔b
        @apiSuccess {Number} c 数字c
        @apiSuccess {Object} d 对象d
        @apiSuccess {String} d.a 对象d的a字段
        @apiSuccess {Number} d.b 对象d的b字段
        @apiSuccessExample {JSON} 响应示例
        1. 说明写这里1
        2. 说明写这里2
        curl http://localhost/api/example2/uuid
        {
          "id": "uuid",
          "a": "",
          "a1": [],
          "b": true,
          "c": 1,
          "d": {
            "a": "A",
            "b": 1
          }
        }
        """
        pass

    def put(self):
        """put request

        @api {put} /api/example2/:id 更新example2
        @apiName UpdateExample2
        @apiGroup example2
        @apiDescription api简单描述
        @apiHeader Content-Type=application/json
        @apiParam (Path) {String} id example2 id

        @apiParam {String} a 字符串a
        @apiParam {String[]} a1 字符数组a1
        @apiParam {Boolean} b 布尔b
        @apiParam {Number} c 数字c
        @apiParam {Object} d 对象d
        @apiParam {String=A,B,C} d.a="A" 对象d的a字段，默认值为A，可选为A,B,C
        @apiParam {Number} d.b 对象d的b字段
        @apiParamExample {JSON} 请求示例
        1. 说明写这里1，可以不写
        2. 说明写这里2，可以不写
        {
          "a": "",
          "a1": [],
          "b": true,
          "c": 1,
          "d": {
            "a": "A",
            "b": 1
          }
        }

        @apiSuccess {String} id id
        @apiSuccess {String} a 字符串a
        @apiSuccess {String[]} a1 字符数组a1
        @apiSuccess {Boolean} b 布尔b
        @apiSuccess {Number} c 数字c
        @apiSuccess {Object} d 对象d
        @apiSuccess {String} d.a 对象d的a字段
        @apiSuccess {Number} d.b 对象d的b字段
        @apiSuccessExample {JSON} 响应示例
        1. 说明写这里1，可以不写
        2. 说明写这里2，可以不写
        {
          "id": "uuid",
          "a": "",
          "a1": [],
          "b": true,
          "c": 1,
          "d": {
            "a": "A",
            "b": 1
          }
        }
        """
        pass

    def delete(self):
        """delete request

        @api {delete} /api/example2/:id 删除example2
        @apiName DeleteExample2
        @apiGroup example2
        @apiDescription api简单描述
        @apiParam (Path) {String} id example2 id
        """
        pass
