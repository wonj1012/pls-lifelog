import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import datetime as dt
import time

user_id = '315'
# csv 파일 dataframe 객체로 읽어오기
df = pd.read_csv('hs_g73_m08/hs_' + user_id + '_m08_0903_1355.csv', encoding='ANSI')
toilet_times = []
toilet_times_sec = []

# 용변 시간 리스트에 저장
for index, row in df.iterrows():
    if ('용변' in row['Act']):
        ttime = dt.datetime.strptime(row['Time'], '\'%Y-%m-%d %H:%M:%S')
        if (ttime not in toilet_times):
            toilet_times.append(ttime)
            toilet_times_sec.append(time.mktime(ttime.timetuple()))
    end_index = index

# 기록된 첫 시간, 마지막 시간
start_time = dt.datetime.strptime(df['Time'][0], '\'%Y-%m-%d %H:%M:%S')
end_time = dt.datetime.strptime(df['Time'][end_index], '\'%Y-%m-%d %H:%M:%S')
# 일 평균 용변 횟수
average_toilet_time = len(toilet_times) / (end_time.date() - start_time.date()).days
# print(round(average_toilet_time, 4))
# 용변 표준편차
std_toilet_time = np.std(toilet_times_sec)
# print(std_toilet_time)

# # index: 용변 시간 column: 용변 횟수 dataframe 형성
# temp = start_time.date()
# times_list = []
# while (temp != end_time.date()):
#     times_list.append(temp)
#     temp += dt.timedelta(days=1)
# times_list.append(temp)
# toilet_times_df = pd.DataFrame({'times': 0}, index=times_list)
# for t in toilet_times:
#     toilet_times_df['times'][t.date()] += 1
# print(toilet_times_df)
# {용변 시간: 용변 횟수} dictionary 생성
toilet_times_dict = {}
temp = start_time.date()
while (temp != end_time.date()):
    toilet_times_dict[temp] = 0
    temp += dt.timedelta(days=1)
toilet_times_dict[temp] = 0
for t in toilet_times:
    toilet_times_dict[t.date()] += 1

toilet_data = go.Scatter(x=list(toilet_times_dict.keys()), y=list(toilet_times_dict.values()))
toilet_fig = go.Figure()
toilet_fig.add_trace(toilet_data)

# 새벽 용변 횟수
dusk_toilet_times = []
for t in toilet_times:
    if (dt.time(0, 0, 0) <= t.time() <= dt.time(6, 0, 0)):
        dusk_toilet_times.append(t)
print(dusk_toilet_times)