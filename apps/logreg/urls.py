from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'login$', views.login),
    url(r'^landing_page$', views.landing_page, name = "dashboard"),
    url(r'^createPost$', views.createPost),
    url(r'^createFavorite$', views.createFavorite),
    url(r'^removeFavorite$', views.removeFavorite),
    url(r'^users/(?P<id>\d+)', views.users),
    url(r'logout$', views.logout, name='my_logout'),
]