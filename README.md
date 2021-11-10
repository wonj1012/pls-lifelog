# pls-lifelog: 2021-2 프로그래밍언어구조론 프로젝트
## 프로그램 소개
주어진 데이터를 이용해 6가지 영역으로 나누어 분석 후 점수를 매긴 뒤, 여섯 영역의 점수 총합이 100점이 되도록 구성하여 한 달 동안 어떤 생활을 했는지 확인할 수 있습니다. 

## 사용방법
### 1. 가상환경 생성
conda create -n pjLifelog python=3.8

### 2. 가상환경 활성화 및 라이브러리 설치
conda activate pjLifelog
pip install -r requirements.txt

### 3. 프로그램 실행
conda activate pjLifelog
python manage.py runserver

## 프로그램 구조
아나콘다를 이용하여 장고로 개발하였습니다.  
가장 상위 폴더는 startData, chartData, lifelogProject, hs_g93_m08 폴더와, manage.py, user_profile.csv로 이루어져 있습니다.  
lifelogProject 폴더는 기본적인 장고 세팅, urls.py 등으로 이루어져 있습니다.  
중간 보고서의 구성도와 마찬가지로 startData 앱과 chartData 앱으로 구성되어 있습니다.  
주어진 데이터는 가장 상위 폴더에 user_profile.csv, 그리고 hs_g93_m08 폴더에 이용자들의 엑셀 파일들을 넣어뒀습니다.  
startData는 시작 페이지를 보여주는 index.html, 점수를 볼 수 있는 버튼이 있는 wait.html, user_id가 존재하는지 확인하는 views.py 등으로 구성되어 있습니다.  
chartData는 생활 점수 총합을 보여주는 chart.html, 각 영역마다 자세한 분석 내용을 보여주는 details.html(1~6), 각 영역마다 데이터를 분석하고 점수를 매기는 views.py로 구성되어 있습니다.  
