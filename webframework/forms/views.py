from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render
from django.shortcuts import redirect

from .forms import MealForm
from .forms import UserForm
from .forms import TransportationForm
from .forms import TripForm
from .forms import DailyExpensesForm
from .forms import RegistrationFeesForm
from .forms import FinancialForm
from .forms import PersonalCarForm
from .forms import MiscellaneousForm
from .models import Miscellaneous
from .models import PersonalCar
from .models import Transportation
from .models import Meal
from .models import Trip
from .models import Post
from .models import DailyExpenses
from .models import RegistrationFees
from .models import Financial
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from django.utils.formats import date_format
from django.utils import formats
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format



#TODO copy views from expenses
def register(request):
	# if this is a post request we need to process the form data

	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = UserForm(request.POST)
		# confirm = UserForm(request.POST)
		# check whether it's valid:

		if  form.is_valid():
			 # & confirm.is_valid()
			# save data as an instance in a database
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			# confirm_password = form.cleaned_data['confirm_password']
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']


			user = User.objects.create_user(username, email, password,  first_name = first_name, last_name  = last_name)
			# save data as an instance in a database

			user.save()
			# reply with thank you, offer them a chance to enter again
			return redirect('/')
		else:
			return redirect('/forms/failregistration/')

	else:
		# We'll create a blank form if we have a GET
		form = UserForm()
		# confirm = UserForm()
		return render(request, 'register.html', {'form': form})

@login_required(login_url='/')
def index(request):
	current_user = request.user;
	name = current_user.first_name;
	if Trip.objects.filter(Is_Active = True, Username = current_user.id).exists():
		active = Trip.objects.get(Is_Active = True, Username = current_user.id)
		recent = Post.objects.select_related('meal', 'dailyexpenses', 'registrationfees', 'financial').filter(Trip_ID_id = active.Trip_ID).order_by('-Added')[:6]
		popuperror2= 'True'
		na = 'N/A'
		return render(request, 'main.html', {'recent': recent, 'name' : name, 'active' : active, 'popuperror2': popuperror2, 'na': na})
	else:
		popuperror= 'True'
		trip = 'None'
		category = 'No Active Trip'
		na = 'N/A'
		return render(request, 'main.html', {'name' : name, 'trip': trip, 'category': category, 'na': na, 'popuperror': popuperror})




@login_required(login_url='/')
def trip(request):
	current_user = request.user
	if Trip.objects.filter(Is_Active = True, Username = current_user.id).exists():
		active = Trip.objects.get(Is_Active = True, Username = current_user.id)
		recent = Meal.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-Meal_ID')[:3]
		recentexp = DailyExpenses.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-DailyExpense_ID')[:3]
		recentcar = PersonalCar.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-PersonalCar_ID')[:3]
		recentpub = Transportation.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-Transportation_ID')[:3]
		recentreg = RegistrationFees.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-RegistrationFee_ID')[:3]
		recentcos = Financial.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-Financial_ID')[:3]
		recentmis = Miscellaneous.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-Miscellaneous_ID')[:3]

		na = 'N/A'
		no = 'No Recent Expense'
		return render(request, 'trip.html', {'recent': recent, 'no': no, 'na': na, 'active': active, 'recentexp': recentexp, 'recentcar': recentcar, 'recentpub': recentpub, 'recentreg': recentreg, 'recentcos': recentcos, 'recentmis': recentmis})
	else:
		return redirect('/forms/')



@login_required(login_url='/')
def addtrip(request):
	current_user = request.user;
	if Trip.objects.filter(Is_Active = True, Username = current_user.id).exists():
		# if this is a post request we need to process the form data
		return redirect('/forms/')
	else:
		if request.method == 'POST':

			# create a form instance and populate it with data from the request:
			form = TripForm(request.POST)
			# check whether it's valid:
			if form.is_valid():
				# save data as an instance in a database
				form.save()
				# reply with thank you, offer them a chance to enter again
				return redirect('/forms/trip/')
		else:
			# We'll create a blank form if we have a GET
			form = TripForm()
		return render(request, 'addtrip.html', {'form': form})


@login_required(login_url='/')
def addexpense(request):
	return render(request, 'addexpenses.html', {})

@login_required(login_url='/')
def addmeal(request):
	# if this is a post request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = MealForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# save data as an instance in a database
			form.save()
			# reply with thank you, offer them a chance to enter again
			return redirect('/forms/trip/')
			# return HttpResponse('Thank you! <a href="/forms/trip/">Return</a>')
		else:
			return HttpResponse('nope')
	else:
		# We'll create a blank form if we have a GET
		form = MealForm()
		current_user = request.user
		active = Trip.objects.get(Is_Active = "True", Username=current_user.id)
		timestamp = Meal.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-Added')
		return render(request, 'addmeal.html', {'form': form, 'active': active.Trip_ID, 'timestamp': timestamp})


