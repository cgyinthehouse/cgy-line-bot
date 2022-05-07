import json
import requests

url = 'https://data.tycg.gov.tw/api/v1/rest/datastore/a1b4714b-3b75-4ff8-a8f2-cc377e4eaa0f?format=json' + '&limit=300'
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"}

req = requests.get(url, headers=headers)
datas = json.loads(req.text)


def ubike_printallinfo():
    # 取的公車  中 所有 dict 的"2001","2002".....資料
    size1 = len(datas["result"]["records"])
    for x in range(size1):
        print(x + 1,
              "中文場站名稱:" + datas["result"]["records"][x]["sna"],
              "場站總停車格:" + datas["result"]["records"][x]["tot"],
              "場站目前車輛數:" + datas["result"]["records"][x]["sbi"],
              "地址:" + datas["result"]["records"][x]["ar"],
              "場站是否暫停營運" + datas["result"]["records"][x]["act"], sep='\n')
    print(f'筆數:{size1}')


def ubike_info(station):
    for x in range(0, len(datas["result"]["records"])):
        if datas["result"]["records"][x]["sna"] == station:
            info = str(
                    "中文場站名稱:" + datas["result"]["records"][x]["sna"]+'\n'+\
                    "場站總停車格:" + datas["result"]["records"][x]["tot"]+'\n'+\
                    "場站目前車輛數:" + datas["result"]["records"][x]["sbi"]+'\n'+\
                    "地址:" + datas["result"]["records"][x]["ar"]+'\n'+\
                    "場站是否暫停營運" + datas["result"]["records"][x]["act"])
            return info

ubike_printallinfo()