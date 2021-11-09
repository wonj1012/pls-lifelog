import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import datetime as dt
import time

# user_id = '315'
# csv 파일 dataframe 객체로 읽어오기
try:
    df = pd.read_csv('hs_g73_m08/hs_' + u_id + '_m08_0903_1355.csv', encoding='ANSI')
except FileNotFoundError:
    df = pd.read_csv('hs_g73_m08/hs_' + u_id + '_m08_0903_1356.csv', encoding='ANSI')
toilet_times = []
toilet_times_sec = []
toilet_times_time_sec = []

# 용변 시간 리스트에 저장
for index, row in df.iterrows():
    if ('용변' in row['Act']):
        ttime = dt.datetime.strptime(row['Time'], '\'%Y-%m-%d %H:%M:%S')
        if (ttime not in toilet_times):
            toilet_times.append(ttime)
            toilet_times_sec.append(time.mktime(ttime.timetuple()))
            toilet_times_time_sec.append(ttime.time().hour * 3600 + ttime.time().minute * 60 + ttime.time().second)
    end_index = index

# 데이터 시작 시간, 끝 시간
start_time = dt.datetime.strptime(df['Time'][0], '\'%Y-%m-%d %H:%M:%S')
end_time = dt.datetime.strptime(df['Time'][end_index], '\'%Y-%m-%d %H:%M:%S')

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

# 시간대별 용변 
# toilet_timezone[0], [1], [2], [3] = 0~6시, 6~12시, 12시~18시, 18시~24시
toilet_timezone = [0, 0, 0, 0] 
for t in toilet_times:
    # 새벽
    if (dt.time(0, 0, 0) <= t.time() < dt.time(6, 0, 0)):
        toilet_timezone[0] += 1
    # 아침
    elif (dt.time(6, 0, 0) <= t.time() < dt.time(12, 0, 0)):
        toilet_timezone[1] += 1
    # 점심
    elif (dt.time(12, 0, 0) <= t.time() < dt.time(18, 0, 0)):
        toilet_timezone[2] += 1
    # 저녁
    else:
        toilet_timezone[3] += 1
toilet_timezone_data = go.Scatter(x=['새벽 (0시 ~ 6시)', '아침 (6시 ~ 12시)', '점심 (12시 ~ 18시)', '저녁 (18시 ~ 24시)'], y=toilet_timezone)
toilet_timezone_fig = go.Figure()
toilet_timezone_fig.add_trace(toilet_timezone_data)

# 일 평균 용변 횟수
average_toilet_time = len(toilet_times) / (end_time.date() - start_time.date()).days
# print(round(average_toilet_time, 4))
# 용변시간 표준편차
std_toilet_time = np.std(toilet_times_sec)
# 일중 용변시간 표준편차
std_toilet_time_inday = np.std(toilet_times_time_sec)
print(std_toilet_time, std_toilet_time_inday)
