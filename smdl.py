# -*- coding: utf-8 -*-import random
host='http://192.168.1.1:5700'
client_id='XXXXXXXXXXX'
client_secret='XXXXXXXXXXXXXXXX'
secrett="机器人@shihuhua_bot获取的secret"

from flask import Flask, render_template
import time,json,requests
import re
app = Flask(__name__)
key=[]
@app.route('/')
def index():
    # 自动请求一个 API 并显示返回结果
    try:
        url = 'https://k557e25139.goho.co/second-api'
        token=secrett
        auto_api_response = requests.post(url,data=token)
        auto_result = auto_api_response.json()['img']
        res=auto_api_response.json()['link']
        k=auto_api_response.json()['k']
        key.append(k)
        print(auto_result)
        return render_template('index_sm.html', auto_result=auto_result,res=res),k
    except:
        return render_template('index_cw.html')

@app.route('/send_api', methods=['POST'])
def send_api():
    def evn(huhu_wsck):
        def get_token():
            url = host + "/open/auth/token?client_id={}&client_secret={}".format(client_id, client_secret)
            response = requests.request("GET", url).json()
            # print("获取青龙面板的token:", response)
            return response["data"]["token"]

        def match_ck(ck):
            token = get_token()
            pt_pin = str(re.findall(r"pin=(.+?);wskey", ck)[0])
            # print(pt_pin)
            cklist = get_all_ck(token)
            for i in cklist:
                if pt_pin in str(i["value"]):
                    # print("匹配成功，匹配到当前变量:", i)
                    id = i["_id"]
                    # print("-------------------")
                    # print("更新ck")
                    update_ck(ck, id, token)
                    if i["status"] == 1:
                        start_ck(token, id)
                        print("启用成功")
                    return
            add_ck(ck, token)
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
        def update_ck(ck, id, token):
            t = int(round(time.time() * 1000))
            url = host + "/open/envs?t=" + str(t)
            payload = json.dumps({
                "name": "huuh_wskey",
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

        def add_ck(ck, token):
            t = int(round(time.time() * 1000))
            url = host + "/open/envs?t=" + str(t)
            payload = json.dumps([
                {
                    "value": ck,
                    "name": "huuh_wskey",
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

        try:
            match_ck(huhu_wsck)
            return "上传成功"
        except:
            return "请检查青龙配置"
    url = 'https://k557e25139.goho.co/que-api'
    # print(key)
    data=key[0]
    response = requests.post(url, data=data)
    key.clear()  # 清空 key 列表
    print(key)
    if "huhu_wsck" in response.json():
        ql=evn(response.json()["huhu_wsck"])
        return render_template('index_sm.html', send_result=response.json()["huhu_wsck"],ql=ql)
    else:
        return render_template('index_cg.html', send_result=response.json())

if __name__ == '__main__':
    app.run(app.run(host='0.0.0.0', port=1111))
