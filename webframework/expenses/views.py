from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.contrib.auth import authenticate, login

def index(request):
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return render(request, '../forms/main.html', {})
		else:
			return render(request, 'index.html', {})

