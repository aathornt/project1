from django.forms import ModelForm
from .models import Meal
from .models import Trip
from .models import DailyExpenses
from .models import RegistrationFees
from .models import Post
from .models import Transportation
from .models import Financial
from .models import PersonalCar
from .models import Miscellaneous
from django import forms
from django.contrib.auth.models import User
from time import strftime
from datetimewidget.widgets import DateWidget, TimeWidget


class UserForm(ModelForm):
	password=forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User;
		fields = ['username', 'password', 'email', 'first_name', 'last_name']

class ConfirmForm(ModelForm):
	password=forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User;
		fields = ['password']

class MealForm(ModelForm):
	Date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
	Cost = forms.FloatField()
	class Meta:
		model = Meal;
		fields = ['Meal_Category', 'Date', 'Cost', 'Added', 'Tip', 'Trip_ID', 'PCategory']


class DailyExpensesForm(ModelForm):
	Date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
	Cost = forms.FloatField()
	class Meta:
		model = DailyExpenses;
		fields = ['Category', 'Date', 'Cost', 'Added', 'Trip_ID', 'PCategory']

class TripForm(ModelForm):
	Date_Departed = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
	Date_Returned = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
	Time_Departed = forms.TimeField(widget=TimeWidget(usel10n=True, bootstrap_version=3))
	Time_Returned = forms.TimeField(widget=TimeWidget(usel10n=True, bootstrap_version=3))

	class Meta:
		model = Trip;
		fields = [ 'Username', 'Department', 'Place', 'Purpose', 'Accompanied_By', 'Phone_Number', 'Exchange',  'Date_Departed', 'Time_Departed', 'Date_Returned', 'Time_Returned', 'Contact_Person', 'Is_Active']

class RegistrationFeesForm(ModelForm):
	Date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
	class Meta:
		model = RegistrationFees;
		fields = ['Category', 'Date', 'Cost', 'Added', 'Trip_ID', 'PCategory']

class TransportationForm(ModelForm):
	Date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
	class Meta:
		model = Transportation;
		fields = ['Category', 'Date', 'Cost', 'Added', 'Trip_ID', 'PCategory']

class FinancialForm(ModelForm):
	Date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
	class Meta:
		model = Financial;
		fields = ['Category', 'Date', 'Cost', 'Added', 'Number', 'Trip_ID', 'PCategory']

class PersonalCarForm(ModelForm):
	Date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
	class Meta:
		model = PersonalCar;
		fields = ['From', 'To', 'Category', 'Mileage', 'Date', 'Cost', 'Added', 'Trip_ID', 'PCategory']

class MiscellaneousForm(ModelForm):
	Date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
	class Meta:
		model = Miscellaneous;
		fields = ['Date', 'Cost', 'Added', 'Trip_ID', 'Description', 'PCategory']
