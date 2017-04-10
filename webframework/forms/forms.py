from django.forms import ModelForm
from .models import Traveler
from .models import Meal
from django import forms
from django.contrib.auth.models import User


class UserForm(ModelForm):
	class Meta:
		model = User;
		fields = ['username', 'email', 'password', 'first_name', 'last_name']

class TravelerForm(ModelForm):
	class Meta:
		model = Traveler;
		fields = ['SAP_ID', 'First_Name', 'Last_Name', 'Email', 'Title', 'Department_Name',]

# class MealForm(ModelForm):
# 	Date = forms.DateField(input_formats=['%m-%d-%y'])
# 	class Meta:
# 		model = Meal;
# 		fields = ['Date', 'Breakfast_No_Tip', 'Breakfast_Tip', 'Lunch_No_Tip', 'Lunch_Tip', 'Dinner_No_Tip','Dinner_Tip',]


class MealForm(ModelForm):
	Date = forms.DateField(input_formats=['%m-%d-%y'])
	class Meta:
		model = Meal;
		fields = ['Meal_Category', 'Date', 'Meal_No_Tip', 'Meal_Tip']
