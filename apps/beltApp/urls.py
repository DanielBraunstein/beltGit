from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^register$', views.register),
    url(r'^login', views.login),
    url(r'^logout', views.logout),
    url(r'^friends', views.friends),
    url(r'^dislike/(?P<former_friend_id>\d+)$', views.dislike),
    url(r'^like/(?P<new_friend_id>\d+)$', views.like),
    url(r'^user/(?P<user_id>\d+)/$', views.userInfo),
    url(r'^$', views.index),
]
