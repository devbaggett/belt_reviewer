from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^users$', views.createUser),
	url(r'^login$', views.loginUser),
	url(r'^books$', views.indexBook),
	url(r'^books/new$', views.newBook),
	url(r'^reviews$', views.createBookAndReview),
	url(r'^logout$', views.logout),
]