from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Sum

from .forms import MealForm
from .forms import UserForm
from .forms import TransportationForm
from .forms import TripForm
from .forms import DailyExpensesForm
from .forms import RegistrationFeesForm
from .forms import FinancialForm
from .forms import PersonalCarForm
from .forms import MiscellaneousForm
from .forms import ConfirmForm

from .models import Meal
from .models import Transportation
from .models import Trip
from .models import Post
from .models import DailyExpenses
from .models import RegistrationFees
from .models import Financial
from .models import PersonalCar
from .models import Miscellaneous
from .models import Confirm

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.formats import date_format
from django.utils import formats
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format




def register(request):
	# if this is a post request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = UserForm(request.POST)
		confirm = ConfirmForm(request.POST)
		# check whether it's valid:
		if  form.is_valid() and confirm.is_valid():
			# save data as an instance in a database
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			confirm = confirm.cleaned_data['confirm']

			# save data as an instance in a database
			if password != confirm:
				popuperror = True
				form = UserForm()
				confirm = ConfirmForm()
				return render(request, 'register.html', {'form': form, 'confirm': confirm, 'popuperror': popuperror})
			else:
				user = User.objects.create_user(username, email, password,  first_name = first_name, last_name  = last_name)
				user.save()
			# redirect to home
			return redirect('/')
		else:
			#redirect to failed signup page
			return redirect('/forms/failregistration/')
	else:
		# We'll create a blank form if we have a GET
		form = UserForm()
		confirm = ConfirmForm()
		return render(request, 'register.html', {'form': form, 'confirm': confirm})

@login_required(login_url='/')
def index(request):
	current_user = request.user;
	name = current_user.first_name;
	if Trip.objects.filter(Is_Active = True, Username = current_user.id).exists():
		active = Trip.objects.get(Is_Active = True, Username = current_user.id)
		recent = Post.objects.select_related('meal', 'dailyexpenses', 'registrationfees', 'financial').filter(Trip_ID_id = active.Trip_ID).order_by('-Added')[:6]
		popuperror2= 'True'
		yea = 'Your Most Recent Expenses'
		na = 'N/A'
		return render(request, 'main.html', {'recent': recent, 'name' : name, 'yea': yea, 'active' : active, 'popuperror2': popuperror2, 'na': na})
	else:
		popuperror= 'True'
		trip = 'None'
		na = 'N/A'
		no = 'No Active Trip'
		return render(request, 'main.html', {'name' : name, 'no': no, 'trip': trip, 'na': na, 'popuperror': popuperror})


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
		post = Post.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-id')
		na = 'N/A'
		no = 'No Recent Expense'
		return render(request, 'trip.html', {'recent': recent, 'no': no, 'na': na, 'post': post, 'active': active, 'recentexp': recentexp, 'recentcar': recentcar, 'recentpub': recentpub, 'recentreg': recentreg, 'recentcos': recentcos, 'recentmis': recentmis})
	else:
		return redirect('/forms/')

@login_required(login_url='/')
def addtrip(request):
	current_user = request.user;
	#if active trip exists don't allow user to add another trip
	if Trip.objects.filter(Is_Active = True, Username = current_user.id).exists():
		return redirect('/forms/')
	else:
		if request.method == 'POST':
			# create a form instance and populate it with data from the request:
			form = TripForm(request.POST)
			# check whether it's valid:
			if form.is_valid():
				if form.cleaned_data['Date_Returned'] < form.cleaned_data['Date_Departed']:
					popuperror = 'True'
					return render(request, 'addtrip.html', {'form': form, 'popuperror':popuperror})
				if (form.cleaned_data['Date_Returned'] == form.cleaned_data['Date_Departed']) & (form.cleaned_data['Time_Returned'] < form.cleaned_data['Time_Departed']):
					popuperror = 'True'
					return render(request, 'addtrip.html', {'form': form, 'popuperror':popuperror})
				# save data as an instance in a database
				form.save()
				# redirect to trip page
				return redirect('/forms/trip/')
		else:
			# We'll create a blank form if we have a GET
			form = TripForm()
		return render(request, 'addtrip.html', {'form': form})


