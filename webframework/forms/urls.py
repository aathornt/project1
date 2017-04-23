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
url(r'^dailyexpenses/', views.dailyexpenses, name='dailyexpenses')
]
# ,
# url(r'^finalizetrip/', views.finalizetrip, name='finalizetrip')