#my_settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # 1. 사용할 엔진 설정
        'NAME': 'lifelog_data', # 2. 연동할 MySQL의 데이터베이스 이름
        'USER': 'root', # 3. DB 접속 계정명
        'PASSWORD': 'lifelogproject', # 4. 해당 DB 접속 계정 비밀번호
        'HOST': 'localhost', # 5. 실제 DB 주소
        'PORT': '3306', # 6. 포트번호
    }
}
SECRET_KEY = 'django-insecure-71-jr&fdno3%j6cmi%)&8wosb4xb89i#l=*x^4jbpz(i&nuc%r'