@login_required(login_url='/')
def addexpense(request):
	current_user = request.user
	active = Trip.objects.get(Is_Active="True", Username=current_user.id)
	return render(request, 'addexpenses.html', {'active': active})

@login_required(login_url='/')
def addmeal(request):
	# if this is a post request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = MealForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			current_user = request.user
			active = Trip.objects.get(Is_Active = "True", Username=current_user.id)
			if (form.cleaned_data['Date'] < active.Date_Departed) | (form.cleaned_data['Date'] > active.Date_Returned):
				popuperror = 'True'
				return render(request, 'addmeal.html', {'form': form, 'active':active.Trip_ID, 'popuperror':popuperror})
			if Meal.objects.filter(Meal_Category = form.cleaned_data['Meal_Category'], Date = form.cleaned_data['Date']).exists():
				existerror = 'True'
				return render(request, 'addmeal.html', {'form': form, 'active':active.Trip_ID, 'existerror':existerror})
			if ((form.cleaned_data['Cost'] < 0) | (form.cleaned_data['Tip'] < 0)):
				zeroerror = 'True'
				return render(request, 'addmeal.html', {'form': form, 'active':active.Trip_ID, 'zeroerror': zeroerror})
			if (form.cleaned_data['Tip'] > (form.cleaned_data['Cost'] * 0.2)):
				tiperror = 'True'
				return render(request, 'addmeal.html', {'form': form, 'active':active.Trip_ID, 'tiperror': tiperror})
			# save data as an instance in a database
			form.save()
			# reply with thank you, offer them a chance to enter again
			return redirect('/forms/trip/')
			# return HttpResponse('Thank you! <a href="/forms/trip/">Return</a>')
		# else:
		# 	return HttpResponse('nope')
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
			current_user = request.user
			active = Trip.objects.get(Is_Active = "True", Username=current_user.id)
			if (form.cleaned_data['Date'] < active.Date_Departed) | (form.cleaned_data['Date'] > active.Date_Returned):
				popuperror = 'True'
				return render(request, 'personalcar.html', {'form': form, 'active':active.Trip_ID, 'popuperror':popuperror})
			if form.cleaned_data['Cost'] < 0:
				zeroerror = 'True'
				return render(request, 'personalcar.html', {'form': form, 'active':active.Trip_ID, 'zeroerror': zeroerror})
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
			current_user = request.user
			active = Trip.objects.get(Is_Active = "True", Username=current_user.id)
			if (form.cleaned_data['Date'] < active.Date_Departed) | (form.cleaned_data['Date'] > active.Date_Returned):
				popuperror = 'True'
				return render(request, 'transportation.html', {'form': form, 'active':active.Trip_ID, 'popuperror':popuperror})
			if form.cleaned_data['Cost'] < 0:
				zeroerror = 'True'
				return render(request, 'transportation.html', {'form': form, 'active':active.Trip_ID, 'zeroerror': zeroerror})
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
			current_user = request.user
			active = Trip.objects.get(Is_Active = "True", Username=current_user.id)
			if (form.cleaned_data['Date'] < active.Date_Departed) | (form.cleaned_data['Date'] > active.Date_Returned):
				popuperror = 'True'
				return render(request, 'dailyexpenses.html', {'form': form, 'active':active.Trip_ID, 'popuperror':popuperror})
			if DailyExpenses.objects.filter(Category = form.cleaned_data['Category'], Date = form.cleaned_data['Date']).exists():
				existerror = 'True'
				return render(request, 'dailyexpenses.html', {'form': form, 'active':active.Trip_ID, 'existerror':existerror})
			if form.cleaned_data['Cost'] < 0:
				zeroerror = 'True'
				return render(request, 'dailyexpenses.html', {'form': form, 'active':active.Trip_ID, 'zeroerror': zeroerror})
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
			current_user = request.user
			active = Trip.objects.get(Is_Active = "True", Username=current_user.id)
			if (form.cleaned_data['Date'] < active.Date_Departed) | (form.cleaned_data['Date'] > active.Date_Returned):
				popuperror = 'True'
				return render(request, 'miscellaneous.html', {'form': form, 'active':active.Trip_ID, 'popuperror':popuperror})
			if form.cleaned_data['Cost'] < 0:
					zeroerror = 'True'
					return render(request, 'miscellaneous.html', {'form': form, 'active':active.Trip_ID, 'zeroerror': zeroerror})
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
			current_user = request.user
			active = Trip.objects.get(Is_Active = "True", Username=current_user.id)
			if (form.cleaned_data['Date'] < active.Date_Departed) | (form.cleaned_data['Date'] > active.Date_Returned):
				popuperror = 'True'
				return render(request, 'registrationfees.html', {'form': form, 'active':active.Trip_ID, 'popuperror':popuperror})
			if form.cleaned_data['Cost'] < 0:
				zeroerror = 'True'
				return render(request, 'registrationfees.html', {'form': form, 'active':active.Trip_ID, 'zeroerror': zeroerror})
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
	name = "All Trips for " + current_user.first_name
	none = "No Trips for " + current_user.first_name
	if Trip.objects.filter(Is_Active=True, Username = current_user.id).exists():
		trip = Trip.objects.get(Is_Active = True, Username = current_user.id)
		trips = Trip.objects.filter(Username = current_user.id).order_by('-Trip_ID')
		return render(request, 'triplist.html', {'trips': trips, 'trip': trip, 'name': name})
	else:
		place = 'None'
		na = 'N/A'
		trips = Trip.objects.filter(Username = current_user.id).order_by('-Trip_ID')
		return render(request, 'triplist.html', {'trips': trips, 'none': none, 'place': place, 'na': na})

