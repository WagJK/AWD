from django.shortcuts import render_to_response,render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from . import user_view
from ..models import Student

def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return user_view.homepage(request)
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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(
            username=username, password=password
        )
        #g = Group.objects.get(name='Student')
        #g.user_set.add(user)
        Student.objects.create(user=user)
        return render_to_response('tutoria/login.html')
    else:
        return render_to_response('tutoria/registration.html')

@login_required
def logout(request):
    auth.logout(request)
    return render_to_response('tutoria/login.html')