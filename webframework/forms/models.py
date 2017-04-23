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

class Trip(models.Model):
	Trip_ID = models.AutoField(primary_key=True)
	Username = models.ForeignKey(User, on_delete=models.CASCADE, blank=
		True, null=True)
	Contact_Person = models.CharField(max_length=200)
	Department = models.CharField(max_length=200)
	Place = models.CharField(max_length=200)
	Purpose = models.CharField(max_length=200)
	Date_Left = models.DateField()
	Date_Returned = models.DateField()
	Time_Left = models.TimeField()
	Time_Returned = models.TimeField()
	Is_Active = models.CharField(max_length=5)

class Post(models.Model):
	Date = models.DateField()
	Cost = models.FloatField()
	Added = models.DateTimeField(default=datetime.now, blank=True)
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
	
