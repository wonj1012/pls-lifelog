from django.shortcuts import render
from .models import UserProfile
from .models import Hs228M0809031355
from django.db.models import Q

# 기본 페이지
def main(requests):
    return render(requests, 'index.html')

# user_id가 존재하는지 확인
def checkID(request):
    # user로부터 id 값 받아옴
    get_user_id = request.GET.get('userID')

    # 연결한 sql에 해당 id가 존재하는지 확인하기
    # id가 존재하면 다음 페이지로 넘어감
    if UserProfile.objects.filter(user_id=int(get_user_id)).exists():
        return render(request, 'wait.html', {'user_id': get_user_id})
    # id가 존재하지 않으면 다시 입력해야함
    else:
        return render(request, 'index.html', {'user_id': 'id가 없습니다'})
    