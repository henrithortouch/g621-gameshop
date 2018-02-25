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
    path('activate/<str:activation_link>/', activate),
    url(r'^register/$', register),
    url(r'^login/$', auth_views.login, {'template_name': 'gameshop/authentication/login.html'}),
    url(r'^logout/$',logout_page),
    path('shop/<str:genre>/', shop),
    path('shop/', shop),
    path('gamescreen/<int:game_id>/save/', machine_save),
    path('gamescreen/<int:game_id>/load/', machine_load),
    path('gamescreen/<int:game_id>/score/', machine_score),
    path('gamescreen/<int:game_id>/', views.gamescreen),
    path('studio/<int:game_id>/', editgame),
    path('studio/addgame/', editgame),
    path('studio/', studio),
    path('inventory/', inventory),
    url(r'^buy/$', buy),
    url(r'^payment/cancel/$', payment),
    url(r'^payment/error/$', payment),
    url(r'^payment/success/$', payment),
    ]
