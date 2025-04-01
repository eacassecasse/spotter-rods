from django.urls import path

from .views import ShortHaulRemarkList
from .views import ShortHaulRemarkDetail

urlpatterns = [
    path('remarks/', ShortHaulRemarkList.as_view(), name='short-haul-remark-list'),
    path('remarks/<uuid:id>/', ShortHaulRemarkDetail.as_view(),
         name='short-haul-remark-details'),
]
