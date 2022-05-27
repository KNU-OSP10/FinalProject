# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests, json
import psycopg2

pharmacy_name = []
lat = []
long = []
address = []

## 북구 약국 데이터를 가져와 경북대 근처인지 확인한 후, 각 list에 넣음 - 26건
for num in range(1, 22):
     request_pharmacys = requests.get("https://api.odcloud.kr/api/15025684/v1/uddi:4c7db7f6-b786-4fc9-8560-87a16ca87fb5?page={}&perPage=10&serviceKey=7mNZWRMWcGvUjboFRTOFbF7lMbFLsF%2F%2Ff9wkD3vZ6DqJ8QRu4zse0OMfQDgAgbs6EZST23Ndv3j2e4gHO2we5g%3D%3D".format(num))
     js = json.loads(request_pharmacys.content)
     for num2 in range(10):
        if num == 21:
            if num2 == 2:
                break
        else:
            if(( float(js['data'][num2]['위도']) >= 35.881402 and
            float(js['data'][num2]['위도']) <= 35.902007 ) and 
            ( float(js['data'][num2]['경도']) >= 128.599561 and
             float(js['data'][num2]['경도']) <= 128.620031 )):
                pharmacy_name.append(js['data'][num2]['기관명'])
                lat.append(js['data'][num2]['경도'])
                long.append(js['data'][num2]['위도']) 
                address.append(js['data'][num2]['소재지(도로명)'])

# 35.881402 <= x <= 35.902007, 
# 128.599561 <= y <= 128.620031
con = psycopg2.connect(
host = "localhost",
    database = "seunghwan",
    user = "seunghwan",
    password = "seunghwan"
)

cur = con.cursor()
## 약국 데이터 넣기
for num3 in range(len(pharmacy_name)):
    cur.execute("insert into pharmacy_schema.bukku_list (id, lat, long, address, name ) values (%s, %s, %s, %s, %s)", (num3 + 1, lat[num3], long[num3], address[num3], pharmacy_name[num3]) )

## 입력 후 해줘야 하는 commit()
con.commit()

cur.close()

con.close()
