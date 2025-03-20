from django.urls import path

from .views import AdverseDrivingConditionList
from .views import AdverseDrivingConditionDetail
from .views import DutyStatusList
from .views import DutyStatusDetail
from .views import DutyRemarkList
from .views import DutyRemarkDetail
from .views import OnDutyLimitList
from .views import OnDutyLimitDetail
from .views import OtherDutyList
from .views import OtherDutyDetail
from .views import RestBreakList
from .views import RestBreakDetail
from .views import RestartList
from .views import RestartDetail
from .views import ShortHaulList
from .views import ShortHaulDetail
from .views import ShortHaulRemarkList
from .views import ShortHaulRemarkDetail
from .views import SleeperBerthList
from .views import SleeperBerthDetail

urlpatterns = [
    path('/adverse-conditions/', AdverseDrivingConditionList.as_view(),
         name='adverse-condition-exception-list'),
    path('/duty-statuses/', DutyStatusList.as_view(), name='duty-status-list'),
    path('/duty-limits/', OnDutyLimitList.as_view(), name='duty-limit-list'),
    path('/other-duties/', OtherDutyList.as_view(), name='other-duty-list'),
    path('/rest-breaks/', RestBreakList.as_view(), name='rest-break-list'),
    path('/restarts/', RestartList.as_view(), name='restart-list'),
    path('/short-hauls/', ShortHaulList.as_view(), name='short-haul-exception-list'),
    path('/sleeper-berths/', SleeperBerthList.as_view(), name='sleeper-berths-list'),
    path('/adverse-conditions/<pk:id>/', AdverseDrivingConditionDetail.as_view(),
         name='adverse-condition-exception-details'),
    path('/duty-statuses/<pk:id>/', DutyStatusDetail.as_view(), name='duty-status-details'),
    path('/duty-limits/<pk:id>/', OnDutyLimitDetail.as_view(), name='duty-limit-details'),
    path('/other-duties/<pk:id>/', OtherDutyDetail.as_view(), name='other-duty-details'),
    path('/rest-breaks/<pk:id>/', RestBreakDetail.as_view(), name='rest-break-details'),
    path('/restarts/<pk:id>/', RestartDetail.as_view(), name='restart-details'),
    path('/short-hauls/<pk:id>/', ShortHaulDetail.as_view(),
         name='short-haul-exception-details'),
    path('/sleeper-berths/<pk:id>/', SleeperBerthDetail.as_view(), name='sleeper-berth-details'),
    # TODO: Review the definitions of these routes
    path('duty-statuses/<pk:duty_status_id>/remarks/', DutyRemarkList.as_view(), name='duty-remark-list'),
    path('duty-statuses/<pk:duty_status_id>/remarks/<pk:id>/', DutyRemarkDetail.as_view(), name='duty-remark-details'),
    path('short-hauls/<pk:short_hauls_id>/remarks/', ShortHaulRemarkList.as_view(), name='short-haul-remark-list'),
    path('short-hauls/<pk:short_hauls_id>/remarks/<pk:id>/', ShortHaulRemarkDetail.as_view(),
         name='short-haul-remark-details'),
]
