# -*- coding: utf-8 -*-
from typing import Sequence
from django.shortcuts import render
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import datetime as dt
import time

# 해당 id의 data 분석
def checkData(request):
    
    global user_id
    user_id = str(request.GET.get('getId'))
    
    activeData()
    exerciseData()
    regularData()
    sleepData()
    mealData()
    #sooniData()

    return render(request, 'chart.html', {'zList': zList, 'newList2': newList2, 'newList3': newList3, 'graph': graph, 'actGraph' : actGraph, 'sleepGraph': sleepGraph, 'sleepAvg': avg})

def activeData():
    global zList
    zList = [[0] * 12 for row in range(32)]
    df = pd.read_csv('hs_g73_m08/hs_' + user_id + '_m08_0903_1355.csv', encoding='ANSI')
    for index, row in df.iterrows():
        dateNum = int(row['Time'][9:11])
        timeNum = int(int(row['Time'][12:14]) / 2)
        if row['Z'] == '부동':
            zList[dateNum][timeNum] += 0        
        elif row['Z'] == '미동':
            zList[dateNum][timeNum] += 0.33
        elif row['Z'] == '활동':
            zList[dateNum][timeNum] += 0.66
        elif row['Z'] == '외출':
            zList[dateNum][timeNum] += 0.66
        elif row['Z'] == '매우 활동':
            zList[dateNum][timeNum] += 1
    
    global newList, newList2, newList3
    newList = []
    for row in zList:
        newList.append(row)

    newList2 = []
    for i in range(1, 32):
        a = 0
        for col in range(0, 12):
            a += zList[i][col]
        newList2.append(a)

    newList3 = [0, 0, 0, 0, 0]
    for j in range(0, 31):
        if (int)(j / 7) == 0:
            newList3[0] += newList2[j]
        elif (int)(j / 7) == 1:
            newList3[1] += newList2[j]
        elif (int)(j / 7) == 2:
            newList3[2] += newList2[j]
        elif (int)(j / 7) == 3:
            newList3[3] += newList2[j]
        else:
            newList3[4] += newList2[j]

    global graph
    labels = ['나의 활동 정도']
    x_data = np.vstack((np.arange(1, 32),)*4)
    newList22 = [newList2]
    y_data = np.array(newList22)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data[0], y=y_data[0], mode='lines', name=labels[0], connectgaps=True,))
    graph = fig.to_html(full_html=False, default_height=500, default_width=700)

def exerciseData():
    # 2. 운동 정도 분석하기
    # Act에서 '실외운동', '실내운동' 횟수 계산
    # '실외운동', '실내운동'이면 (다음 시각) - (이전 시각)으로 운동 시간 계산
    # 운동시간은 주중 몇 시간인지만 제공하기 (..복잡해..ㅠㅠ)

    global actNumWeek, actNumMonth, actGraph
    actNumWeek = [0, 0, 0, 0, 0]
    
    df = pd.read_csv('hs_g73_m08/hs_' + user_id + '_m08_0903_1355.csv', encoding='ANSI')
    for index, row in df.iterrows():
        if (row['State'] == '실외운동하기') or (row['State'] == '실내운동하기'):
            if int(row['Time'][9:11]) <= 7:
                actNumWeek[0] += 1
            elif int(row['Time'][9:11]) <= 14:
                actNumWeek[1] += 1
            elif int(row['Time'][9:11]) <= 21:
                actNumWeek[2] += 1
            elif int(row['Time'][9:11]) <= 28:
                actNumWeek[3] += 1
            elif int(row['Time'][9:11]) <= 31:
                actNumWeek[4] += 1
    
    actNumMonth = 0
    for i in range(0, 5):
        actNumMonth += actNumWeek[i]
        
    # actNumWeek : 주간 운동 횟수 list
    # actNumMonth : 월간 운동 횟수 변수
            
    fig2 = go.Figure(data=[go.Bar(
        x=[1, 2, 3, 4, 5],
        y=[actNumWeek[0], actNumWeek[1], actNumWeek[2], actNumWeek[3], actNumWeek[4]],
        width=[0.3, 0.3, 0.3, 0.3, 0.3]
    )])
    
    actGraph = fig2.to_html(full_html=False)

def regularData():
    # 3. 규칙성 분석하기   
    # z에서 '약', act에서 '용변' 검색 가능
    # 만약 '약', '용변' 횟수가 0회라면 아예 분석 x => 규칙성 점수 0점 처리
    
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

