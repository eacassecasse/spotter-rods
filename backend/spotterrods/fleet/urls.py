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
    path('carriers/', CarrierList.as_view(), name='carrier-list'),
    path('carriers/<pk:id>/', CarrierDetail.as_view(), name='carrier-details'),
    path('carriers/<pk:carrier_id>/drivers/', DriverList.as_view(), name='driver-list'),
    path('carriers/<pk:carrier_id>/drivers/<pk:id>', DriverDetail.as_view(), name='driver-details'),
    path('carriers/<pk:carrier_id>/trucks/', TruckList.as_view(), name='truck-list'),
    path('carriers/<pk:carrier_id>/trucks/<pk:id>', TruckDetail.as_view(), name='truck-details'),
    path('carriers/<pk:carrier_id>/trailers/', TrailerList.as_view(), name='trailer-list'),
    path('carriers/<pk:carrier_id>/trailers/<pk:id>', TrailerDetail.as_view(), name='trailer-details'),
]
