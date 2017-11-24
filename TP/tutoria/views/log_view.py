from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import re
#import from self defined packages
from .student_view import homepage_view as student_homepage_view
from .tutor_view import homepage_view as tutor_homepage_view
from .both_view import homepage_view as both_homepage_view
from ..models import Tutor, Student, TutorProfile

validReg = True
error_message = ""

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
    elif isTutor:
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
            else:
                return HttpResponseRedirect('/admin')
        #simply request login page
        else:
            return render_to_response('tutoria/login.html',{'wrong_password':False, 'invalid_user':False,'reg_success':False})
    #if POST method
    else:
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
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
                return render_to_response('tutoria/login.html',{'wrong_password':True, 'invalid_user':False, 'reg_success':False})
        else:
            return render_to_response('tutoria/login.html', {'wrong_password':False, 'invalid_user':True, 'reg_success':False})

def registrate(request):
    global validReg
    validReg = True
    global error_message
    error_message = ""
    if request.method == 'POST':
        #create a user
        username = request.POST['username']
        usernameCheck(username)
        
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        passwordCheck(password, confirmpassword)
        
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        phone = request.POST['phone']

        if validReg:
            user = User.objects.create_user(
                username=username, password=password, email=email, first_name=firstname, last_name=lastname
            )
        else:
            university = TutorProfile.objects.values_list('university',flat=True).distinct()
            return render_to_response('tutoria/registration.html', {'error_message': error_message, 'flag':True, 'university_list':university})
        #create a corresponding type object
        usr_type = request.POST['type']
        if usr_type == 'student':       
            Student.objects.create(user=user, login_type='Student',phone=phone)
        elif usr_type == 'tutor':
            university = request.POST['university']
            tutortype = request.POST['tutortype']
            if tutortype == 'private':
                hourly_rate = request.POST['hourlyrate']
                tempProfile = TutorProfile.objects.create(university=university, hourly_rate=hourly_rate)
            else:
                tempProfile = TutorProfile.objects.create(university=university, hourly_rate=0)
            Tutor.objects.create(user=user, login_type='Tutor', tutor_type=tutortype, profile=tempProfile, phone=phone)
        elif usr_type == 'both':
            Student.objects.create(user=user, login_type='Student',phone=phone)
            university = request.POST['university']
            tutortype = request.POST['tutortype']
            if tutortype == 'private':
                hourly_rate = request.POST['hourlyrate']
                tempProfile = TutorProfile.objects.create(university=university, hourly_rate=hourly_rate)
            else:
                tempProfile = TutorProfile.objects.create(university=university, hourly_rate=0)
            Tutor.objects.create(user=user, login_type='Tutor', tutor_type=tutortype, profile=tempProfile, phone=phone)

        return render_to_response('tutoria/login.html',{'wrong_password':False, 'invalid_user':False, 'reg_success':True})
    # if request registration
    else:
        university = TutorProfile.objects.values_list('university',flat=True).distinct()
        return render_to_response('tutoria/registration.html',{'university_list':university})

@login_required
def logout(request):
    auth.logout(request)
    return render_to_response('tutoria/login.html',{'wrong_password':False, 'invalid_user':False, 'reg_success':False})

def usernameCheck(username):
    global error_message
    global validReg

    if User.objects.filter(username=username).exists():
        error_message += "duplicate username "
        validReg = False

def passwordCheck(password,confirmpassword):
    global error_message
    global validReg
    '''
    if len(password) < 8:
        error_message += "password length less than 8, "
        validReg = False
    
    if re.search(r"\d", password) is None:
        error_message += "password has no digit, "
        validReg = False
    
    if re.search(r"[A-Z]", password) is None:
        error_message += "password has no uppercase letter, "
        validReg = False
    
    if re.search(r"[a-z]", password) is None:
        error_message += "password has no lowercase letter, "
        validReg = False
    
    if re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is not None:
        error_message += "password has invalid symbol, "
        validReg = False
        '''
    
    if not password == confirmpassword:
        error_message += "password doesnot match with confirmpassword "
        validReg = False
