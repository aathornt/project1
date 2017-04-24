from django.forms import ModelForm
from .models import Meal
from .models import Trip
from .models import DailyExpenses
from .models import Post
from django import forms
from django.contrib.auth.models import User
from time import strftime


class UserForm(ModelForm):
	password=forms.CharField(widget=forms.PasswordInput())
	# confirm_password=forms.CharField()
	class Meta:
		model = User;
		fields = ['username', 'password', 'email', 'first_name', 'last_name']


class MealForm(ModelForm):
	Date = forms.DateField(input_formats=['%m/%d/%y'])
	Cost = forms.FloatField()
	class Meta:
		model = Meal;
		fields = ['Meal_Category', 'Date', 'Cost', 'Added', 'Tip', 'Trip_ID']


class DailyExpensesForm(ModelForm):
	Date = forms.DateField(input_formats=['%m/%d/%y'])
	Cost = forms.FloatField()
	class Meta:
		model = DailyExpenses;
		fields = ['Category', 'Date', 'Cost', 'Added', 'Trip_ID']

class TripForm(ModelForm):
	Date_Departed = forms.DateField(input_formats=['%m/%d/%y'])
	Date_Returned = forms.DateField(input_formats=['%m/%d/%y'])
	Time_Departed = forms.TimeField(input_formats=['%H:%M'])
	Time_Returned = forms.TimeField(input_formats=['%H:%M'])
	class Meta:
		model = Trip;
		fields = [ 'Username', 'Department', 'Place', 'Purpose', 'Date_Departed', 'Time_Departed', 'Date_Returned', 'Time_Returned', 'Contact_Person', 'Is_Active']

