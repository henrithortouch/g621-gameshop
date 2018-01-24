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
"from django.urls import path"
from django.conf.urls import url
from gameshop.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^$', home),
    url(r'^about/$', about),
    url(r'^register/$', register),
    url(r'^login/$', auth_views.login, {'template_name': 'gameshop/authentication/login.html'}),
    url(r'^logout/$',logout_page),
    url(r'^shop/$'), gameshop),
    url(r'^gamescreen/$', gamescreen),
    url(r'^inventory/dev/$', dev_inventory),
    url(r'^inventory/$', inventory),
    ]
