"""g621 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path
from gameshop.views import *
from django.contrib.auth import views as auth_views
from gameshop import views

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^$', home, name="home"),
    url(r'^about/$', about),
    url(r'^register/$', register),
    url(r'^login/$', auth_views.login, {'template_name': 'gameshop/authentication/login.html'}),
    url(r'^logout/$',logout_page),
    url(r'^shop/$', shop),
    path('gamescreen/<int:game_id>/save/', machine_save),
    path('gamescreen/<int:game_id>/load/', machine_load),
    path('gamescreen/<int:game_id>/score/', machine_score),
    path('gamescreen/<int:game_id>/', views.gamescreen),
    url(r'^inventory/dev/$', dev_inventory),
    url(r'^inventory/user/$', user_inventory),
    url(r'^games/$', games),
    url(r'^buy/$', buy),
    url(r'^payment/cancel/$', payment),
    url(r'^payment/error/$', payment),
    url(r'^payment/success/$', payment),
    ]