@login_required(login_url='/')
def reportlist(request):
	current_user = request.user
	name = "All Trips for " + current_user.first_name
	none = "No Trips for " + current_user.first_name
	if Trip.objects.filter(Username = current_user.id).exists():
		trips = Trip.objects.filter(Username = current_user.id).order_by('-Trip_ID')
		return render(request, 'reportlist.html', {'trips': trips, 'trip': trip, 'name': name})
	else:
		place = 'None'
		na = 'N/A'
		return render(request, 'reportlist.html', {'place': place, 'na': na, 'none': none})


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
			if form.cleaned_data['Date_Returned'] < form.cleaned_data['Date_Departed']:
				popuperror = 'True'
				return render(request, 'edittrip.html', {'form': form, 'popuperror':popuperror})
			if (form.cleaned_data['Date_Returned'] == form.cleaned_data['Date_Departed']) & (form.cleaned_data['Time_Returned'] < form.cleaned_data['Time_Departed']):
				popuperror = 'True'
				return render(request, 'edittrip.html', {'form': form, 'popuperror':popuperror})
			instance = form.save(commit=False)
			instance.Trip_ID = active.Trip_ID
			form.save()
			return redirect('/forms/triplist/')
		else:
			return HttpResponse('nope')
	else:
		edit = 'True'
		my_record = Trip.objects.get(Trip_ID = active.Trip_ID)
		form = TripForm(instance=my_record)
		return render(request, 'edittrip.html', {'form' : form, 'edit':edit})

