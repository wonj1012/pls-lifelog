from django.shortcuts import render
from .models import UserProfile
from django.db.models import Q
import pandas as pd

# 기본 페이지
def main(requests):
    return render(requests, 'index.html')

# user_id가 존재하는지 확인
def checkID(request):
    # user로부터 id 값 받아옴
    get_user_id = request.GET.get('userID')

    # 연결한 sql에 해당 id가 존재하는지 확인하기
    # id가 존재하면 다음 페이지로 넘어감
    
    flag = False
    df = pd.read_csv('user_profile.csv', encoding='ANSI')
    for index, row in df.iterrows():
        if str(row['user_id']) == get_user_id:
            flag = True
        
    if flag:
        return render(request, 'wait.html', {'user_id': get_user_id})
    else:
        return render(request, 'index.html', {'user_id': 'id가 없습니다'})
    