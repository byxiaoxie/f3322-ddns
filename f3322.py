# Update f3322 IP
# API文档 [https://www.pubyun.com/wiki/帮助:api]
#
# Update Log:
# 2021-11-23 05:26:56 - Fix stack overflow.
# 2021-11-24 10:39:53 - Change to two minute update.
# 2021-11-24 11:23:14 - Add getip url.
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

def GetIp(mod):
    try:
        if mod:
            req = request.Request("http://ipinfo.io/ip")
        else:
            req = request.Request("http://ip.3322.net")
        conn = request.urlopen(req).read().decode('GBK')
        ipaddr = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',conn)
        ipaddress = ipaddr.group()
        return ipaddress
    except:
        print_log("Get IP Time Out!")
        return ""

def UpdateIP():
    try:
        while True:
            BoolGetIp = True
            ipaddress = GetIp(BoolGetIp)
            if ipaddress != "":
                break
            else:
                if BoolGetIp:
                    BoolGetIp = False
                else:
                    BoolGetIp = True
                time.sleep(5)
                ipaddress = GetIp(BoolGetIp)

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
        time.sleep(120)