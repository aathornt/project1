from django.forms import ModelForm
from .models import Traveler
from .models import Meal
# from .models import Trip
from django import forms
from django.contrib.auth.models import User


class TravelerForm(ModelForm):
	class Meta:
		model = Traveler;
		fields = ['SAP_ID', 'First_Name', 'Last_Name', 'Email', 'Title', 'Department_Name',]
	
class MealForm(ModelForm):
	Date = forms.DateField(input_formats=['%m-%d-%y'])
	class Meta:
		model = Meal;
		fields = ['Meal_Category', 'Date', 'Meal_No_Tip', 'Meal_Tip']

class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ('username', 'password', 'email', 'first_name', 'last_name')

# class TripForm(ModelForm):
# 	class Meta:
# 		model = Trip;
# 		fields = ['Trip_ID', 'Traveler', 'Contact_Person', 'Place', 'Purpose', 'Date_Left', 'Date_Returned', 'Time_Left', 'Time_Returned']
# 		exclude = ("Traveler",)