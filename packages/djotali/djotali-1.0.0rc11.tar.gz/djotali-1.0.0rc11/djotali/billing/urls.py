# coding: utf8

from django.conf.urls import url

from djotali.billing import views

app_name = 'billing'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
]