@login_required(login_url='/')
def personalcar(request):
	if request.method == "POST":
		form = PersonalCarForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# save data as an instance in a database
			form.save()
			# reply with thank you, offer them a chance to enter again
			return redirect('/forms/trip/')
			# return HttpResponse('Thank you! <a href="/forms/trip/">Return</a>')
	else:
		# We'll create a blank form if we have a GET
		form = PersonalCarForm()
		current_user = request.user
		active = Trip.objects.get(Is_Active = "True", Username=current_user.id)
		timestamp = PersonalCar.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-Added')
		return render(request, 'personalcar.html', {'form': form, 'active': active.Trip_ID, 'timestamp': timestamp })



@login_required(login_url='/')
def transportation(request):
	if request.method == "POST":
		form = TransportationForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# save data as an instance in a database
			form.save()
			# reply with thank you, offer them a chance to enter again
			return redirect('/forms/trip/')
			# return HttpResponse('Thank you! <a href="/forms/trip/">Return</a>')
	else:
		# We'll create a blank form if we have a GET
		form = TransportationForm()
		current_user = request.user
		active = Trip.objects.get(Is_Active = "True", Username=current_user.id)
		timestamp = Transportation.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-Added')
		return render(request, 'transportation.html', {'form': form, 'active': active.Trip_ID, 'timestamp': timestamp })



@login_required(login_url='/')
def dailyexpenses(request):
	# if this is a post request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = DailyExpensesForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# save data as an instance in a database
			form.save()
			# reply with thank you, offer them a chance to enter again
			return redirect('/forms/trip/')
			# return HttpResponse('Thank you! <a href="/forms/trip/">Return</a>')
	else:
		# We'll create a blank form if we have a GET
		form = DailyExpensesForm()
		current_user = request.user
		active = Trip.objects.get(Is_Active = "True", Username=current_user.id)
		timestamp = DailyExpenses.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-Added')
		return render(request, 'dailyexpenses.html', {'form': form, 'active': active.Trip_ID, 'timestamp': timestamp })


@login_required(login_url='/')
def miscellaneous(request):
	# if this is a post request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = MiscellaneousForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# save data as an instance in a database
			form.save()
			# reply with thank you, offer them a chance to enter again
			return redirect('/forms/trip/')
	else:
		# We'll create a blank form if we have a GET
		form = MiscellaneousForm()
		current_user = request.user
		active = Trip.objects.get(Is_Active = "True", Username=current_user.id)
		timestamp = Miscellaneous.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-Added')
		return render(request, 'miscellaneous.html', {'form': form, 'active': active.Trip_ID, 'timestamp': timestamp })



@login_required(login_url='/')
def registrationfees(request):
	# if this is a post request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = RegistrationFeesForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# save data as an instance in a database
			form.save()
			# reply with thank you, offer them a chance to enter again
			return redirect('/forms/trip/')
			# return HttpResponse('Thank you! <a href="/forms/trip/">Return</a>')
	else:
		# We'll create a blank form if we have a GET
		form = RegistrationFeesForm()
		current_user = request.user
		active = Trip.objects.get(Is_Active = "True", Username=current_user.id)
		timestamp = RegistrationFees.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-Added')
		return render(request, 'registrationfees.html', {'form': form, 'active': active.Trip_ID, 'timestamp': timestamp })


@login_required(login_url='/')
def triplist(request):
	current_user = request.user
	if Trip.objects.filter(Is_Active=True, Username = current_user.id).exists():
		trip = Trip.objects.get(Is_Active = True, Username = current_user.id)
		trips = Trip.objects.filter(Username = current_user.id).order_by('-Trip_ID')
		return render(request, 'triplist.html', {'trips': trips, 'trip': trip})
	else:
		place = 'None'
		na = 'N/A'
		trips = Trip.objects.filter(Username = current_user.id).order_by('-Trip_ID')
		return render(request, 'triplist.html', {'trips': trips, 'place': place, 'na': na})

@login_required(login_url='/')
def expenselist(request):
	current_user = request.user
	active = Trip.objects.get(Is_Active = True, Username = current_user.id)
	if Post.objects.select_related('meal', 'dailyexpenses').filter(Trip_ID_id = active.Trip_ID).exists():
		recent = Post.objects.select_related('meal', 'dailyexpenses', 'registrationfees').filter(Trip_ID_id = active.Trip_ID).order_by('-Added')
		return render(request, 'expenselist.html', {'active': active, 'recent': recent})

	else:
		category = 'None'
		na = 'N/A'
		return render(request, 'expenselist.html', {'category': category, 'na': na})

