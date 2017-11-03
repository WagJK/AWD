from django.shortcuts import render_to_response,render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from . import user_view, tutor_view
from ..models import Student,Tutor

def typeSelect(id):
    if Student.objects.filter(user__pk=id).exists():
        #print(Student.objects.filter(user__pk=id).login_type)
        return Student.objects.filter(user__pk=id)[0].login_type
    elif Tutor.objects.filter(user__pk=id).exists():
        #print(Tutor.objects.filter(user__pk=id).login_type)
        return Tutor.objects.filter(user__pk=id)[0].login_type

def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            user_type = typeSelect(request.user.id)
            if user_type == "Student":
                return user_view.homepage(request)
            elif user_type == "Tutor":
                return tutor_view.homepage(request)
        else:
            return render_to_response('tutoria/login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user_type = request.POST['type']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            if user_type == "1":
                auth.login(request,user)
                if Student.objects.filter(user=request.user).exists():
                    return user_view.homepage(request)
                else:
                    return passive_logout(request)
            elif user_type == "2":
                auth.login(request,user)
                if Tutor.objects.filter(user=request.user).exists():
                    return tutor_view.homepage(request)
                else:
                    return passive_logout(request)
        else:
            return render_to_response('tutoria/login.html',{'wrong_password': True, 'wrong_type':False})

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

@login_required
def passive_logout(request):
    auth.logout(request)
    return render_to_response('tutoria/login.html',{'wrong_password': False, 'wrong_type': True})