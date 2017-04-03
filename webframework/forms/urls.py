from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^trip/', views.trip, name='trip'),
    url(r'^register/',views.register, name='register'),
]
