from django.shortcuts import render_to_response,render
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User, Group
from . import user_view
from ..models import Student

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
            auth.login(request,user)
            return user_view.homepage(request)
        else:
            return render_to_response('tutoria/login.html')

def registrate(request):
    username = request.POST['username']
    password = request.POST['password']
    user = User.objects.create_user(
        username=username, password=password
    )
    g = Group.objects.get(name='Student')
    g.user_set.add(user)
    Student.objects.create(user=user, user_identity='Student')
    return render_to_response('tutoria/login.html')