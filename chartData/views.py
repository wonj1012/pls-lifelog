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
from wordcloud import WordCloud
from konlpy.tag import Twitter
from collections import Counter

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
    
    fullScore = round(getScore(1,1,1,1,1,0.1), 2)
    print(fullArr)

    return render(request, 'chart.html', {'user_id': user_id, 'fullScore': fullScore, 'fullArr': fullArr})

def activeData():
    global zList
    zList = [[0] * 12 for row in range(32)]
    try:
        df = pd.read_csv('hs_g73_m08/hs_' + user_id + '_m08_0903_1355.csv', encoding='ANSI')
    except FileNotFoundError:
        df = pd.read_csv('hs_g73_m08/hs_' + user_id + '_m08_0903_1356.csv', encoding='ANSI')
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
    fig.add_trace(go.Scatter(x=x_data[0], y=y_data[0], mode='lines', line_shape='spline', name=labels[0], connectgaps=True,))
    graph = fig.to_html(full_html=False, default_height=500, default_width=700)
    
    global graph2
    x_data2 = np.vstack((np.arange(1, 5),)*4)
    newList33 = [newList3]
    y_data2 = np.array(newList33)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=x_data2[0], y=y_data2[0], mode='lines', line_shape='spline', connectgaps=True,))
    graph2 = fig2.to_html(full_html=False, default_height=500, default_width=700)

def exerciseData():
    # 2. 운동 정도 분석하기
    # Act에서 '실외운동', '실내운동' 횟수 계산
    # '실외운동', '실내운동'이면 (다음 시각) - (이전 시각)으로 운동 시간 계산
    # 운동시간은 주중 몇 시간인지만 제공하기 (..복잡해..ㅠㅠ)

    global actNumWeek, actNumMonth, actGraph
    actNumWeek = [0, 0, 0, 0, 0]
    
    try:
        df = pd.read_csv('hs_g73_m08/hs_' + user_id + '_m08_0903_1355.csv', encoding='ANSI')
    except FileNotFoundError:
        df = pd.read_csv('hs_g73_m08/hs_' + user_id + '_m08_0903_1356.csv', encoding='ANSI')
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
    try:
        df = pd.read_csv('hs_g73_m08/hs_' + user_id + '_m08_0903_1355.csv', encoding='ANSI')
    except FileNotFoundError:
        df = pd.read_csv('hs_g73_m08/hs_' + user_id + '_m08_0903_1356.csv', encoding='ANSI')
    toilet_times = []

    # 용변 시간 리스트에 저장
    for index, row in df.iterrows():
        if ('용변' in row['Act']):
            try:
                ttime = dt.datetime.strptime(row['Time'], '\'%Y-%m-%d %H:%M:%S')
            except IndexError:
                break
            if (ttime not in toilet_times):
                toilet_times.append(ttime)
        end_index = index

    # 데이터 시작 시간, 끝 시간
    try:
        start_time = dt.datetime.strptime(df['Time'][0], '\'%Y-%m-%d %H:%M:%S')
        end_time = dt.datetime.strptime(df['Time'][end_index], '\'%Y-%m-%d %H:%M:%S')
    except IndexError:
        return -1

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
    toilet_fig.to_html(full_html=False, default_height=500, default_width=700)

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
    toilet_timezone_fig.to_html(full_html=False, default_height=500, default_width=700)

    # 일 평균 용변 횟수
    try:
        average_toilet_time = len(toilet_times) / (end_time.date() - start_time.date()).days
    except ZeroDivisionError:
        average_toilet_time = 0
    
    # 표준편차 등수 확인
    rank_df = pd.read_csv('toilet_rank.csv', index_col=0)
    for index, row in rank_df.iterrows():
        if(index == int(user_id)):
            score = (row['rank']) # 점수
            rank_found = True
            break
    if (not rank_found):
        score = 0 # No data

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
    
    try:
        df = pd.read_csv('hs_g73_m08/hs_' + user_id + '_m08_0903_1355.csv', encoding='ANSI')
    except FileNotFoundError:
        df = pd.read_csv('hs_g73_m08/hs_' + user_id + '_m08_0903_1356.csv', encoding='ANSI')
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
        
        for i in range(0, 32):
            if sleepListVer2[i] == 0:
                sleepListVer2[i] = None
        
        sleepListVer22 = [sleepListVer2]
        y_data = np.array(sleepListVer22)
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=x_data[0], y=y_data[0], mode='lines', line_shape='spline', name=labels2[0], connectgaps=True,))
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
    
    try:
        df = pd.read_csv('hs_g73_m08/hs_' + user_id + '_m08_0903_1355.csv', encoding='ANSI')
    except FileNotFoundError:
        df = pd.read_csv('hs_g73_m08/hs_' + user_id + '_m08_0903_1356.csv', encoding='ANSI')
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
                
    # 만약 식사 횟수가 30회 중 10회 이하이면 기록 오류
    # 오류 확인한 뒤 식사 안한 때는 None으로 표시한 후 조식, 중식, 석식 그래프 생성하기
    notBreakfast = 0
    breakfastFlag = True
    notLunch = 0
    lunchFlag = True
    notDinner = 0
    dinnerFlag = True
    for j in range(1, 32):
        if mealList[j][1] == 0:
            notBreakfast += 1
        if mealList[j][4] == 0:
            notLunch += 1
        if mealList[j][7] == 0:
            notDinner += 1
            
    if notBreakfast >= 20:
        breakfastFlag = False
    if notLunch >= 20:
        lunchFlag = False
    if notDinner >= 20:
        dinnerFlag = False
        
    mealText = ''
    if breakfastFlag == False or lunchFlag == False or dinnerFlag == False:
        mealText = '정보가 부족하여 분석이 불가합니다'

    global mealGraph
    x_data = np.vstack((np.arange(1, 32),)*4)
    
    mealBreakfast = [0 for i in range(32)]
    mealLunch = [0 for i in range(32)]
    mealDinner = [0 for i in range(32)]
    for i in range(0, 32):
        if mealList[i][1] == 0:
            mealBreakfast[i] = None
        else:
            mealBreakfast[i] = mealList[i][0] / 60  
    
        if mealList[i][4] == 0:
            mealLunch[i] = None
        else:
            mealLunch[i] = mealList[i][3] / 60    
            
        if mealList[i][7] == 0:
            mealDinner[i] = None
        else:
            mealDinner[i] = mealList[i][6] / 60    
    
    mealBreakfast2 = [mealBreakfast]
    mealLunch2 = [mealLunch]
    mealDinner2 = [mealDinner]
    y_data1 = np.array(mealBreakfast2)
    y_data2 = np.array(mealLunch2)
    y_data3 = np.array(mealDinner2)
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=x_data[0], y=y_data1[0], mode='lines', line_shape='spline', name='breakfast', connectgaps=True,))
    fig4.add_trace(go.Scatter(x=x_data[0], y=y_data2[0], mode='lines', line_shape='spline', name='lunch', connectgaps=True,))
    fig4.add_trace(go.Scatter(x=x_data[0], y=y_data3[0], mode='lines', line_shape='spline', name='dinner', connectgaps=True,))
    mealGraph = fig4.to_html(full_html=False, default_height=500, default_width=700)
    
