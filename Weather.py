import json
import requests
import urllib.parse
import urllib.request


def getWeather():
    token = "Your-API-Token"
    location = "臺南市"
    
    
    decode_localtion = urllib.parse.quote(location)
    params = f"Authorization={ token }&locationName={ decode_localtion }"
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?" + params
    
    try:      
        re = requests.get(url)
        
        if re.status_code == 200:
            w_data = json.loads(re.text)
            z_data = getWeather_Elements(w_data) 
        
            result = {}
            result["LocationName"] = getLocationName(w_data)
            result["StartTime"] = getStartTime(z_data)
            result["EndTime"] =  getEndTime(z_data)
            result["WeatherName"] = getWeatherName(z_data)
            result["RainPoP"] = getRainPoP(z_data)
            result["MaxT"] = getMaxT(z_data)
            result["MinT"] = getMinT(z_data)
            result["CI"] = getCI(z_data)
            
            
            LineNotifyMsg(getMsg(result))
        else:
            print("抓不到資料!")
            
    except requests.exceptions.ConnectionError as ce:
        print("Remote Server Error")
        
    except Exception as e:
        print(e)
        
def getLocationName(data):
    return  data["records"]["location"][0]["locationName"]

def getWeather_Elements(data):
    return data["records"]["location"][0]["weatherElement"]

def getStartTime(elements):
    return elements[0]["time"][0]["startTime"]

def getEndTime(elements):
    return elements[0]["time"][0]["endTime"]

def getWeatherName(elements):
    return elements[0]["time"][0]["parameter"]["parameterName"] 

def getRainPoP(elements):
    return elements[1]["time"][0]["parameter"]["parameterName"]#降雨機率

def getMaxT(elements):     
    return  elements[4]["time"][0]["parameter"]["parameterName"] #最高溫度

def getMinT(elements):
    return elements[2]["time"][0]["parameter"]["parameterName"] #最低溫度

def getCI(elements):
    return elements[3]["time"][0]["parameter"]["parameterName"] #舒適度

def LineNotifyMsg(msg):
    
    url = "https://notify-api.line.me/api/notify"
    
    headers = {
        "Authorization": "Bearer " + "Your-LineNotify-Token", 
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    
    Msg = {
        'message': msg
    }
    
    r = requests.post(url=url, headers=headers, data=Msg)
    #return r.status_code

def getMsg(data):
    
    message = "\n"
    
    if len(data) == 0:
        message += "無法取得天氣預報資料"
    else:
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
    

if __name__ == "__main__":
    getWeather()