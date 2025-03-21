from django.urls import path

from .views import ShippingList
from .views import ShippingDetail

urlpatterns = [
    path('carriers/<uuid:carrier_id>/shippings/', ShippingList.as_view(), name='carrier-shippings'),
    path('carriers/<uuid:carrier_id>/shippings/<uuid:id>', ShippingDetail.as_view(), name='shipping-details'),
]
