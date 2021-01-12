# apidoc2yapi

该代码是参考[zhangchun617](https://github.com/zhangchun617/apidoc2yapi) 的代码修
改而成，用于apidoc生成的json文件转化为yapi可导入的json文件，只支持json类型的请求和相应参数，
可以解析个各种类型的参数和各种嵌套的参数，如果有bug，希望能够指出。

我公司的思路是git提交的时候自动运行apidoc检查和提交到yapi上的检查来判断注释是否规范，
同时每次提交都会更新yapi中的api文档，达到只需要在代码中修改apidoc的注释，同步更新yapi。
缺点：接口中的注释会很多，不支持apidoc的不同版本的api。

支持转化为jsonschema请求格式检查转换，大致转换，需要自行修改
​帮助文档:[help.md](./doc/help.md)

​Email:cxjwllxm@gmail.com

