import requests
from bs4 import BeautifulSoup as bs
import math
import time
from dateutil import parser as timeparser
import datetime as dt

import config
import functions as fn




#Get position&time predictions of the ISS
#Time is in UTC
def getFlyOverData(location, targetDate):
    payload = {
        "lang": "en",
        "satellite": "ISS",
        "count": 10,
        "loc": "",
        "lat": location.latitude,
        "latdir": "+" if location.latitude > 0 else "-",
        "lng": location.longitude,
        "longdir": "+" if location.longitude > 0 else "-",
        "ele": 0,
        "doPredict": "Predict"
    }

    #!!! ONLY FOR TESTING TO NOT SEND THOUSANDS OF REQUESTS TO THE SERVER
    #data = requests.get(config.PosPredURL, payload)
    data = open("cachedRequestForFlyOverData.txt").read()
    if False:#data.status_code != 200:
        print("Error: " + str(data.status_code))
    else:
        soup = bs(data, features="html.parser")#.text)
        elemsRaw = [None, None]
        elemsRaw[0] = soup.find_all('tr', {"bgcolor": "white"})[:math.ceil(payload["count"]/2)]
        elemsRaw[1] = soup.find_all('tr', {"bgcolor": "gainsboro"})[:round(payload["count"]/2)]
        
        elems = [None for i in range(len(elemsRaw[0]) + len(elemsRaw[1]))]
        for idx, ele in enumerate(elemsRaw[0]):
            elems[idx*2] = ele.find_all('td')
        for idx, ele in enumerate(elemsRaw[1]):
            elems[idx*2 +1] = ele.find_all('td')
        
        finalElems2 = []
        for ele in elems:
            #print(ele)
            el = str(ele).split(",")
            temp = []
            for e in  el:
                e = e[2:]
                e = e[e.find(">")+1:e.find("<")]
                temp.append(e)
            finalElems2.append(temp)
        
        finalElems = []
        for ele in finalElems2:
            dateTransform = timeparser.parse(ele[0])
            date = dt.date(dateTransform.year, dateTransform.month, dateTransform.day)
            ele[1] = ele[1].split(":")
            ele[2] = ele[2].split(":")
            ele[7] = ele[7].split(":")
            starttime = dt.time(int(ele[1][0]), int(ele[1][1]), int(ele[1][2]))
            duration = dt.time(int(ele[2][0]), int(ele[2][1]), int(ele[2][2]))
            endtime = dt.time(int(ele[7][0]), int(ele[7][1]), int(ele[7][2]))
            frame = fn.FlyoverFrame(date, starttime, duration, endtime)
            finalElems.append(frame)
        
        
        # print("Date, Starttime, Duration, Endtime")
        # for ele in finalElems:
        #     print(ele.date, ele.starttime, ele.duration, ele.endtime)
        
            
        #get only targetDate flyovers
        #today = dt.date.today()
        targetDayFlyovers = []
        for ele in finalElems:
            if ele.date == targetDate:
                targetDayFlyovers.append(ele)
        print()
        print(f"Todays flyovers in {location.name}, {location.country} on {targetDate}:")
        # print('{:^10} {:^8} {:^8} {:^8}'.format(*["Date", "Starttime", "Duration", "Endtime"]))
        print("   Date    Startime Duration Endtime")
        for ele in targetDayFlyovers:
            print(ele.date, ele.starttime, ele.duration, ele.endtime)
        return targetDayFlyovers
            


locations = [
    fn.Location(44.84175, 0.56681, "Bordeaux", "France", "http://ham.websdrbordeaux.fr:8000/index3.html"),
    fn.Location(36.98038, 22.44201, "Sparti", "Greece", "http://sv3gcb.ddns.net:8905/"),
    fn.Location(45.1875, 25.625, "Breaza", "Romania", "http://websdr.yo3ggx.ro:8765/"),
    fn.Location(52.02366, 5.03883, "IJsselstein", "Netherlands", "http://websdr.pi1utr.hamnet.nl:8901/")
]

for location in locations:
    getFlyOverData(location, dt.date.today() + dt.timedelta(days=0))