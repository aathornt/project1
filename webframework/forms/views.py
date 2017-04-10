from django.http import HttpResponse
from django.shortcuts import render

from .forms import TravelerForm
from .forms import MealForm
from .forms import UserForm
from .models import Traveler
from .models import Meal
from .models import User

from django.contrib.auth.models import User

# Originally, there is no post so we go to the else and create a form
# from TravelerForm() in forms.py we then render the request and the
# template to display a basic html page

#TODO copy views from expenses

def register(request):
	# if this is a post request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = UserForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# save data as an instance in a database
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
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
	return render(request, 'register.html', {'form': form})

def addtrip(request):
	return render(request, 'addtrip.html', {})

def index(request):
	# recent = Traveler.objects.all().order_by('First_Name')[:3]
	recent = Meal.objects.all().order_by('-Meal_ID')[:3]
	return render(request, 'main.html', {'recent': recent})

def trip(request):
	recent = Meal.objects.all().order_by('-Meal_ID')[:3]
	return render(request, 'trip.html', {'recent': recent})

def addexpense(request):
	return render(request, 'addexpenses.html', {})

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
