import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import datetime as dt
import time

# 전체 이용자 분석
profile_df = pd.read_excel('user_profile.xlsx')
t_time_std_list = []
t_time_std_inday_list = []
for index, row in profile_df.iterrows():
    u_id = str(row['id'])
    try:
        df = pd.read_csv('hs_g73_m08/hs_' + u_id + '_m08_0903_1355.csv', encoding='ANSI')
    except FileNotFoundError:
        df = pd.read_csv('hs_g73_m08/hs_' + u_id + '_m08_0903_1356.csv', encoding='ANSI')
    t_times = [] # 용변 시간 리스트
    t_times_sec = [] # 용변 시간 초로 변환한 리스트
    t_times_time_sec = [] # 용변 시간 날짜 제외하고 초로 변환한 리스트
    print(u_id)
    for index, row in df.iterrows():
        if ('용변' in row['Act']):
            try:
                ttime = dt.datetime.strptime(row['Time'], '\'%Y-%m-%d %H:%M:%S')
            except IndexError:
                break
            if (ttime not in t_times):
                t_times.append(ttime)
                t_times_sec.append(time.mktime(ttime.timetuple()))
                t_times_time_sec.append(ttime.time().hour * 3600 + ttime.time().minute * 60 + ttime.time().second)
        end_index = index

    try:
        # 데이터 시작 시간, 끝 시간
        start_time = dt.datetime.strptime(df['Time'][0], '\'%Y-%m-%d %H:%M:%S')
        end_time = dt.datetime.strptime(df['Time'][end_index], '\'%Y-%m-%d %H:%M:%S')
        # 일 평균 용변 횟수
        average_t_time = len(t_times) / (end_time.date() - start_time.date()).days
        # print(round(average_toilet_time, 4))
        # 용변시간 표준편차
        t_time_std = np.std(t_times_sec)
        # 일중 용변시간 표준편차
        t_time_inday_std = np.std(t_times_time_sec)
        print(t_time_std, t_time_inday_std)
        if (not np.isnan(t_time_std) and not np.isnan(t_time_inday_std)):
            t_time_std_list.append(t_time_std)
            t_time_std_inday_list.append(t_time_inday_std)
    except IndexError:
        continue
    except ZeroDivisionError:
        continue
    