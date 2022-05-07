from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from flask import render_template
line_bot_api = LineBotApi('IVzkSnELK9I3QJTuhaSHPF/ymv+fkLA8X6ZkLoFJS5FRJlDGvX0z42TxLadRTGcmXoC8ysu4FxycyV/yYOE9IVsqw6OiGEpPp3N4zp4zXNKh22LFbPHtWBnjwZl8WVWePSMqQAJ5TmChyBI0yFwGgQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('14f1d3cfab824b0a56b29a7029e9fd3e')

# http://127.0.0.1:5000/

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@app.route("/ubike")
def ubike():
    str1="ubike!"
    return str1



@app.route("/fun1", methods=['GET'])
def fun1():
    用戶輸入的文字 = request.args.get('用戶輸入的文字')
    # 回傳值, Log文字 = mylibs.Line_處理用的問題v2(用戶輸入的文字, sheet問答題)
    return "  用戶輸入的文字=" + 用戶輸入的文字

@app.route('/', methods=['GET', 'POST'])
def index():
    str1 = render_template('index.html', 標題1="Python 課程", 內容1="你好啊～")
    return str1


if __name__ == '__main__':
    app.run(port=5000)

