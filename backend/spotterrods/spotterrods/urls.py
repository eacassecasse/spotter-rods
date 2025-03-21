"""
URL configuration for spotterrods project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('api/v1/carriers/', include('fleet.urls')),
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/drivers/<uuid:driver_id>/', include('logs.urls')),
    path('api/v1/carriers/<uuid:carrier_id>/', include('shipping.urls')),
    path('api/v1/drivers/<uuid:driver_id>/', include('compliance.urls')),
    path("admin/", admin.site.urls),
]
