# -*- coding:utf-8 -*-
import pandas as pd

data = pd.read_csv('../y原始数据/夜班车数据 - 脱敏/demand.csv', low_memory=False)
# lat&lon insert
location = pd.read_csv('../y原始数据/夜班车数据 - 脱敏/Location_gcj_api.csv')
result = pd.merge(data, location, left_on='上车地点', right_on='地点', how='left')
del result['地点']
result.rename(columns={'gcj_lat': '上车地点_lat',
                       'gcj_lon': '上车地点_lon'}, inplace=True)
result = pd.merge(result, location, left_on='下车地点', right_on='地点', how='left')
del result['地点']
result.rename(columns={'gcj_lat': '下车地点_lat',
                       'gcj_lon': '下车地点_lon'}, inplace=True)

result.to_csv('../y原始数据/夜班车数据 - 脱敏/demand_spatial.csv', index=False)
