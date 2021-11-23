# Update f3322 IP
# API文档 [https://www.pubyun.com/wiki/帮助:api]
#
# Update Log:
# 2021-11-23 05:26:56 - Fix stack overflow.
#
# ByXiaoXie   Www.ByXiaoXie.Com

import time
import re
import base64
import urllib
from urllib import request

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

def print_log(str):
    if not str.strip():
        return
    str = str.replace("\r","").replace("\n","")
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(now + "：" + str)

    with open("f3322.log","a") as file:
            file.write(now + "：" + str + "\n")

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
        return ""

def UpdateIP():
    try:
        while True:
            ipaddress = GetIp()
            if ipaddress != "":
                break
            else:
                time.sleep(5)
                ipaddress = GetIp()

        url = "http://members.3322.net/dyndns/update?hostname=" + domainname + "&myip=" + ipaddress + "&wildcard=OFF&mx=mail.exchanger.ext&backmx=NO&offline=NO"
        req = request.Request(url,headers=headers)
        getpost = request.urlopen(req).read().decode('utf-8')
        print_log(getpost)
        
        return True
    except:
        print_log("Update Error!")
        return False

if __name__ == "__main__":
    while True:
        UpdateIP()
        time.sleep(60)