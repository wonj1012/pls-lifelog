# -*- coding: utf-8 -*-
from typing import Sequence
from django.shortcuts import render
from startData.models import Hs228M0809031355
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

# 해당 id의 data 분석
def checkData(request):
    #===========================================================
    #===========================================================
    # 1. 활동 정도 분석하기
    # Time에서 날짜, 시간 확인하여 Z 상태 나누기 (2차원 list로 구현하기) => 일간 활동 정보 생성
    # list[1][0] = 1일 0시~2시
    # list[12][3] = 12일 6시~8시
    # Time에서 시간 확인 한 뒤, 시간 / 2 값
    zList = [[0] * 12 for row in range(32)]

    for hs228 in Hs228M0809031355.objects.all():
        dateNum = int(hs228.time[9:11])
        # print(dateNum)
        timeNum = int(int(hs228.time[12:14]) / 2)
        if hs228.z == '부동':
            zList[dateNum][timeNum] += 0
        elif hs228.z == '미동':
            zList[dateNum][timeNum] += 0.33
        elif hs228.z == '활동':
            zList[dateNum][timeNum] += 0.66
        elif hs228.z == '외출':
            zList[dateNum][timeNum] += 0.66
        elif hs228.z == '매우 활동':
            zList[dateNum][timeNum] += 1

    # 생성된 list를 7일치씩 더하기 => 주간 활동 정보 생성
    # 생성된 list를 전부 다 더하기 => 월간 활동 정보 생성

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

    labels = ['나의 활동 정도']
    x_data = np.vstack((np.arange(1, 32),)*4)
    newList22 = [newList2]
    y_data = np.array(newList22)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data[0], y=y_data[0], mode='lines', name=labels[0], connectgaps=True,))
    graph = fig.to_html(full_html=False, default_height=500, default_width=700)

    #===========================================================
    #===========================================================
    # 2. 운동 정도 분석하기
    # Act에서 '실외운동', '실내운동' 횟수 계산
    # '실외운동', '실내운동'이면 (다음 시각) - (이전 시각)으로 운동 시간 계산
    # 운동시간은 주중 몇 시간인지만 제공하기 (..복잡해..ㅠㅠ)

    actNumWeek = [0, 0, 0, 0, 0]
    for hs228 in Hs228M0809031355.objects.all():
        if (hs228.state == '실외운동하기') or (hs228.state == '실내운동하기'):
            if int(hs228.time[9:11]) <= 7:
                actNumWeek[0] += 1
            elif int(hs228.time[9:11]) <= 14:
                actNumWeek[1] += 1
            elif int(hs228.time[9:11]) <= 21:
                actNumWeek[2] += 1
            elif int(hs228.time[9:11]) <= 28:
                actNumWeek[3] += 1
            elif int(hs228.time[9:11]) <= 31:
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

    #===========================================================
    #===========================================================
    # 3. 규칙성 분석하기   
    # z에서 '약', act에서 '용변' 검색 가능
    # 만약 '약', '용변' 횟수가 0회라면 아예 분석 x => 규칙성 점수 0점 처리
     

    return render(request, 'chart.html', {'zList': zList, 'newList2': newList2, 'newList3': newList3, 'graph': graph, 'actGraph' : actGraph})