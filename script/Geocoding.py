# -*- coding:utf-8 -*-
import requests
import pandas as pd
import json
from urllib.request import urlopen, quote
import time

def getlnglat(address):
    url = 'http://restapi.amap.com/v3/geocode/geo'
    params = {'key': '0d5246d56226a35c2ecbedca4ee5ad1d',
              'output': 'JSON',
              'address': address,
              'city': 'shenzhen'}
    # output = 'JSON'
    # city = 'shenzhen'
    # key = '0d5246d56226a35c2ecbedca4ee5ad1d'
    # add = quote(address)
    # url2 = url+address+'&city='+city+'&output='+output+"&key="+key
    # requests.adapters.DEFAULT_RETRIES = 5
    req = requests.get(url, params)
    temp = req.json()
    # req = urlopen(url2)
    # res = req.read().decode()
    # temp = json.loads(res)
    while True:
        try:
            status = temp['status']
            if status == '1':
                if len(temp['geocodes']) > 0:
                    lat = float(temp['geocodes'][0]['location'].split(',')[1])
                    lon = float(temp['geocodes'][0]['location'].split(',')[0])
                else:
                    lat = -1
                    lon = -1
                time.sleep(1)
                break
        except requests.exceptions.ConnectionError:
            print('ConnectionError -- please wait 30 seconds')
            time.sleep(5)
        except requests.exceptions.ChunkedEncodingError:
            print('ChunkedEncodingError -- please wait 30 seconds')
            time.sleep(5)
        except:
            print('Unfortunitely -- An Unknow Error Happened, Please wait 30 seconds')
            time.sleep(5)
    return status, lat, lon

location_all = pd.read_csv('../y原始数据/夜班车数据 - 脱敏/Location_all.csv')
location_all['gcj_lat'] = -1
location_all['gcj_lon'] = -1
for i in range(0, len(location_all)):
    location = location_all.iloc[i, 0]
    status, lat, lon = getlnglat(location)
    location_all.iloc[i, 1] = lat
    location_all.iloc[i, 2] = lon
    print('No.{} complete!'.format(i))
    if i % 50 == 0:
        location_all.to_csv('../y原始数据/夜班车数据 - 脱敏/Location_all_gcj.csv')


