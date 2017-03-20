from django.db import models

# Create your models here.
class Traveler(models.Model):
	employee_id = models.BigIntegerField(primary_key=True)
	employee_name = models.CharField(max_length=200)
	sap_id = models.BigIntegerField()
	employee_email = models.CharField(max_length=200)

# class Trip(models.Model)
# 	trip_id = models.AutoField(primary_key = True)
# 	trip_loc = models.CharField(max_length=200)
# 	start_date = models.DateTimeField()
# 	end_date = models.DateTimeField()
# 	transportation_type = models.CharField(max_length=200)
# 	employee = models.ForeignKey(Traveler, on_delete=models.CASCADE)

# class Expense(models.Model)
# 	expenses_id = models.AutoField(primary_key = True)
# 	trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
# 	date