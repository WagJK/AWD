from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
#import from self defined packages
from .student_view import homepage_view as student_homepage_view
from .tutor_view import homepage_view as tutor_homepage_view
from .both_view import homepage_view as both_homepage_view
from ..models import Tutor, Student

#select login type
def typeSelect(id):   
    isStudent = False
    isTutor = False
    
    if Student.objects.filter(user__pk=id).exists():
        isStudent = True
    if Tutor.objects.filter(user__pk=id).exists():
        isTutor = True
    
    if isStudent:
        if isTutor:
            return 'Both'
        else:
            return 'Student'
    else:
        return 'Tutor'

def login(request):
    #if GET method 
    if request.method == 'GET':
        #user's previous login has not expired
        if request.user.is_authenticated():
            user_type = typeSelect(request.user.id)
            if user_type == 'Student':
                return student_homepage_view.homepage(request)
            elif user_type == 'Tutor':
                return tutor_homepage_view.homepage(request)
            elif user_type == 'Both':
                return both_homepage_view.homepage(request)
        #simply request login page
        else:
            return render_to_response('tutoria/login.html')
    #if POST method
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            user_type = typeSelect(user.id)
            auth.login(request,user)
            if user_type == 'Student':               
                return student_homepage_view.homepage(request)
            elif user_type == 'Tutor':
                return tutor_homepage_view.homepage(request)
            elif user_type == 'Both':
                return both_homepage_view.homepage(request)
        else:
            return render_to_response('tutoria/login.html',{'wrong_password': True})

def registrate(request):
    if request.method == 'POST':
        #create a user
        username = request.POST['username']
        password = request.POST['password']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        user = User.objects.create_user(
            username=username, password=password, email=email, first_name=firstname, last_name=lastname
        )
        #create a corresponding type object
        usr_type = request.POST['type']
        if usr_type == 'student':       
            Student.objects.create(user=user, login_type='Student')
        elif usr_type == 'tutor':
            Tutor.objects.create(user=user, login_type='Tutor')
        elif usr_type == 'both':
            Student.objects.create(user=user, login_type='Student')
            Tutor.objects.create(user=user, login_type='Tutor')

        return render_to_response('tutoria/login.html')
    # if request registration
    else:
        return render_to_response('tutoria/registration.html')

@login_required
def logout(request):
    auth.logout(request)
    return render_to_response('tutoria/login.html')
