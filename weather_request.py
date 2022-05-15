import json
import ssl
import sys
from datetime import datetime

try:
    import urllib2 as httplib  # 2.x
except Exception:
    import urllib.request as httplib  # 3.x

# python 08-WeatherData.py "臺北市"
print("Arguments count:", len(sys.argv))
city = " 桃園市 "
if sys.argv:
    print(f'argv1: {sys.argv[0]}\nargv2: {sys.argv[1]}')
    city = sys.argv[1]

context = ssl._create_unverified_context()
# url="https://data.tycg.gov.tw/opendata/datalist/datasetMeta/download?id=5ca2bfc7-9ace-4719-88ae-4034b9a5a55c&rid=a1b4714b-3b75-4ff8-a8f2-cc377e4eaa0f"
url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=rdec-key-123-45678-011121314"
req = httplib.Request(url)
try:
    response = httplib.urlopen(req, context=context)
    if response.code == 200:
        contents = response.read()  # .decode("UTF-8")
        data = json.loads(contents)
        t1 = data["records"]["location"]
        for item in t1:
            if city == item["locationName"]:
                print(item["weatherElement"][0]["time"][0]["parameter"]["parameterName"])
                break
        if data:
            current_time = datetime.now().strftime("%Y%m%d")  # 印出時間的格式
            fileName = f'天氣{str(current_time)}.json'
            with open(fileName, 'w') as f:
                f.write(contents.decode("UTF-8"))
except:  # 處理網路連線異常
    print("error")
