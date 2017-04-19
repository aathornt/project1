from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render
from django.shortcuts import redirect

from .forms import MealForm
from .forms import UserForm
from .forms import ConfirmForm
from .forms import TripForm
from .models import Meal
from .models import Trip
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

#TODO copy views from expenses
def register(request):
	# if this is a post request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = UserForm(request.POST)
		confirm = UserForm(request.POST)
		# check whether it's valid:
		if (form.is_valid() & confirm.is_valid()):
			# save data as an instance in a database
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			confirm = confirm.cleaned_data['password']
			first = form.cleaned_data['first_name']
			last = form.cleaned_data['last_name']
			first = form.cleaned_data['first_name']
			last = form.cleaned_data['last_name']
			email = form.cleaned_data['email']
			user = User.objects.create_user(username, email, password, first_name=first, last_name=last)
			user.save()
			# reply with thank you, offer them a chance to enter again
			return HttpResponse('Thank you! <a href="../../">Return</a>')
	else:
		# We'll create a blank form if we have a GET
		form = UserForm()
		confirm = UserForm()
		return render(request, 'register.html', {'form': form, 'confirm': confirm})

@login_required(login_url='/')
def addtrip(request):

	# if this is a post request we need to process the form data
	if request.method == 'POST':

		# create a form instance and populate it with data from the request:
		form = TripForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# save data as an instance in a database
			form.save()
			# reply with thank you, offer them a chance to enter again
			return HttpResponse('Thank you! <a href="/forms/trip/">Return</a>')
	else:
		# We'll create a blank form if we have a GET
		form = TripForm()
	return render(request, 'addtrip.html', {'form': form})

@login_required(login_url='/')
def index(request):
	# recent = Traveler.objects.all().order_by('First_Name')[:3]
	recent = Meal.objects.all().order_by('-Meal_ID')[:3]
	return render(request, 'main.html', {'recent': recent})

def signout(request):
	logout(request)
	return redirect('/')

@login_required(login_url='/')
def trip(request):
	recent = Meal.objects.all().order_by('-Meal_ID')[:3]
	return render(request, 'trip.html', {'recent': recent})

@login_required(login_url='/')
def addexpense(request):
	# if not request.user.is_authenticated:
	# 	return redirect('/')
	return render(request, 'addexpenses.html', {})

@login_required(login_url='/')
def addmeal(request):
	# if this is a post request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = MealForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# save data as an instance in a database
			form.save()
			# reply with thank you, offer them a chance to enter again
			return HttpResponse('Thank you! <a href="/forms/trip/">Return</a>')
	else:
		# We'll create a blank form if we have a GET
		form = MealForm()
		current_user = request.user
		active = Trip.objects.get(Is_Active = "True", Username=current_user.id)
	return render(request, 'addmeal.html', {'form': form, 'active': active.Trip_ID})
