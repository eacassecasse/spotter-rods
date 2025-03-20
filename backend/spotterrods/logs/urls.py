from django.urls import path

from .views import DailyLogList
from .views import DailyLogDetail

urlpatterns = [
    path('/daily-logs/', DailyLogList.as_view(), name='daily-log-list'),
    path('/daily-logs/<pk:id>', DailyLogDetail.as_view(), name='daily-detail'),
]
