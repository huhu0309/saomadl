# -*- coding: utf-8 -*-import random
host='http://192.168.1.1:5700'
client_id='XXXXXXXXXXX'
client_secret='XXXXXXXXXXXXXXXX'
secrett="机器人@shihuhua_bot获取的secret"


from flask import Flask, render_template
import time,json,requests
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
    def get_token(wskey):
        try:
            url = host + "/open/auth/token?client_id=" + client_id + "&client_secret=" + client_secret
            response = requests.request("GET", url).json()
            token = response["data"]["token"]
            print(token)
            t = int(round(time.time() * 1000))
            url1 = host + "/open/envs?t=" + str(t)
            payload = json.dumps([
                {
                    "value": wskey,
                    "name": "huuh_wskey",
                }
            ])
            headers = {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json'
            }
            # print("添加成功")
            response = requests.request("POST", url1, headers=headers, data=payload)
            print(response.json())
            return "上传成功"
        except:
            return "请检查青龙配置"
    url = 'https://k557e25139.goho.co/que-api'
    print(key)
    data=key[0]
    response = requests.post(url, data=data)
    key.clear()  # 清空 key 列表
    print(key)
    if "huhu_wsck" in response.json():
        get_token(response.json()["huhu_wsck"])
        return render_template('index_sm.html', send_result=response.json()["huhu_wsck"])
    else:
        return render_template('index_cg.html', send_result=response.json())
if __name__ == '__main__':
    app.run(app.run(host='0.0.0.0', port=1111))
