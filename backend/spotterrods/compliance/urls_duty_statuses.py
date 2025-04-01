from django.urls import path
from .views import DutyRemarkList
from .views import DutyRemarkDetail

urlpatterns = [
    path('remarks/', DutyRemarkList.as_view(), name='duty-remark-list'),
    path('remarks/<uuid:id>/', DutyRemarkDetail.as_view(), name='duty-remark-details'),
]