def sleepData():
    # 4. 수면시간 분석하기
    # act에서 '취침' 검색 가능
    # list에 취침 시간 넣기 (단, 시 * 60 + 분의 형태로 넣기)
    # 하루에 취침이 2번 이상일 경우 더 늦은 시간의 취침으로 넣기
    # 만약 취침이 기록되지 않은 날이면 0으로 넣기
    # list 완성 후 0이 아닌 날짜 수를 구한 후 평균 취침 시간 계산
    # 꺾은선그래프로 주간, 월간 취침 시간 그래프 그리기
    # 평균 취침 시간 보여주기
     
    # 한 달 동안 취침 시간 나타낸 list (단, 0~1440의 범위로)
    global sleepList
    sleepList = [0 for i in range(32)]
    
    df = pd.read_csv('hs_g73_m08/hs_' + user_id + '_m08_0903_1355.csv', encoding='ANSI')
    for index, row in df.iterrows():
        if row['Act'] == '취침':
            dateNum = int(row['Time'][9:11])
            sleepList[dateNum] = int(row['Time'][12:14]) * 60 + int(row['Time'][15:17])
           
    sleepNum = 0 
    for i in range(1, 32):
        if sleepList[i] != 0:
            sleepNum += 1
        
    sum = 0    
    for j in range(1, 32):
        sum += sleepList[j]
    
    # 평균 취침 시간
    global avg
    avg = sum / sleepNum
             
    # 한 달 동안 취침 시간 나타낸 list (단, 0~24의 범위로)
    global sleepListVer2
    sleepListVer2 = [0 for i in range(32)]
    for k in range(1, 32):
        sleepListVer2[k] = sleepList[k] / 60
    
    global sleepGraph
    if sum == 0:
        sleepGraph = '수면 기록이 없습니다'
    else:
        labels2 = ['나의 수면 시간']
        x_data = np.vstack((np.arange(1, 32),)*4)
        sleepListVer22 = [sleepListVer2]
        y_data = np.array(sleepListVer22)
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=x_data[0], y=y_data[0], mode='lines', name=labels2[0], connectgaps=True,))
        sleepGraph = fig3.to_html(full_html=False, default_height=500, default_width=700)

def mealData():
    # 5. 식사 시간 분석
    # state로 '조식', '중식', '석식' 검색 가능
    # 한 달짜리 list 생성하여 조식, 중식, 석식이 모두 기록되어 있지 않으면 이를 알려주기
    # 조식 시간은 오전 6시 ~ 오전 9시 (360분 ~ 540분)
    # 중식 시간은 오전 11시 ~ 오후 1시 (660분 ~ 780분)
    # 석식 시간은 오후 5시 ~ 오후 8시 (1020분 ~ 1200분)
    # 이 시간에 식사를 한 게 아니면 표시하기

    # 식사 시간 표시한 list 
    # [0, 3, 6] : 식사 시간 분 표시
    # [1, 4, 7] : 식사했는지 여부
    # [2, 5, 8] : 올바른 식사시간인지 확인
    global mealList
    mealList= [[0] * 9 for row in range(32)]
    
    df = pd.read_csv('hs_g73_m08/hs_' + user_id + '_m08_0903_1355.csv', encoding='ANSI')
    for index, row in df.iterrows():
        dateNum = int(row['Time'][9:11])
        if row['State'] == '조식':
            mealList[dateNum][0] = int(row['Time'][12:14]) * 60 + int(row['Time'][15:17])
            mealList[dateNum][1] = 1
        elif row['State'] == '중식':
            mealList[dateNum][3] = int(row['Time'][12:14]) * 60 + int(row['Time'][15:17])
            mealList[dateNum][4] = 1
        elif row['State'] == '석식':
            mealList[dateNum][6] = int(row['Time'][12:14]) * 60 + int(row['Time'][15:17])
            mealList[dateNum][7] = 1
            
    for i in range(1, 32):
        if mealList[i][1] == 1:
            if mealList[i][0] < 360:
                mealList[i][2] = -1
            elif mealList[i][0] > 540:
                mealList[i][2] = 1
        if mealList[i][4] == 1:
            if mealList[i][3] < 660:
                mealList[i][5] = -1
            elif mealList[i][3] > 780:
                mealList[i][5] = 1
        if mealList[i][7] == 1:
            if mealList[i][6] < 1020:
                mealList[i][8] = -1
            elif mealList[i][6] > 1200:
                mealList[i][8] = 1

def sooniData():
    # 6. 순이 분석
    # 한 달 동안 대화 횟수 기록하기 (막대 그래프로 나타내기)
    # 대화 text를 하나의 string으로 합치고 이를 wordcloud 라이브러리로 표시하기

    # 한 달 간 순이 대화 횟수 list
    sooniList = [0 for i in range(32)]
    text = ''
    df = pd.read_csv('hs_g73_m08/hs_' + user_id + '_m08_0903_1355.csv', encoding='ANSI')
    for index, row in df.iterrows():
        if row['Message_1'] != "" or row['Message_2'] != "" or row['Message_3'] != "":
            dateNum = int(row['Time'][9:11])
        sooniList[dateNum] += 1
        text =  text + ' ' + row['Message_1']

def details(request):
    
    return render(request, 'details.html', {'zList': zList, 'newList2': newList2, 'newList3': newList3, 'graph': graph, 'actGraph' : actGraph, 'sleepGraph': sleepGraph, 'sleepAvg': avg, 'mealList': mealList})