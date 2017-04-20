from django.forms import ModelForm
from .models import Meal
from .models import Trip
from django import forms
from django.contrib.auth.models import User


class UserForm(ModelForm):
	password=forms.CharField(widget=forms.PasswordInput())
	# confirm_password=forms.CharField()
	class Meta:
		model = User;
		fields = ['username', 'password', 'email', 'first_name', 'last_name']

# def clean(self):
# 	cleaned_data = super(UserForm, self).clean()
# 	password = cleaned_data.get("password")
# 	confirm_password = cleaned_data.get("confirm_password")




# class ConfirmForm(forms.Form):
# 	confirm = forms.CharField(max_length=30)

class MealForm(ModelForm):
	Date = forms.DateField(input_formats=['%m-%d-%y'])
	class Meta:
		model = Meal;
		fields = ['Meal_Category', 'Date', 'Meal_No_Tip', 'Meal_Tip', 'Trip_ID']

class TripForm(ModelForm):
	Date_Left = forms.DateField(input_formats=['%m-%d-%y'])
	Date_Returned = forms.DateField(input_formats=['%m-%d-%y'])
	Time_Left = forms.TimeField(input_formats=['%H:%M'])
	Time_Returned = forms.TimeField(input_formats=['%H:%M'])
	class Meta:
		model = Trip;
		fields = [ 'Username', 'Place', 'Purpose', 'Date_Left', 'Time_Left', 'Date_Returned', 'Time_Returned', 'Contact_Person', 'Is_Active']

