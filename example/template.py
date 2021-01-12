# _*_ coding: utf-8 _*_


class Template:
    """API for Template"""

    def get(self, test_param):
        """get request

        :param test_param: test param

        @api {get} /api/template 获取template列表
        @apiName ListTemplate
        @apiGroup template
        @apiDescription api简单描述
        @apiParam (Query) {Number} limit 分页操作
        @apiParam (Query) {Number} offset 分页操作

        @apiSuccess {Object[]} datas 根对象数组
        @apiSuccessExample {JSON} 响应示例
        1. 说明写这里，可以不写，格式不会变
        curl http://localhost/api/template?limit=5&offset=5
        {}
        """
        pass

    def post(self):
        """post request

        @api {post} /api/template 创建template
        @apiName CreateTemplate
        @apiGroup template
        @apiDescription api简单描述
        @apiHeader Content-Type=application/json

        @apiParam {Object} data 根对象
        @apiParamExample {JSON} 请求示例
        1. 说明写这里，可以不写
        {}

        @apiSuccess {Object} data 根对象
        @apiSuccessExample {JSON} 响应示例
        1. 说明写这里，可以不写
        {}
        """
        pass

    def put(self):
        """t request

        @api {put} /api/template/:id 更新template
        @apiName UpdateTemplate
        @apiGroup template
        @apiDescription api简单描述
        @apiHeader Content-Type=application/json
        @apiParam (Path) {String} id template id

        @apiParam {Object} data 根对象
        @apiParamExample {JSON} 请求示例
        1. 说明写这里，可以不写
        {}

        @apiSuccess {Object} data 根对象
        @apiSuccessExample {JSON} 响应示例
        1. 说明写这里，可以不写
        {}
        """
        pass

    def delete(self):
        """delete request

        @api {delete} /api/template/:id 删除template
        @apiName DeleteTemplate
        @apiGroup template
        @apiDescription api简单描述
        @apiParam (Path) {String} id template id
        """
        pass

