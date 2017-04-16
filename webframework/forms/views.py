from django.http import HttpResponse
from django.shortcuts import render
from .forms import MealForm
from .forms import UserForm
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
		# check whether it's valid:
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			email = form.cleaned_data['email']
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']

			user = User.objects.create_user(username, email, password,  first_name = first_name, last_name  = last_name)
			# save data as an instance in a database
			user.save()
			return HttpResponse('Thank You! <a href="../../">Return</a>')
			
	else:
		# We'll create a blank form if we have a GET
		form = UserForm()
	return render(request, 'register.html', {'form': form})

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
	return render(request, 'addmeal.html', {'form': form})
