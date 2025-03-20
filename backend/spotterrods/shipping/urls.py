from django.urls import path

from .views import ShippingList
from .views import ShippingDetail

urlpatterns = [
    path('carriers/<pk:carrier_id>/shippings/', ShippingList.as_view(), name='carrier-shippings'),
    path('carriers/<pk:carrier_id>/shippings/<pk:id>', ShippingDetail.as_view(), name='shipping-details'),
]
