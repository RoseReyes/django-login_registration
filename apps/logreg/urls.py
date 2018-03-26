from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'login$', views.login),
    url(r'^quotes$', views.quotes, name = "dashboard"),
    url(r'^addQuote$', views.addQuote),
    url(r'^addFavorite$', views.addFavorite),
    url(r'^delFavorite$', views.delFavorite),
    url(r'^users$', views.users),
    url(r'^showUserPost$', views.showUserPost),
    url(r'logout$', views.logout, name='my_logout'),
]