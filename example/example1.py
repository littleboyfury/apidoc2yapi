# _*_ coding: utf-8 _*_
# @Time: 2020/9/21 09:36
# @Author: Zhang Xingjun
# @Version: V 0.1
# @File: example1.py.py


class Examples1:
    """API for Examples1"""

    def get(self):
        """get request

        @api {get} /api/examples1 获取example1列表
        @apiName ListExample1
        @apiGroup example1
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
        curl http://localhost/api/examples1?limit=5&offset=5
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

        @api {post} /api/examples1 创建example1
        @apiName CreateExample1
        @apiGroup example1
        @apiDescription api简单描述
        @apiHeader Content-Type=application/json

        @apiParam {String} a 字符串a
        @apiParam {String[]} a1 字符数组a1
        @apiParam {Boolean} b 布尔b
        @apiParam {Number} c 数字c
        @apiParam {Object} d 对象d
        @apiParam {String=A,B,C} [d.a="A"] 对象d的a字段，默认值为A，可选为A,B,C
        @apiParam
            {String=A,B,C} [d.b="A"] 对象d的a字段，默认值为A，可选为A,B,C
        @apiParam {String=A,B,C} [d.c="A"]
            对象d的a字段，默认值为A，可选为A,B,C
        @apiParam {String=A,B,C} [d.a="A"] 对象d的a字段，默认值为A，可选为A,B,C 参数过长  # noqa
        @apiParam
            {String=A,B,C} [d.aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa="A"]  # noqa
            参数过长
        @apiParam {String=A,B,C} [d.aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa="A"]  # noqa
            参数过长
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


class Example1:
    """API for Example1"""

    def get(self):
        """get request

        @api {get} /api/example1/:id 获取example1详细信息
        @apiName GetExample1Details
        @apiGroup example1
        @apiDescription api简单描述
        @apiParam (Path) {String} id example1 id

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
        curl http://localhost/api/example1/uuid
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

        @api {put} /api/example1/:id 更新example1
        @apiName UpdateExample1
        @apiGroup example1
        @apiDescription api简单描述
        @apiHeader Content-Type=application/json
        @apiParam (Path) {String} id example1 id

        @apiParam {String} a 字符串a
        @apiParam {String[]} a1 字符数组a1
        @apiParam {Boolean} b 布尔b
        @apiParam {Number} c 数字c
        @apiParam {Object} d 对象d
        @apiParam {String=A,B,C} [d.a="A"] 对象d的a字段，默认值为A，可选为A,B,C
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

        @api {delete} /api/example1/:id 删除example1
        @apiName DeleteExample1
        @apiGroup example1
        @apiDescription api简单描述
        @apiParam (Path) {String} id example1 id
        """
        pass