def sooniData():
    # 6. 순이 분석
    # 한 달 동안 대화 횟수 기록하기 (막대 그래프로 나타내기)
    # 대화 text를 하나의 string으로 합치고 이를 wordcloud 라이브러리로 표시하기

    # 한 달 간 순이 대화 횟수 list
    sooniList = [0 for i in range(32)]
    text = ''
    try:
        df = pd.read_csv('hs_g73_m08/hs_' + user_id + '_m08_0903_1355.csv', encoding='ANSI')
    except FileNotFoundError:
        df = pd.read_csv('hs_g73_m08/hs_' + user_id + '_m08_0903_1356.csv', encoding='ANSI')
    for index, row in df.iterrows():
        mg1 = row['Message_1']
        mg2 = row['Message_2']
        mg3 = row['Message_3']
        if pd.isna(mg1) == False:
            dateNum = int(row['Time'][9:11])
            sooniList[dateNum] += 1
            text += mg1
        if pd.isna(mg2) == False:
            dateNum = int(row['Time'][9:11])
            sooniList[dateNum] += 1
            text += mg2
        if pd.isna(mg3) == False:
            dateNum = int(row['Time'][9:11])
            sooniList[dateNum] += 1
            text += mg3
            
    twitter = Twitter()
    sentences_tag = []
    sentences_tag = twitter.pos(text)
    
    noun_adj_list = []
    
    for word, tag in sentences_tag:
        if tag in ['Noun', 'Adjective']:
            noun_adj_list.append(word)
    
    counts = Counter(noun_adj_list)
    tags = counts.most_common(40)
    
    wc = WordCloud(font_path='malgun.ttf', background_color="white", max_font_size=60)
    cloud = wc.generate_from_frequencies(dict(tags))
    cloud.to_file('test.jpg')
  
