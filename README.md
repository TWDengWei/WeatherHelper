# 利用LINE Notify傳遞python所抓取API資料
## 取得氣象局API-TOKEN
到氣象局API平台註冊並取得TOKEN
> [點這裡註冊](https://opendata.cwb.gov.tw/devManual/insrtuction )
並選取預報第一個選項點選GET，接著TRYITOUT，貼上TOKEN
>[點選這裡操作](https://opendata.cwb.gov.tw/dist/opendata-swagger.html#/%E9%A0%90%E5%A0%B1/get_v1_rest_datastore_F_C0032_001)

## 取得LINE notify Token
> [點選這裡進入教學](https://ithelp.ithome.com.tw/articles/10282029)

## 程式碼區塊1
```python=
    token = "Your-API-Token"  <--輸入你的API-TOKEN
    location = "臺南市"        <-- 地點選取為你所在城市
    decode_localtion = urllib.parse.quote(location)
    params = f"Authorization={ token }&locationName={ decode_localtion }"
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?" + params
```
## 程式碼2
下述Function為從json檔中抓取各個所需要的值，分開定義實行一個Function一個動作。
```python=
    def getLocationName(data):
    def getWeather_Elements(data):
    def getStartTime(elements):
    def getEndTime(elements):
    def getWeatherName(elements):
    def getRainPoP(elements):
    def getMaxT(elements):     
    def getMinT(elements):
    def getCI(elements):
```
## 程式碼3
輸入LINE-Token
```python=
def LineNotifyMsg():

    headers = {
        "Authorization": "Bearer " + "輸入你的LINE-TOKEN", 
        "Content-Type" : "application/x-www-form-urlencoded"
    }

```
## 程式碼4
定義新一個Function，以便執行訊息存取操作
以字典型態儲存並輸出
```python=
def getMsg(data):
    if len(data) == 0:          <--- 資料長度若為0，則輸出下列資訊。
        message += "無法取得天氣預報資料"
    else:                       <---若不為0，則輸出下列文字串
        message += f"現在[{ data['LocationName'] }]的天氣: { data['WeatherName'] }"   
        message += f"\n時間為: \n{ data['StartTime'] }~ \n{ data['EndTime'] }"
        message += f"\n降雨機率: { data['RainPoP'] }%"
        message += f"\n溫度 { data['MinT'] }°C至 {data['MaxT']}°C"
        message += f"\n舒適度: { data['CI'] }"
        
        message += "\n溫馨小提醒:"
        if int(data["RainPoP"]) >50:
            message += f"\n下雨機率很大，記得帶把傘唷!!!"
        if int(data["MinT"]) <20:
            message += f"\n天氣有點冷，記得多穿點衣服!"
    return message
```


