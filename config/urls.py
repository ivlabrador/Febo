"""Febo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core.login.views import LoginFormView
from config import settings


urlpatterns = [
    path('', LoginFormView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('login/', include('core.login.urls')),
    path('user/', include('core.user.urls')),
    path('company/', include('core.company.urls')),
    path('product/', include('core.product.urls')),
    path('client/', include('core.client.urls')),
    path('provider/', include('core.provider.urls')),
    path('stock/', include('core.stock.urls')),
    path('sales/', include('core.sales.urls')),
    path('api/', include('core.api.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)