@login_required(login_url='/')
def editexpense(request):
	current_user = request.user
	active = Trip.objects.get(Is_Active=True, Username = current_user.id)
	inst = request.GET.get('category',"")
	ins = str(inst)
	# if not request.GET.get('id',""):
	# 	return redirect('/forms/expenselist/')
	post_id = request.GET.get('id',"")
	edit = "True"


	if request.method == "POST":
		if request.POST.get("PCategory", "") == 'Meal':
			form = MealForm(request.POST)
			if form.is_valid():
				if (form.cleaned_data['Date'] < active.Date_Departed) | (form.cleaned_data['Date'] > active.Date_Returned):
					popuperror = 'True'
					mealid = request.POST.get("Meal_ID", "")
					meal = Meal.objects.get(Meal_ID = mealid)
					record = Meal.objects.get(Meal_ID =meal.Meal_ID)
					form = MealForm(instance = record)
					return render(request, 'addmeal.html', {'form' : form, 'edit' : edit, 'record' : record.Meal_ID, 'active' : active.Trip_ID, 'popuperror':popuperror})
				if Meal.objects.filter(Meal_Category = form.cleaned_data['Meal_Category'], Date = form.cleaned_data['Date']).exists():
					test = Meal.objects.get(Meal_Category = form.cleaned_data['Meal_Category'], Date = form.cleaned_data['Date']).Meal_ID
					mealid = request.POST.get("Meal_ID", "")
					meal = Meal.objects.get(Meal_ID = mealid)
					record = Meal.objects.get(Meal_ID =meal.Meal_ID)
					if test != record.Meal_ID:
						existerror = 'True'
						form = MealForm(instance = record)
						return render(request, 'addmeal.html', {'form': form, 'edit' : edit, 'record' : record.Meal_ID, 'active':active.Trip_ID, 'existerror':existerror, 'test':test})
					mealid = request.POST.get("Meal_ID", "")
					instance = form.save(commit=False)
					meal = Meal.objects.get(Meal_ID = mealid)
					instance.Trip_ID = meal.Trip_ID
					instance.post_ptr_id = meal.post_ptr_id
					instance.Meal_ID = meal.Meal_ID
					form.save()
					return redirect('/forms/expenselist/')
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
				if (form.cleaned_data['Date'] < active.Date_Departed) | (form.cleaned_data['Date'] > active.Date_Returned):
					popuperror = 'True'
					financialid = request.POST.get("Financial_ID", "")
					finance = Financial.objects.get(Financial_ID = financialid)
					record = Financial.objects.get(Financial_ID =finance.Financial_ID)
					form = FinancialForm(instance = record)
					return render(request, 'addfinancial.html', {'form' : form, 'edit' : edit, 'record' : record.Financial_ID, 'active' : active.Trip_ID, 'popuperror':popuperror})
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
				if (form.cleaned_data['Date'] < active.Date_Departed) | (form.cleaned_data['Date'] > active.Date_Returned):
					popuperror = 'True'
					dailyexpenseid = request.POST.get("DailyExpense_ID", "")
					daily = DailyExpenses.objects.get(DailyExpense_ID = dailyexpenseid)
					record = DailyExpenses.objects.get(DailyExpense_ID =daily.DailyExpense_ID)
					form = DailyExpensesForm(instance = record)
					return render(request, 'dailyexpenses.html', {'form' : form, 'edit' : edit, 'record' : record.DailyExpense_ID, 'active' : active.Trip_ID, 'popuperror':popuperror})
				if DailyExpenses.objects.filter(Category = form.cleaned_data['Category'], Date = form.cleaned_data['Date']).exists():
					test = DailyExpenses.objects.get(Category = form.cleaned_data['Category'], Date = form.cleaned_data['Date']).DailyExpense_ID
					dailyexpenseid = request.POST.get("DailyExpense_ID", "")
					daily = DailyExpenses.objects.get(DailyExpense_ID = dailyexpenseid)
					record = DailyExpenses.objects.get(DailyExpense_ID =daily.DailyExpense_ID)
					if test != record.DailyExpense_ID:
						existerror = 'True'
						form = DailyExpensesForm(instance = record)
						return render(request, 'dailyexpenses.html', {'form': form, 'edit' : edit, 'record' : record.DailyExpense_ID, 'active':active.Trip_ID, 'existerror':existerror})
					dailyexp = request.POST.get("DailyExpense_ID", "")
					instance = form.save(commit=False)
					daily = DailyExpenses.objects.get(DailyExpense_ID = dailyexp)
					instance.Trip_ID = daily.Trip_ID
					instance.post_ptr_id = daily.post_ptr_id
					instance.DailyExpense_ID = daily.DailyExpense_ID
					form.save()
					return redirect('/forms/expenselist/')
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
				if (form.cleaned_data['Date'] < active.Date_Departed) | (form.cleaned_data['Date'] > active.Date_Returned):
					popuperror = 'True'
					registrationid = request.POST.get("RegistrationFee_ID", "")
					reg = RegistrationFees.objects.get(RegistrationFee_ID = registrationid)
					record = RegistrationFees.objects.get(RegistrationFee_ID =reg.RegistrationFee_ID)
					form = RegistrationFeesForm(instance = record)
					return render(request, 'registrationfees.html', {'form' : form, 'edit' : edit, 'record' : record.RegistrationFee_ID, 'active' : active.Trip_ID, 'popuperror':popuperror})
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
				if (form.cleaned_data['Date'] < active.Date_Departed) | (form.cleaned_data['Date'] > active.Date_Returned):
					popuperror = 'True'
					transpotationid = request.POST.get("Transportation_ID", "")
					transport = Transportation.objects.get(Transportation_ID = transpotationid)
					record = Transportation.objects.get(Transportation_ID =transport.Transportation_ID)
					form = TransportationForm(instance = record)
					return render(request, 'transportation.html', {'form' : form, 'edit' : edit, 'record' : record.Transportation_ID, 'active' : active.Trip_ID, 'popuperror':popuperror})
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
				if (form.cleaned_data['Date'] < active.Date_Departed) | (form.cleaned_data['Date'] > active.Date_Returned):
					popuperror = 'True'
					miscid = request.POST.get("Miscellaneous_ID", "")
					misc = Miscellaneous.objects.get(Miscellaneous_ID = miscid)
					record = Miscellaneous.objects.get(Miscellaneous_ID =misc.Miscellaneous_ID)
					form = MiscellaneousForm(instance = record)
					return render(request, 'miscellaneous.html', {'form' : form, 'edit' : edit, 'record' : record.Miscellaneous_ID, 'active' : active.Trip_ID, 'popuperror':popuperror})
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
				if (form.cleaned_data['Date'] < active.Date_Departed) | (form.cleaned_data['Date'] > active.Date_Returned):
					popuperror = 'True'
					personalid = request.POST.get("PersonalCar_ID", "")
					percar = PersonalCar.objects.get(PersonalCar_ID = personalid)
					record = PersonalCar.objects.get(PersonalCar_ID =percar.PersonalCar_ID)
					form = PersonalCarForm(instance = record)
					return render(request, 'personalcar.html', {'form' : form, 'edit' : edit, 'record' : record.PersonalCar_ID, 'active' : active.Trip_ID, 'popuperror':popuperror})
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
		elif ins == "Miscellaneous":
			mis = Miscellaneous.objects.get(post_ptr_id = post_id)
			record = Miscellaneous.objects.get(Miscellaneous_ID = mis.Miscellaneous_ID)
			form = MiscellaneousForm(instance = record)
			return render(request, 'miscellaneous.html', {'form' : form, 'edit' : edit, 'record' : record.Miscellaneous_ID, 'active' : active.Trip_ID})
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
	else:
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
			current_user = request.user
			active = Trip.objects.get(Is_Active = "True", Username=current_user.id)
			if (form.cleaned_data['Date'] < active.Date_Departed) | (form.cleaned_data['Date'] > active.Date_Returned):
				popuperror = 'True'
				return render(request, 'addfinancial.html', {'form': form, 'active':active.Trip_ID, 'popuperror':popuperror})
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

