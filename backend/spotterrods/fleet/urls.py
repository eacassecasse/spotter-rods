from django.urls import path


from .views import CarrierList
from .views import CarrierDetail
from .views import TruckList
from .views import TruckDetail
from .views import TrailerList
from .views import TrailerDetail
from .views import DriverList
from .views import DriverDetail

urlpatterns = [
    path('', CarrierList.as_view(), name='carrier-list'),
    path('<uuid:id>/', CarrierDetail.as_view(), name='carrier-details'),
    path('<uuid:carrier_id>/drivers/', DriverList.as_view(), name='driver-list'),
    path('<uuid:carrier_id>/drivers/<uuid:id>', DriverDetail.as_view(), name='driver-details'),
    path('<uuid:carrier_id>/trucks/', TruckList.as_view(), name='truck-list'),
    path('<uuid:carrier_id>/trucks/<uuid:id>', TruckDetail.as_view(), name='truck-details'),
    path('<uuid:carrier_id>/trailers/', TrailerList.as_view(), name='trailer-list'),
    path('<uuid:carrier_id>/trailers/<uuid:id>', TrailerDetail.as_view(), name='trailer-details'),
]
