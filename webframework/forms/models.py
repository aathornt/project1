from django.db import models

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
		('BR', 'Breakfast'),
		('LUN', 'Lunch'),
		('DIN', 'Dinner'),

	)

class Meal(models.Model):
	Meal_ID = models.AutoField(primary_key=True)
	Meal_Category = models.CharField(max_length=3, choices=CHOICES, default='BR')
	Date = models.DateField()
	Meal_No_Tip = models.FloatField()
	Meal_Tip = models.FloatField()
	# Breakfast_No_Tip = models.FloatField()
	# Breakfast_Tip = models.FloatField()
	# Lunch_No_Tip = models.FloatField()
	# Lunch_Tip = models.FloatField()
	# Dinner_No_Tip = models.FloatField()
	# Dinner_Tip = models.FloatField()