@login_required(login_url='/')
def pdf(request):
	current_user = request.user
	id = request.GET.get('id','')
	active = Trip.objects.get(Trip_ID = id, Username=current_user.id)
	date1 = active.Date_Departed
	date2 = active.Date_Returned
	date3 = abs((date2-date1).days)
	date_list = [date1 + timedelta(days=x) for x in range(0, 7)]
	breakfast_costs = [0]*7
	breakfast_total = Meal.objects.filter(Trip_ID_id = active.Trip_ID, Meal_Category="Breakfast").aggregate(Sum('Cost'))
	lunch_costs = [0]*7
	lunch_total = Meal.objects.filter(Trip_ID_id = active.Trip_ID, Meal_Category="Lunch").aggregate(Sum('Cost'))
	dinner_costs = [0]*7
	dinner_total = Meal.objects.filter(Trip_ID_id = active.Trip_ID, Meal_Category="Dinner").aggregate(Sum('Cost'))
	day_total = [0]*7
	meal_total = Meal.objects.filter(Trip_ID_id = active.Trip_ID).aggregate(Sum('Cost'))
	lodging_costs = [0]*7
	lodging_total = DailyExpenses.objects.filter(Trip_ID_id = active.Trip_ID, Category="Lodging").aggregate(Sum('Cost'))
	if Meal.objects.filter(Trip_ID_id=active.Trip_ID).exists():
		if DailyExpenses.objects.filter(Trip_ID_id = active.Trip_ID, Category="Lodging").exists():
			meal_and_lodging = meal_total['Cost__sum'] + lodging_total['Cost__sum']
		else:
			meal_and_lodging = meal_total['Cost__sum']
	else:
		if DailyExpenses.objects.filter(Trip_ID_id = active.Trip_ID, Category="Lodging").exists():
			meal_and_lodging = lodging_total['Cost__sum']
		else:
			meal_and_lodging = 0.00;
	mealtips = [0]*7
	other_total = 0
	if Meal.objects.filter(Trip_ID_id = active.Trip_ID).exists():
		tips_total = Meal.objects.filter(Trip_ID_id = active.Trip_ID).aggregate(Sum('Tip'))
		other_total = other_total + tips_total['Tip__sum']
	else:
		tips_total = 0.00
	taxi_costs = [0]*7
	if DailyExpenses.objects.filter(Trip_ID_id = active.Trip_ID, Category="Taxi").exists():
		taxi_total = DailyExpenses.objects.filter(Trip_ID_id = active.Trip_ID, Category="Taxi").aggregate(Sum('Cost'))
		other_total = other_total + taxi_total['Cost__sum']
	else:
		taxi_total = 0.00
	parking_costs = [0]*7
	if DailyExpenses.objects.filter(Trip_ID_id = active.Trip_ID, Category="Parking, Tolls").exists():
		parking_total = DailyExpenses.objects.filter(Trip_ID_id = active.Trip_ID, Category="Parking, Tolls").aggregate(Sum('Cost'))
		other_total = other_total + parking_total['Cost__sum']
	else:
		parking_total = 0.00
	gasoline_costs = [0]*7
	if DailyExpenses.objects.filter(Trip_ID_id = active.Trip_ID, Category="Gasoline").exists():
		gasoline_total = DailyExpenses.objects.filter(Trip_ID_id = active.Trip_ID, Category="Gasoline").aggregate(Sum('Cost'))
		other_total = other_total + gasoline_total['Cost__sum']
	else:
		gasoline_total = 0.00
	businesscall_costs = [0]*7
	if DailyExpenses.objects.filter(Trip_ID_id = active.Trip_ID, Category="Business Calls").exists():
		businesscall_total = DailyExpenses.objects.filter(Trip_ID_id = active.Trip_ID, Category="Business Calls").aggregate(Sum('Cost'))
		other_total = other_total + businesscall_total['Cost__sum']
	else:
		businesscall_total = 0.00

	# other_total = tips_total['Tip__sum'] + taxi_total['Cost__sum'] + parking_total['Cost__sum'] + gasoline_total['Cost__sum'] + businesscall_total['Cost__sum']
	count = 0
	for date in date_list:
		try:
			breakfast = Meal.objects.get(Trip_ID_id = active.Trip_ID, Meal_Category="Breakfast", Date=date)
			cost = breakfast.Cost
			breakfast_costs[count] = float(cost)
			count = count + 1
		except Meal.DoesNotExist:
			count = count + 1
	count = 0
	for date in date_list:
		try:
			lunch = Meal.objects.get(Trip_ID_id = active.Trip_ID, Meal_Category="Lunch", Date=date)
			cost = lunch.Cost
			lunch_costs[count] = float(cost)
			count = count + 1
		except Meal.DoesNotExist:
			count = count + 1
	count = 0
	for date in date_list:
		try:
			dinner = Meal.objects.get(Trip_ID_id = active.Trip_ID, Meal_Category="Dinner", Date=date)
			cost = dinner.Cost
			dinner_costs[count] = float(cost)
			count = count + 1
		except Meal.DoesNotExist:
			count = count + 1
	count = 0
	for date in date_list:
		try:
			day_total[count] = Meal.objects.filter(Trip_ID_id = active.Trip_ID, Date=date).aggregate(Sum('Cost'))
			count = count + 1
		except Meal.DoesNotExist:
			count = count + 1
	count = 0
	for date in date_list:
		try:
			lodging = DailyExpenses.objects.get(Trip_ID_id = active.Trip_ID, Category="Lodging", Date=date)
			cost = lodging.Cost
			lodging_costs[count] = float(cost)
			count = count + 1
		except DailyExpenses.DoesNotExist:
			count = count + 1
	count = 0
	for date in date_list:
		try:
			mealtips[count] = Meal.objects.filter(Trip_ID_id = active.Trip_ID, Date=date).aggregate(Sum('Tip'))
			count = count + 1
		except Meal.DoesNotExist:
			count = count + 1
	count = 0
	for date in date_list:
		try:
			taxi = DailyExpenses.objects.get(Trip_ID_id = active.Trip_ID, Category="Taxi", Date=date)
			cost = taxi.Cost
			taxi_costs[count] = float(cost)
			count = count + 1
		except DailyExpenses.DoesNotExist:
			count = count + 1
	count = 0
	for date in date_list:
		try:
			parking = DailyExpenses.objects.get(Trip_ID_id = active.Trip_ID, Category="Parking, Tolls", Date=date)
			cost = parking.Cost
			parking_costs[count] = float(cost)
			count = count + 1
		except DailyExpenses.DoesNotExist:
			count = count + 1
	count = 0
	for date in date_list:
		try:
			gasoline = DailyExpenses.objects.get(Trip_ID_id = active.Trip_ID, Category="Gasoline", Date=date)
			cost = gasoline.Cost
			gasoline_costs[count] = float(cost)
			count = count + 1
		except DailyExpenses.DoesNotExist:
			count = count + 1
	count = 0
	for date in date_list:
		try:
			businesscall = DailyExpenses.objects.get(Trip_ID_id = active.Trip_ID, Category="Business Calls", Date=date)
			cost = businesscall.Cost
			businesscall_costs[count] = float(cost)
			count = count + 1
		except DailyExpenses.DoesNotExist:
			count = count + 1
	mis = Miscellaneous.objects.filter(Trip_ID_id = active.Trip_ID).order_by("-Date")[:2]
	mis1 = Miscellaneous.objects.filter(Trip_ID_id = active.Trip_ID).order_by("-Date")[2:4]
	mis2 = Miscellaneous.objects.filter(Trip_ID_id = active.Trip_ID).order_by("-Date")[4:6]
	mis3 = Miscellaneous.objects.filter(Trip_ID_id = active.Trip_ID).order_by("Date")[6:]
	recentcar = PersonalCar.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-PersonalCar_ID')[:1]
	recentcar1 = PersonalCar.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-PersonalCar_ID')[1:2]
	recentcar2 = PersonalCar.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-PersonalCar_ID')[2:3]
	recentcar3 = PersonalCar.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-PersonalCar_ID')[3:4]
	recentcar4 = PersonalCar.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-PersonalCar_ID')[4:5]
	recentcar5 = PersonalCar.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-PersonalCar_ID')[5:6]
	recentcar6 = PersonalCar.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-PersonalCar_ID')[6:7]
	recentcar7 = PersonalCar.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-PersonalCar_ID')[7:8]
	conf = RegistrationFees.objects.filter(Trip_ID_id = active.Trip_ID, Category = "Conference Fees").aggregate(Sum('Cost'))
	banq = RegistrationFees.objects.filter(Trip_ID_id = active.Trip_ID, Category = "Banquet Fees").aggregate(Sum('Cost'))
	dues = RegistrationFees.objects.filter(Trip_ID_id = active.Trip_ID, Category = "Dues").aggregate(Sum('Cost'))
	airfare = Transportation.objects.filter(Trip_ID_id = active.Trip_ID, Category = "Airfare").aggregate(Sum('Cost'))
	rental_car = Transportation.objects.filter(Trip_ID_id = active.Trip_ID, Category = "Rental Car").aggregate(Sum('Cost'))
	bus_train = Transportation.objects.filter(Trip_ID_id = active.Trip_ID, Category = "Bus/Train").aggregate(Sum('Cost'))
	pertotal = PersonalCar.objects.filter(Trip_ID_id = active.Trip_ID).aggregate(Sum('Cost'))
	missum = Miscellaneous.objects.filter(Trip_ID_id = active.Trip_ID).aggregate(Sum('Cost'))
	regtotal = RegistrationFees.objects.filter(Trip_ID_id = active.Trip_ID).aggregate(Sum('Cost'))
	expense_total = meal_and_lodging + other_total
	cos = Financial.objects.filter(Trip_ID_id = active.Trip_ID, Category = "Cost Center").order_by('-Date')[:1]
	into = Financial.objects.filter(Trip_ID_id = active.Trip_ID, Category = "Internal Order").order_by('-Date')[:1]
	cos1 = Financial.objects.filter(Trip_ID_id = active.Trip_ID, Category = "Cost Center").order_by('-Date')[1:2]
	into1 = Financial.objects.filter(Trip_ID_id = active.Trip_ID, Category = "Internal Order").order_by('-Date')[1:2]
	cos2 = Financial.objects.filter(Trip_ID_id = active.Trip_ID, Category = "Cost Center").order_by('-Date')[2:3]
	into2 = Financial.objects.filter(Trip_ID_id = active.Trip_ID, Category = "Internal Order").order_by('-Date')[2:3]
	if Transportation.objects.filter(Trip_ID_id = active.Trip_ID).exists():
		expense_total = expense_total + Transportation.objects.filter(Trip_ID_id = active.Trip_ID).aggregate(Sum('Cost'))['Cost__sum']
	if PersonalCar.objects.filter(Trip_ID_id = active.Trip_ID).exists():
		expense_total = expense_total + pertotal['Cost__sum']
	if RegistrationFees.objects.filter(Trip_ID_id = active.Trip_ID).exists():
		expense_total = expense_total + regtotal['Cost__sum']
	if Miscellaneous.objects.filter(Trip_ID_id = active.Trip_ID).exists():
		expense_total = expense_total + missum['Cost__sum']
	return render(request, 'expensepages.htm', {'current_user': current_user, 'active': active, 'date_list': date_list, 'breakfast_costs': breakfast_costs, 'lunch_costs':lunch_costs, 'dinner_costs': dinner_costs, 'day_total': day_total, 'breakfast_total': breakfast_total, 'lunch_total': lunch_total, 'dinner_total': dinner_total, 'lodging_costs': lodging_costs, 'lodging_total': lodging_total, 'meal_total': meal_total, 'meal_and_lodging': meal_and_lodging, 'mealtips': mealtips, 'taxi_costs': taxi_costs, 'tips_total':tips_total, 'taxi_total':taxi_total, 'parking_costs': parking_costs, 'parking_total': parking_total, 'gasoline_costs':gasoline_costs, 'gasoline_total':gasoline_total, 'businesscall_costs':businesscall_costs, 'businesscall_total':businesscall_total, 'other_total': other_total, 'missum': missum, 'pertotal': pertotal, 'regtotal': regtotal, 'dues': dues, 'conf': conf, 'banq': banq, 'mis': mis, 'mis1' : mis1, 'mis2': mis2, 'mis3': mis3, 'recentcar': recentcar, 'airfare': airfare, 'rental_car': rental_car, 'bus_train': bus_train, 'recentcar1': recentcar1 , 'recentcar2': recentcar2 , 'recentcar3': recentcar3 , 'recentcar4': recentcar4 , 'recentcar5': recentcar5 , 'recentcar6': recentcar6 , 'recentcar7': recentcar7, 'expense_total': expense_total, 'cos':cos, 'into':into, 'cos1':cos1,'into1':into1,'cos2':cos2,'into2':into2})
