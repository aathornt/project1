from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime

CHOICES=(
		('Breakfast', 'Breakfast'),
		('Lunch', 'Lunch'),
		('Dinner', 'Dinner'),

	)
CATEGORIES=(
		('Lodging', 'Lodging'),
		('Meal Tips', 'Meal Tips'),
		('Taxi', 'Taxi'),
		('Parking, Tolls', 'Parking, Tolls'),
		('Gasoline', 'Gasoline'),
		('Business Calls', 'Business Calls'),
	)
FEES=(
		('Conference Fees', 'Conference Fees'),
		('Banquet Fees', 'Banquet Fees'),
		('Dues', 'Dues'),
	)
VEHICLES=(
		('Airfare', 'Airfare'),
		('Rental Car','Rental Car'),
		('Bus/Train','Bus/Train'),
	)
FINANCIAL=(
		('Cost Center', 'Cost Center'),
		('Internal Order', 'Internal Order'),
)

class Trip(models.Model):
	Trip_ID = models.AutoField(primary_key=True)
	Username = models.ForeignKey(User, on_delete=models.CASCADE, blank=
		True, null=True)
	Contact_Person = models.CharField(max_length=200)
	Department = models.CharField(max_length=200)
	Place = models.CharField(max_length=200)
	Purpose = models.CharField(max_length=200)
	Date_Departed = models.DateField()
	Time_Departed = models.TimeField()
	Date_Returned = models.DateField()
	Time_Returned = models.TimeField()
	Is_Active = models.CharField(max_length=5)

class Post(models.Model):
	Date = models.DateField()
	Cost = models.FloatField()
	Added = models.DateTimeField(default=datetime.now, blank=True)
	PCategory = models.CharField(max_length=30)
	def __published_today(self):
		return self.Added.date() == datetime.date.today()
	Trip_ID = models.ForeignKey(Trip, on_delete=models.CASCADE, blank=True, null=True)

	class Meta:
		abstract = False


class Meal(Post):
	Meal_ID = models.AutoField(primary_key=True)
	Meal_Category = models.CharField(max_length=30, choices=CHOICES, default='Breakfast')
	Tip = models.FloatField()

class DailyExpenses(Post):
	DailyExpense_ID = models.AutoField(primary_key=True)
	Category = models.CharField(max_length=30, choices = CATEGORIES, default='Lodging')

class RegistrationFees(Post):
	RegistrationFee_ID = models.AutoField(primary_key = True)
	Category = models.CharField(max_length=30, choices = FEES, default='Conference Fees')

class Transportation(Post):
	Transportation_ID = models.AutoField(primary_key = True)
	Category = models.CharField(max_length=30, choices = VEHICLES, default='Airfare')

class Financial(Post):
	Financial_ID = models.AutoField(primary_key = True)
	Category = models.CharField(max_length=30, choices = FINANCIAL, default='Cost Center')
	Number = models.CharField(max_length=30)
