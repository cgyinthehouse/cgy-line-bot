import flask     # pip install flask
from flask import render_template
from flask import request
import mylibs
import json
# 測試 請透過
# http://127.0.0.1:5000/
# http://127.0.0.1:5000/chat
# http://127.0.0.1:5000/func1?userInput=你好
# http://127.0.0.1:5000/func1?userInput=健行科技大學的ubike
# http://127.0.0.1:5000/func1?userInput=健行科技大學的ubike&format=json
# 在 python 執行檔的目錄下，創建 templates/ 資料夾
# 本程式.py
# templates/data1.html
# templates/data2.html

sheetQA = mylibs.openpyxl_open_sheet('line.xlsx', "問答題")   # 取得要用來查詢的excel sheet

app = flask.Flask(__name__,static_url_path='/static')


@app.route("/func1", methods=['GET'])
def func1():
    userInput = request.args.get('userInput')
    format = request.args.get('format')
    retval, logtext = mylibs.line_get_response(userInput, sheetQA)
    if format == "json":  # 當使用者指定回傳json格式時
        dict1 = {"用戶輸入的文字": userInput,
                 "response": logtext}
        # json.dumps(dict) # 是將字典轉換為字串
        json_str = json.dumps(dict1, ensure_ascii=False)  # ensure_ascii=False 讓中文正常顯示
        return json_str
    else:
        return logtext


@app.route('/', methods=['GET', 'POST'])
def index():
    str1 = render_template('index.html', 標題1="Python 課程", 內容1="你好啊～")
    return str1


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    str1 = render_template('聊天室.html', 標題1="Python 課程", 內容1="你好啊～")
    return str1


if __name__ == '__main__':
    app.run(port=5000)
