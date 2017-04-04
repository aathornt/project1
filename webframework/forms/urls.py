from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^addtrip/', views.addtrip, name='addtrip'),
    url(r'^register/',views.register, name='register'),
    url(r'^addexpense/', views.addexpense, name='addexpense'),
    url(r'^trip/', views.trip, name='trip'),
    url(r'^addmeal/', views.addmeal, name='addmeal')

]
