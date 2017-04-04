from django.http import HttpResponse
from django.shortcuts import render

from .forms import TravelerForm
from .forms import MealForm
from .models import Traveler
from .models import Meal


# Originally, there is no post so we go to the else and create a form
# from TravelerForm() in forms.py we then render the request and the
# template to display a basic html page
def register(request):
	# if this is a post request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = TravelerForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# save data as an instance in a database
			form.save()
			# reply with thank you, offer them a chance to enter again
			return HttpResponse('Thank you! <a href="/forms/register/">Return</a>')
	else:
		# We'll create a blank form if we have a GET
		form = TravelerForm()
	return render(request, 'register.html', {'form': form})

def addtrip(request):
	return render(request, 'addtrip.html', {})

def main(request):
	recent = Traveler.objects.all().order_by('First_Name')[:3]
	return render(request, 'main.html', {'recent' : recent})

def addexpense(request):
	return render(request, 'addexpenses.html', {})

def trip(request):
	return render(request, 'trip.html', {})

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
			return HttpResponse('Thank you! <a href="/forms/addmeal/">Return</a>')
	else:
		# We'll create a blank form if we have a GET
		form = MealForm()
	return render(request, 'addmeal.html', {'form': form})