def failregistration(request):
	return render(request, 'failregistration.html', {})


@login_required(login_url='/')
def finalconfirm(request):
	return render(request, 'finalconfirm.html', {})


def signout(request):
	logout(request)
	return redirect('/')

@login_required(login_url='/')
def finalize(request):
	current_user = request.user
	active = Trip.objects.get(Is_Active = True, Username = current_user.id)
	active.Is_Active = "False"
	active.save()
	return redirect('/forms/finalconfirm/')


@login_required(login_url='/')
def edittrip(request):
	current_user = request.user
	active = Trip.objects.get(Is_Active = True, Username = current_user.id)

	if request.method == "POST":
		form = TripForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.Trip_ID = active.Trip_ID
			form.save()
			return redirect('/forms/triplist/')
	else:
		my_record = Trip.objects.get(Trip_ID = active.Trip_ID)
		form = TripForm(instance=my_record)
		return render(request, 'edittrip.html', {'form' : form})

@login_required(login_url='/')
def editexpense(request):
	current_user = request.user
	active = Trip.objects.get(Is_Active=True, Username = current_user.id)
	inst = request.GET.get('category',"")
	ins = str(inst)
	post_id = request.GET.get('id',"")
	edit = "True"


	if request.method == "POST":
		if request.POST.get("PCategory", "") == 'Meal':
			form = MealForm(request.POST)
			if form.is_valid():
				mealid = request.POST.get("Meal_ID", "")
				instance = form.save(commit=False)
				meal = Meal.objects.get(Meal_ID = mealid)
				instance.Trip_ID = meal.Trip_ID
				instance.post_ptr_id = meal.post_ptr_id
				instance.Meal_ID = meal.Meal_ID
				form.save()
				return redirect('/forms/expenselist/')
		elif request.POST.get("PCategory", "") == 'Financial':
			form = FinancialForm(request.POST)
			if form.is_valid():
				financial = request.POST.get("Financial_ID", "")
				instance = form.save(commit=False)
				finance = Financial.objects.get(Financial_ID = financial)
				instance.Trip_ID = finance.Trip_ID
				instance.post_ptr_id = finance.post_ptr_id
				instance.Financial_ID = finance.Financial_ID
				form.save()
				return redirect('/forms/expenselist/')
		elif request.POST.get("PCategory", "") == 'DailyExpense':
			form = DailyExpensesForm(request.POST)
			if form.is_valid():
				dailyexp = request.POST.get("DailyExpense_ID", "")
				instance = form.save(commit=False)
				daily = DailyExpenses.objects.get(DailyExpense_ID = dailyexp)
				instance.Trip_ID = daily.Trip_ID
				instance.post_ptr_id = daily.post_ptr_id
				instance.DailyExpense_ID = daily.DailyExpense_ID
				form.save()
				return redirect('/forms/expenselist/')
		elif request.POST.get("PCategory", "") == 'RegistrationFees':
			form = RegistrationFeesForm(request.POST)
			if form.is_valid():
				regis = request.POST.get("RegistrationFee_ID", "")
				instance = form.save(commit=False)
				reg = RegistrationFees.objects.get(RegistrationFee_ID = regis)
				instance.Trip_ID = reg.Trip_ID
				instance.post_ptr_id = reg.post_ptr_id
				instance.RegistrationFee_ID = reg.RegistrationFee_ID
				form.save()
				return redirect('/forms/expenselist/')
		elif request.POST.get("PCategory", "") == 'Transportation':
			form = TransportationForm(request.POST)
			if form.is_valid():
				trans = request.POST.get("Transportation_ID", "")
				instance = form.save(commit=False)
				tran = Transportation.objects.get(Transportation_ID = trans)
				instance.Trip_ID = tran.Trip_ID
				instance.post_ptr_id = tran.post_ptr_id
				instance.Transportation_ID = tran.Transportation_ID
				form.save()
				return redirect('/forms/expenselist/')
		elif request.POST.get("PCategory", "") == 'Miscellaneous':
			form = MiscellaneousForm(request.POST)
			if form.is_valid():
				misc = request.POST.get("Miscellaneous_ID", "")
				instance = form.save(commit=False)
				mis = Miscellaneous.objects.get(Miscellaneous_ID = misc)
				instance.Trip_ID = mis.Trip_ID
				instance.post_ptr_id = mis.post_ptr_id
				instance.Miscellaneous_ID = mis.Miscellaneous_ID
				form.save()
				return redirect('/forms/expenselist/')
		else:
			form = PersonalCarForm(request.POST)
			if form.is_valid():
				pers = request.POST.get("PersonalCar_ID", "")
				instance = form.save(commit=False)
				per = PersonalCar.objects.get(PersonalCar_ID = pers)
				instance.Trip_ID = per.Trip_ID
				instance.post_ptr_id = per.post_ptr_id
				instance.PersonalCar_ID = per.PersonalCar_ID
				form.save()
				return redirect('/forms/expenselist/')


	else:
		if ins == "Meal":
			meal = Meal.objects.get(post_ptr_id = post_id)
			record = Meal.objects.get(Meal_ID =meal.Meal_ID)
			form = MealForm(instance = record)
			return render(request, 'addmeal.html', {'form' : form, 'edit' : edit, 'record' : record.Meal_ID, 'active' : active.Trip_ID})
		elif ins == "Financial":
			finance = Financial.objects.get(post_ptr_id = post_id)
			record = Financial.objects.get(Financial_ID = finance.Financial_ID)
			form = FinancialForm(instance = record)
			return render(request, 'addfinancial.html', {'form': form, 'edit':edit, 'record': record.Financial_ID, 'active': active.Trip_ID})
		elif ins == "DailyExpense":
			daily = DailyExpenses.objects.get(post_ptr_id = post_id)
			record = DailyExpenses.objects.get(DailyExpense_ID =daily.DailyExpense_ID)
			form = DailyExpensesForm(instance = record)
			return render(request, 'dailyexpenses.html', {'form' : form, 'edit' : edit, 'record' : record.DailyExpense_ID, 'active' : active.Trip_ID})
		elif ins == "RegistrationFees":
			reg = RegistrationFees.objects.get(post_ptr_id = post_id)
			record = RegistrationFees.objects.get(RegistrationFee_ID = reg.RegistrationFee_ID)
			form = RegistrationFeesForm(instance = record)
			return render(request, 'registrationfees.html', {'form' : form, 'edit' : edit, 'record' : record.RegistrationFee_ID, 'active' : active.Trip_ID})
		elif ins == "Transportation":
			trans = Transportation.objects.get(post_ptr_id = post_id)
			record = Transportation.objects.get(Transportation_ID = trans.Transportation_ID)
			form = TransportationForm(instance = record)
			return render(request, 'transportation.html', {'form' : form, 'edit' : edit, 'record' : record.Transportation_ID, 'active' : active.Trip_ID})
		else:
			pers = PersonalCar.objects.get(post_ptr_id = post_id)
			record = PersonalCar.objects.get(PersonalCar_ID = pers.PersonalCar_ID)
			form = PersonalCarForm(instance = record)
			return render(request, 'personalcar.html', {'form' : form, 'edit' : edit, 'record' : record.PersonalCar_ID, 'active' : active.Trip_ID})


