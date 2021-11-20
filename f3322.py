# Update f3322 IP
# API文档 [https://www.pubyun.com/wiki/帮助:api]
# ByXiaoXie   Www.ByXiaoXie.Com

import time
import re
import base64
import urllib
from urllib import request

def print_log(str):
    if len(str) <= 2:
        return
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(now + "：" + str)

    with open("f3322.log","a") as file:
            file.write(now + "：" + str +"\n")
    

def GetIp():
    try:
        conn = request.urlopen("http://www.f3322.org/dyndns/getip",timeout=10)
        reip = conn.read()
        reip = reip.decode('GBK')
        ipaddr = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',reip)
        ipaddress = ipaddr.group()
        #print_log("IP:",ipaddress)
        return ipaddress
    except:
        print_log("Get IP Time Out!")
        time.sleep(5)
        GetIp()

def UpdateIP():
    try:
        ipaddress = GetIp()
        domainname = ""
        username = ""
        password = ""
    
        user_info_str = username + ":" + password
        user_info = base64.b64encode(user_info_str.encode())

        headers = {
        'Host': 'members.3322.net',
        'Authorization': "Basic " + user_info.decode(),
        'User-Agent': 'myclient/1.0 me@null.net',
        }

        url = "http://members.3322.net/dyndns/update?hostname=" + domainname + "&myip=" + ipaddress + "&wildcard=OFF&mx=mail.exchanger.ext&backmx=NO&offline=NO"
        req = request.Request(url,headers=headers)
        getpost = request.urlopen(req).read().decode('utf-8')
        print_log(getpost)
        
        time.sleep(60)
        UpdateIP()
    except:
        print_log("Update Error!")
        time.sleep(5)
        UpdateIP()

if __name__ == "__main__":
    UpdateIP()