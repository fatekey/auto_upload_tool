# Auto Upload Tool
为了更方便快速的测试文件上传漏洞写的工具
+ 根据系统、中间件、脚本语言生成字典
+ 进行文件上传测试,根据返回包确定是否上传成功
+ 绕过waf文件上传
+ 条件竞争文件上传
# 使用方法
```

 _    _       _                 _     _______ ____   ____  _      
| |  | |     | |               | |   |__   __/ __ \ / __ \| |     
| |  | |_ __ | | ___   __ _  __| |______| | | |  | | |  | | |     
| |  | | '_ \| |/ _ \ / _` |/ _` |______| | | |  | | |  | | |     
| |__| | |_) | | (_) | (_| | (_| |      | | | |__| | |__| | |____ 
 \____/| .__/|_|\___/ \__,_|\__,_|      |_|  \____/ \____/|______|
       | |                                                        
       |_|  
                                Author: @fatekey                                              
    
usage: upload.py [-h] [-l {asp,php,jsp,all}] [-o {win,linux,all}] [-m {iis,apache,tomcat,nginx}] [-a ALLOW_SUFFIX] [-u URL] [-t TEXT]
                 [--mode {upload,waf,race,dic}]

A auto upload fuzz tool

optional arguments:
  -h, --help            show this help message and exit
  -l {asp,php,jsp,all}, --language {asp,php,jsp,all}
                        上传文件扩展名
  -o {win,linux,all}, --os {win,linux,all}
                        目标操作系统
  -m {iis,apache,tomcat,nginx}, --middleware {iis,apache,tomcat,nginx}
                        目标中间件类型
  -a ALLOW_SUFFIX, --allow ALLOW_SUFFIX
                        允许上传的文件后缀
  -u URL, --url URL     上传成功路径,用于检测是否上传成功
  -t TEXT, --text TEXT  上传成功文本,用于检测是否上传成功
  --mode {upload,waf,race,dic}
                        模式,upload:自动上传测试,waf:绕过waf,race:条件竞争,dic:导出字典到剪切板
```
通过 `--mode `指定模式,默认为`dic`模式
## dic
根据选择的中间件、操作系统等信息生成字典并复制到剪切板,方便在 burpsuite 中使用
## upload
复制burpsuite中抓到的文件上传数据包,程序会根据数据包自动进行上传测试,生成字典的规则同dic模式,可以通过-t指定上传成功的字符串
## waf
复制burpsuite中抓到的文件上传数据包,不会修改文件后缀名,而是会通过修改数据包里的一些特征尝试绕过 waf
## race
复制burpsuite中抓到的文件上传数据包,并指定上传成功后的路径,程序启动 20 线程进行上传和访问请求各 1000 次,访问结果为 200 则认为上传成功.
# 参考项目
+ https://github.com/boy-hack/hack-requests
+ https://github.com/c0ny1/upload-fuzz-dic-builder