def getScore(w_active=1,w_exercise=1,w_regular=1,w_sleep=1,w_meal=1,w_sooni=0.1):
    
    try:
        df = pd.read_csv('hs_g73_m08/hs_' + user_id + '_m08_0903_1355.csv', encoding='ANSI')
    except FileNotFoundError:
        df = pd.read_csv('hs_g73_m08/hs_' + user_id + '_m08_0903_1356.csv', encoding='ANSI')
    
    # 각 점수는 최대 100점. 가중치를 곱해서 총점을 가중평균
    def getScoreAct():
        total_act_num = 0
        active_score=0
        for index, row in df.iterrows():

            total_act_num+=1

            if row['Z'] == '부동':
                active_score+=0
            elif row['Z'] == '미동':
                active_score += 0.33
            elif row['Z'] == '활동':
                active_score += 0.66
            elif row['Z'] == '외출':
                active_score += 0.66
            elif row['Z'] == '매우 활동':
                active_score += 1

        ## 주 5일 이상 활동/외출 정도면 만점처리. 기본점수 있음
        if (total_act_num!=0):
            active_score/=(total_act_num*0.66)

        return 50*(1+np.min([active_score,1]))

    def getScoreEx(): 
        
        ## 운동횟수 합산
        act_num=0
        for index, row in df.iterrows():
            if (row['State'] == '실외운동하기') or (row['State'] == '실내운동하기'):
                act_num+=1
        
        #주 5일 이상 운동시 만점처리. 기본점수 있음.
        act_num=1.4*act_num/31

        return 50*(1+np.min([act_num,1]))

    def getScoreReg():
        return 100
    def getScoreSlp():

        sleepList_score = [0 for i in range(32)]
        
        for index, row in df.iterrows():
            if row['Act'] == '취침':
                dateNum = int(row['Time'][9:11])
                defaulttime=0
                if int(row['Time'][12:14])<=8: ## 오전 8시 59분 59초 까지 잔 것은 전날 잔 것처럼 처리
                    dateNum -= 1
                    defaulttime=24
                sleepList_score[dateNum] = (int(row['Time'][12:14])+defaulttime) * 60 + int(row['Time'][15:17])   

        new_sleeplist = []
        for item in sleepList_score:
            if item!=0:
                new_sleeplist.append(item)

        if len(new_sleeplist)<10: # 수면 횟수 10회 이하는 분석 제외
            return 50
        
        mystd = np.std(new_sleeplist)
        #표준편차가 30분 이내이면 만점 처리.
        if mystd==0:
            mystd=1

        return 50*(1+np.min([1,30/mystd]))

    def getScoreMeal():
        mealList_score=[[0]*3 for _ in range(32)]
        for index, row in df.iterrows():
            dateNum = int(row['Time'][9:11])
            if row['State'] == '조식':
                mealList_score[dateNum][0] = int(row['Time'][12:14]) * 60 + int(row['Time'][15:17])
            elif row['State'] == '중식':
                mealList_score[dateNum][1] = int(row['Time'][12:14]) * 60 + int(row['Time'][15:17])    
            elif row['State'] == '석식':
                mealList_score[dateNum][2] = int(row['Time'][12:14]) * 60 + int(row['Time'][15:17])

        # 2회 이상 식사했는지 (50%) + 정해진 시간에 식사했는지 (50%)

        goodMealTimeNum=0
        morethan2Meals=0

        for i in range(1,32):
            dayMealNum=0
            i0=mealList_score[i][0]
            i1=mealList_score[i][1]
            i2=mealList_score[i][2]
            if i0!=0:
                dayMealNum+=1
                if (360<i0<540):
                    goodMealTimeNum+=1
            if i1!=0:
                dayMealNum+=1
                if (660<i0<780):
                    goodMealTimeNum+=1
            if i2!=0:
                dayMealNum+=1
                if (1020<i0<1200):
                    goodMealTimeNum+=1
            if dayMealNum>=2:
                morethan2Meals+=1
                
        return 50*(morethan2Meals/31)+50*(goodMealTimeNum/(31*3))
            

    def getScoreSooni():
        sooniTalkNum=0
        for index, row in df.iterrows():
            if row['Message_1'] != "" or row['Message_2'] != "" or row['Message_3'] != "":
                sooniTalkNum+=1
        # 10회 이상 대화시 만점
        return 50*(1+np.min([1,sooniTalkNum/10]))

    w_sum = w_active+w_exercise+w_regular+w_sleep+w_meal+w_sooni
    score = w_active*getScoreAct()+w_exercise*getScoreEx()+w_regular*getScoreReg()
    score += w_sleep*getScoreSlp()+w_meal*getScoreMeal()+w_sooni*getScoreSooni()
    score /= w_sum
    
    global fullArr
    fullArr = []
    fullArr.append(round(w_active*getScoreAct()/w_sum, 2))
    fullArr.append(round(w_exercise*getScoreEx()/w_sum, 2))
    fullArr.append(round(w_regular*getScoreReg()/w_sum, 2))
    fullArr.append(round(w_sleep*getScoreSlp()/w_sum, 2))
    fullArr.append(round(w_meal*getScoreMeal()/w_sum, 2))
    fullArr.append(round(w_sooni*getScoreSooni()/w_sum, 2))
    
    arrRound = np.round([score])
    
    return arrRound[0]; # 정수로 점수로 제한.   

def details1(request):
    return render(request, 'details1.html', {'graph': graph, 'graph2': graph2})

def details2(request):
    return render(request, 'details2.html', {'actGraph' : actGraph})

def details3(request):
    return render(request, 'details3.html', {'actGraph' : actGraph})

def details4(request):
    return render(request, 'details4.html', {'sleepGraph' : sleepGraph})

def details5(request):
    return render(request, 'details5.html', {'mealGraph' : mealGraph})

def details6(request):
    return render(request, 'details6.html', {'mealGraph' : mealGraph})
