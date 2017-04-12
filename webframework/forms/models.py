from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


CHOICES=(
		('Breakfast', 'Breakfast'),
		('Lunch', 'Lunch'),
		('Dinner', 'Dinner'),

	)

class Meal(models.Model):
	Meal_ID = models.AutoField(primary_key=True)
	Meal_Category = models.CharField(max_length=30, choices=CHOICES, default='Breakfast')
	Date = models.DateField()
	Meal_No_Tip = models.FloatField()
	Meal_Tip = models.FloatField()

class Trip(models.Model):
	Trip_ID = models.AutoField(primary_key=True)
	User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	Contact_Person = models.CharField(max_length=200)
	Place = models.CharField(max_length=200)
	Purpose = models.CharField(max_length=200)
	Date_Left = models.DateField()
	Date_Returned = models.DateField()
	Time_Left = models.TimeField()
	Time_Returned = models.TimeField()

