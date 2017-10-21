from django.shortcuts import render_to_response,render
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User, Group
from . import user_view

from django.views.decorators.csrf import csrf_protect, csrf_exempt

def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return
        else:
            return render_to_response('tutoria/login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            return user_view.homepage(request)
        else:
            return render_to_response('tutoria/login.html')

def registrate(request):
    username = request.POST['username']
    password = request.POST['password']
    user = User.objects.create_user(
        username=username, password=password
    )
    return render_to_response('tutoria/login.html')