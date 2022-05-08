# 技術文章
# https://developers.line.biz/en/docs/messaging-api/sending-messages/#methods-of-sending-message
import os.path
import requests
import json
import time, datetime                      # 時間
from openpyxl import load_workbook,Workbook
# from sys import version as python_version
# from cgi import parse_header, parse_multipart
import socketserver as socketserver
# import http.server
from http.server import SimpleHTTPRequestHandler as RequestHandler
# from urllib.parse import parse_qs
auth_token='IVzkSnELK9I3QJTuhaSHPF/ymv+fkLA8X6ZkLoFJS5FRJlDGvX0z42TxLadRTGcmXoC8ysu4FxycyV/yYOE9IVsqw6OiGEpPp3N4zp4zXNKh22LFbPHtWBnjwZl8WVWePSMqQAJ5TmChyBI0yFwGgQdB04t89/1O/w1cDnyilFU='


def line_question_lookup(userinput):
    wb = load_workbook('../0504/line_response.xlsx')  # 讀取檔案
    sheet1 = wb.worksheets[0]  # 方法一打開第一個 工作表單
    questions = {}
    for row in sheet1.iter_rows():
        questions[row[0].value] = [row[1].value, row[2].value]
    # fixme:購買key（同個cell多個Key）
    template = {
        "type": "template",
        "altText": "This is a buttons template",
        "template": {
            "type": "buttons",
            "thumbnailImageUrl": 'https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2F25.media.tumblr.com%2Ftumblr_mbovzzeaEB1qldni8o1_500.jpg&f=1&nofb=1',
            "imageAspectRatio": "rectangle",
            "imageSize": "cover",
            "imageBackgroundColor": "#FFFFFF",
            "title": "Menu",
            "text": "Please select",
            "defaultAction": {
                "type": "uri",
                "label": "View detail",
                "uri": "http://www.powenko.com/download_release/get.php"
            },
            "actions": [
                {
                    "type": "uri",
                    "label": "填寫線上問卷",
                    "uri": "https://forms.gle/vdHfmWijtcBTsPNX6"
                },
                {
                    "type": "uri",
                    "label": "產品詳細資訊",
                    "uri": "http://www.yahoo.com"
                }
            ]
        }
    }
    # 根據使用者輸入回傳查表後結果
    for key in questions.keys():
        if key in userinput and questions[key][1] == 'text':
            msg_return = {"type": "text", "text": questions[key][0]}
            return msg_return
        elif key in userinput and questions[key][1] == 'template':
            msg_return = template
            return msg_return
    else:
        msg_return = {'type': "text",
                      'text': 'Unable to recognize user\'s input'}
        return msg_return


class MyHandler(RequestHandler):
    def do_POST(self):
        varLen = int(self.headers['Content-Length'])        # 取得讀取進來的網路資料長度
        if varLen > 0:
            post_data = self.rfile.read(varLen)             # 讀取傳過來的資料
            data = json.loads(post_data)                    # 將json格式的字串轉爲字典格式
            print(data)
            replyToken=data['events'][0]['replyToken']       # 回郵信封(Reply Token)可以不用花錢
            userId3=data['events'][0]['source']['userId']    # 傳資料過來的使用者是誰
            userInput=data['events'][0]['message']['text']        # 用戶的傳遞過來的文字內容
            returnType =data['events'][0]['message']['type'] # 傳過來的資料型態
            time1 = data['events'][0]['timestamp']  # 傳過來的資料型態
            time2 = str(datetime.datetime.fromtimestamp(time1/1000))

        message = {
            "replyToken": replyToken,
            "messages": [line_question_lookup(userInput)]
                  }
        # 資料回傳 到 Line 的 https 伺服器
        hed = {'Authorization': 'Bearer ' + auth_token}
        url = 'https://api.line.me/v2/bot/message/reply'
        self.send_response(200)
        self.end_headers()
        requests.post(url, json=message, headers=hed)      # 把資料HTTP POST送出去

        # log file handling
        if not os.path.exists('../0504/Log.xlsx'):
            log = Workbook()
            sheet1 = log.active
            sheet1.append(['UserID','UserInput','BotReply','Timestamp'])
        else:
            log = load_workbook('../0504/Log.xlsx')
        sheet1 = log.active
        if 'text' in message['messages'][0].keys():
            sheet1.append([userId3,userInput,message['messages'][0]['text'],time2])
        else:
            sheet1.append([userId3, userInput, 'nontextreply', time2])
        log.save('Log.xlsx')

socketserver.TCPServer.allow_reuse_address = True              # 可以重複使用IP
httpd = socketserver.TCPServer(('0.0.0.0', 8888), MyHandler)  # 啟動WebServer   :8888
try:
    httpd.serve_forever()                          # 等待用戶使用 WebServer
except:
    print("Closing the server.")
    httpd.server_close()                           # 關閉 WebServer

