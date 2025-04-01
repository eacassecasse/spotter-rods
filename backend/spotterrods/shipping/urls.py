from django.urls import path

from .views import ShippingList
from .views import ShippingDetail

urlpatterns = [
    path('', ShippingList.as_view(), name='carrier-shippings'),
    path('<uuid:id>', ShippingDetail.as_view(), name='shipping-details'),
]
