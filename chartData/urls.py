from django.urls import path
from startData import views as v1
from chartData import views as v2
from . import views

urlpatterns = [
    path('checkData', v2.checkData),
    path('details1', v2.details1),
    path('details2', v2.details2),
    path('details3', v2.details3),
    path('details4', v2.details4),
    path('details5', v2.details5),
    path('details6', v2.details6)
]
