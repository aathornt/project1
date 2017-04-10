from django.db import models
from django.contrib.auth.models import User


# # Create your models here.
class Traveler(models.Model):
	SAP_ID = models.BigIntegerField(primary_key=True)
	First_Name = models.CharField(max_length=200)
	Last_Name = models.CharField(max_length=200)
	Title = models.CharField(max_length=200)
	Email = models.CharField(max_length=200)
	Department_Name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.First_Name

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
	Traveler = models.ForeignKey('Traveler', on_delete=models.CASCADE)
	Contact_Person = models.CharField(max_length=200)
	Place = models.CharField(max_length=200)
	Purpose = models.CharField(max_length=200)
	Date_Left = models.DateField()
	Date_Returned = models.DateField()
	Time_Left = models.TimeField()
	Time_Returned = models.TimeField()

