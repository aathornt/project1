from django.conf.urls import url
# from django.view.generic.simple import direct_to_template
# from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
url(r'^$', views.index, name='index'),
url(r'^addtrip/', views.addtrip, name='addtrip'),
url(r'^register/', views.register, name='register'),
url(r'^trip/', views.trip, name='trip'),
url(r'^addmeal/', views.addmeal, name='addmeal'),
url(r'^addexpense/', views.addexpense, name='addexpense'),
url(r'^signout/', views.signout, name='signout'),
url(r'^dailyexpenses/', views.dailyexpenses, name='dailyexpenses'),
url(r'^finalize/', views.finalize, name='finalize'),
url(r'^triplist/', views.triplist, name='triplist'),
url(r'^finalconfirm/', views.finalconfirm, name ='finalconfirm'),
url(r'^failregistration/', views.failregistration, name='failregistration'),
url(r'^expenselist/', views.expenselist, name='expenselist'),
url(r'^edittrip/', views.edittrip, name='edittrip'),
url(r'^deletetrip/', views.deletetrip, name='deletetrip'),
url(r'^activate/', views.activate, name='activate'),
url(r'^deleteexpense/', views.deleteexpense, name='deleteexpense'),
url(r'^registrationfees/', views.registrationfees, name='registrationfees'),
url(r'^editexpense/', views.editexpense, name='editexpense'),
url(r'^transportation/', views.transportation, name='transportation'),
url(r'^personalcar/', views.personalcar, name='personalcar')
]
