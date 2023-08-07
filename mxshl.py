
"""
File: mxshl.py
作者：胡胡
cron:  0 8,16,23 * * *
new Env('huhu_wskey转换');
"""
host='http://192.165.123.182:5700'
client_id='XXXXXXXXXXXXXX'
client_secret='XXXXXXXXXXXXXXXXXXXX'



import os
import requests
import logging
import time
import requests
import json
import re
import time


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
cookies = []

def getCookie():
    global cookies
    try:
        if "huuh_wskey" in os.environ:
            if len(os.environ["huuh_wskey"]) > 10:
                cookies.append(os.environ["huuh_wskey"])
                # logging.info("当前从环境变量获取CK")
                return cookies
    except Exception as e:
        logging.error(f"【getCookie Error】{e}")




def evn(huhu_wsck):
    def get_token():
        url = host + "/open/auth/token?client_id={}&client_secret={}".format(client_id, client_secret)
        response = requests.request("GET", url).json()
        # print("获取青龙面板的token:", response)
        return response["data"]["token"]
    def match_ck(ck):
        token=get_token()
        pt_pin = str(re.findall(r"pt_pin=(.+?);", ck)[0])
        # print(pt_pin)
        cklist = get_all_ck(token)
        for i in cklist:
            if pt_pin in str(i["value"]):
                # print("匹配成功，匹配到当前变量:", i)
                id = i["_id"]
                # print("-------------------")
                # print("更新ck")
                update_ck(ck, id,token)
                if i["status"] == 1:
                    start_ck(token,id)
                    print("启用成功")
                return
        add_ck(ck,token)
        return


    # 获取所有的变量
    def get_all_ck(token):
        t = int(round(time.time() * 1000))
        url = host + "/open/envs?searchValue=&t=" + str(t)
        payload = ""
        headers = {
            'Authorization': 'Bearer ' + token
        }
        response = requests.request("GET", url, headers=headers, data=payload).json()

        return response["data"]


    # 更新变量
    def update_ck(ck,  id,token):
        t = int(round(time.time() * 1000))
        url = host + "/open/envs?t=" + str(t)
        payload = json.dumps({
            "name": "JD_COOKIE",
            "value": ck,
            "_id": id
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        print(f"更新{ck}")
        response = requests.request("PUT", url, headers=headers, data=payload)
        return response


    def add_ck(ck,token):
        t = int(round(time.time() * 1000))
        url = host + "/open/envs?t=" + str(t)
        payload = json.dumps([
            {
                "value": ck,
                "name": "JD_COOKIE",
            }
        ])
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }
        print("添加变量")
        response = requests.request("POST", url, headers=headers, data=payload)
        return response


    def start_ck(token, id):
        t = int(round(time.time() * 1000))
        url = host + "/open/envs/enable?t=" + str(t)
        print(id)
        list = []
        list.append(id)
        payload = json.dumps(
            list
        )
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }
        print("启用ck：", payload)
        response = requests.request("PUT", url, headers=headers, data=payload)
        return
    url = 'https://k557e25139.goho.co/zhuanhuan'
    data = huhu_wsck
    response = requests.post(url, data=data)
    # print(response)
    if response.status_code == 200:
        # print(response.status_code)
        # print(data)
        # print(response.json())
        if response.json()["success"]==0:
            print(f"{data}失效请重新获取")
        else:
            # print(response.json()["huhu_wsck"])
            match_ck(response.json()["huhu_wsck"])
    else:
        print(f"Request failed with status code: {response.status_code}")


data = getCookie()
if data:
    data_str = str(data[0])
    variable_list = data_str.split('&')
    # print(variable_list)
    for i in range(len(variable_list)):
        # logging.info(variable_list[i])
        # print(variable_list[i])
        evn(variable_list[i])
        time.sleep(0.1)
else:
    logging.error("未获取到Cookie信息")