@login_required(login_url='/')
def deletetrip(request):
	current_user = request.user
	# active = Trip.objects.get(Is_Active = True, Username = current_user.id)

	ins =request.GET.get('id', "")
	instance = Trip.objects.get(Trip_ID = ins)
	instance.delete()
	return redirect('/forms/triplist/')

@login_required(login_url='/')
def deleteexpense(request):
	current_user = request.user

	ins = request.GET.get('id', "")
	instance = Post.objects.get(id = ins)
	instance.delete()
	return redirect('/forms/expenselist/')

@login_required(login_url='/')
def activate(request):
	current_user = request.user
	if Trip.objects.filter(Is_Active=True, Username = current_user.id).exists():
		active = Trip.objects.get(Is_Active = True, Username = current_user.id)
		active.Is_Active = "False"
		active.save()
		ins = request.GET.get('id',"")
		instance = Trip.objects.get(Trip_ID = ins)
		instance.Is_Active = "True"
		instance.save()
	else :
		ins = request.GET.get('id',"")
		instance = Trip.objects.get(Trip_ID = ins)
		instance.Is_Active = "True"
		instance.save()
	return redirect('/forms/')

@login_required(login_url='/')
def addfinancial(request):
	# if this is a post request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = FinancialForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# save data as an instance in a database
			form.save()
			# reply with thank you, offer them a chance to enter again
			return redirect('/forms/trip/')
			# return HttpResponse('Thank you! <a href="/forms/trip/">Return</a>')
	else:
		# We'll create a blank form if we have a GET
		form = FinancialForm()
		current_user = request.user
		active = Trip.objects.get(Is_Active = "True", Username=current_user.id)
		timestamp = DailyExpenses.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-Added')
		return render(request, 'addfinancial.html', {'form': form, 'active': active.Trip_ID, 'timestamp': timestamp})
