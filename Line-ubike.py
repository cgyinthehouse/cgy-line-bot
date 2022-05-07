import requests
from JSON_ubike_api import info_bystation
# 一定要改的地方～～
auth_token="IVzkSnELK9I3QJTuhaSHPF/ymv+fkLA8X6ZkLoFJS5FRJlDGvX0z42TxLadRTGcmXoC8ysu4FxycyV/yYOE9IVsqw6OiGEpPp3N4zp4zXNKh22LFbPHtWBnjwZl8WVWePSMqQAJ5TmChyBI0yFwGgQdB04t89/1O/w1cDnyilFU="

# from sys import version as python_version
# from cgi import parse_header, parse_multipart
import socketserver as socketserver
import http.server
from http.server import SimpleHTTPRequestHandler as RequestHandler
from urllib.parse import parse_qs
import json
import requests

class MyHandler(RequestHandler):
    def do_POST(self):
        varLen = int(self.headers['Content-Length'])        # 取得讀取進來的網路資料長度
        if varLen > 0:
            post_data = self.rfile.read(varLen)             # 讀取傳過來的資料
            data = json.loads(post_data)                    # 把字串 轉成JSON
            print(data)
            replyToken=data['events'][0]['replyToken']       # 回傳要用Token
            userId3=data['events'][0]['source']['userId']    # 傳資料過來的使用者是誰
            userInput=data['events'][0]['message']['text']        # 用戶的傳遞過來的文字內容
            傳過來的資料型態=data['events'][0]['message']['type'] # 傳過來的資料型態

        # 請參考
        # https://developers.line.biz/zh-hant/docs/messaging-api/sending-messages/#methods-of-sending-message
        message = {
            "replyToken":replyToken,
            "messages": [
                {
                    "type": "text",
                    "text": info_bystation(userInput)
                }
            ]
        }

        # 資料回傳 到 Line 的 https 伺服器
        hed = {'Authorization': 'Bearer ' + auth_token}
        url = 'https://api.line.me/v2/bot/message/reply'
        self.send_response(200)
        self.end_headers()
        requests.post(url, json=message, headers=hed)      # 把資料HTTP POST送出去



socketserver.TCPServer.allow_reuse_address = True              # 可以重複使用IP
httpd = socketserver.TCPServer(('0.0.0.0', 5000), MyHandler)  # 啟動WebServer   :8888
try:
    httpd.serve_forever()                          # 等待用戶使用 WebServer
except:
    print("Closing the server.")
    httpd.server_close()                           # 關閉 WebServer


"""
{
"destination":"Uc56db95c5bdabf2405a3c1c5afb5466d",
"events":[
   {"type":"message",
    "message":{
        "type":"text",
        "id":"16026143839698",
        "text":"111"},
    "webhookEventId":"01G26BHBNVMG06ZSEE27G4GJDB",
    "deliveryContext":{"isRedelivery":false},
    "timestamp":1651628355014,
    "source":{
        "type":"user",
        "userId":"U22869b7bf55a2026578867d615fe8c11"},
        "replyToken":"d35b62f1927d42b0ba4523d79e92e84e",
        "mode":"active"}
    ]
}'


"""