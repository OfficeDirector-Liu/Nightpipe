# -*- coding:utf-8 -*-
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import scipy.cluster.hierarchy as sch
import numpy as np


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    #
    # lon1 = x[0]
    # lat1 = x[1]
    # lon2 = x[2]
    # lat2 = x[3]
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])


    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r * 1000


print('Loading data ...')
data = pd.read_csv('../y原始数据/夜班车数据 - 脱敏/demand_spatial.csv')

print('Reserved demand sensing ...')
re_data = data[(data['申请时间'] > '2019/11/5 21:30') & (data['申请时间'] < '2019/11/5 21:35')]
re_data.sort_values(by='申请时间', inplace=True)

print('Distance calculating ...')
location_list = re_data[['上车地点_lat', '上车地点_lon', '下车地点_lat', '下车地点_lon']].reset_index(drop=True)
distance_list = np.zeros([1, int(len(location_list)*(len(location_list)-1)/2)])
count = 0
for i in range(0, len(location_list)-1):
    up_lat_1 = location_list.iloc[i, 0]
    up_lon_1 = location_list.iloc[i, 1]
    down_lat_1 = location_list.iloc[i, 2]
    down_lon_1 = location_list.iloc[i, 3]
    for j in range(i+1, len(location_list)):
        up_lat_2 = location_list.iloc[j, 0]
        up_lon_2 = location_list.iloc[j, 1]
        down_lat_2 = location_list.iloc[j, 2]
        down_lon_2 = location_list.iloc[j, 3]
        distance_up = haversine(up_lon_1, up_lat_1, up_lon_2, up_lat_2)
        distance_down = haversine(down_lon_1, down_lat_1, down_lon_2, down_lat_2)
        distance_list[0, count] = distance_up + distance_down
        count += 1
distance_list = np.squeeze(distance_list)

print('Clustering ...')
Z = sch.linkage(distance_list, method='average')
label_ = sch.fcluster(Z, t=3000, criterion='distance').tolist()

print('Appending cluster result ...')
re_data['re_label'] = label_

# Test
a = re_data.sort_values(by='re_label')[['re_label', '上车地点', '上车地点_lat', '上车地点_lon', '下车地点', '下车地点_lat', '下车地点_lon']]
