from django.urls import path
from startData import views as v1
from chartData import views as v2
from . import views

urlpatterns = [
    path('checkData', v2.checkData),
    path('details', v2.details)
]
