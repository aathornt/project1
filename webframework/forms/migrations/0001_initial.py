# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('Meal_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Meal_Category', models.CharField(choices=[(b'Breakfast', b'Breakfast'), (b'Lunch', b'Lunch'), (b'Dinner', b'Dinner')], default=b'Breakfast', max_length=30)),
                ('Date', models.DateField()),
                ('Meal_No_Tip', models.FloatField()),
                ('Meal_Tip', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('Trip_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Contact_Person', models.CharField(max_length=200)),
                ('Place', models.CharField(max_length=200)),
                ('Purpose', models.CharField(max_length=200)),
                ('Date_Left', models.DateField()),
                ('Date_Returned', models.DateField()),
                ('Time_Left', models.TimeField()),
                ('Time_Returned', models.TimeField()),
                ('Is_Active', models.CharField(max_length=5)),
                ('Username', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='meal',
            name='Trip_ID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='forms.Trip'),
        ),
    ]
