from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

CHOICES=(
		('Breakfast', 'Breakfast'),
		('Lunch', 'Lunch'),
		('Dinner', 'Dinner'),

	)

class Trip(models.Model):
	Trip_ID = models.AutoField(primary_key=True)
	Username = models.ForeignKey(User, on_delete=models.CASCADE, blank=
		True, null=True)
	Contact_Person = models.CharField(max_length=200)
	Place = models.CharField(max_length=200)
	Purpose = models.CharField(max_length=200)
	Date_Left = models.DateField()
	Date_Returned = models.DateField()
	Time_Left = models.TimeField()
	Time_Returned = models.TimeField()
	Is_Active = models.CharField(max_length=5)

class Meal(models.Model):
	Meal_ID = models.AutoField(primary_key=True)
	Meal_Category = models.CharField(max_length=30, choices=CHOICES, default='Breakfast')
	Date = models.DateField()
	Meal_No_Tip = models.FloatField()
	Meal_Tip = models.FloatField()
	Trip_ID = models.ForeignKey(Trip, on_delete=models.CASCADE, blank=True, null=True)
