from django.shortcuts import render_to_response
from django.contrib.auth import update_session_auth_hash
from django.contrib import auth
from django.contrib.auth.models import User
from ...models import Student

DEBUG = True

def editProfile(request):
    if request.method == 'GET':
        student = Student.objects.get(user=request.user)
        return render_to_response('tutoria/student/editProfile.html',locals())
    elif request.method == 'POST':
        student = Student.objects.get(user=request.user)
        #this edit basic info that does not require checks
        first_name = request.POST['firstname']
        if first_name:
            request.user.first_name = first_name
        last_name = request.POST['lastname']
        if last_name:
            request.user.last_name = last_name
        email = request.POST['email']
        if email:
            request.user.email = email
        phone = request.POST['phone']
        if phone:
            student.phone = phone
        username = request.POST['username']
        duplicateUsername = False
        if username:
            if not User.objects.filter(username=username).exists():
                request.user.username = username
            else:
                duplicateUsername = True
        request.user.save()
        student.save()
        
        #perform reset password, need login again.
        old_password = request.POST['oldpassword']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']

        #only perform a reset when user enter 3 passwords
        if old_password and password and confirm_password:
            user = auth.authenticate(username=request.user.username,password=old_password)
            if  user is not None:
                if password == confirm_password:
                    request.user.set_password(password)
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                else:
                    return render_to_response('tutoria/student/editProfile.html',{'duplicateUsername':False,'success':False,'editError':False,'confirmError':True,'student':student})
            else:
                return render_to_response('tutoria/student/editProfile.html', {'duplicateUsername':False,'success':False,'editError':True,'confirmError':False,'student':student})
        if duplicateUsername:
            return render_to_response('tutoria/student/editProfile.html', {'duplicateUsername':True,'success':False,'editError':False,'confirmError':False,'student':student})
        else:
            return render_to_response('tutoria/student/editProfile.html',{'duplicateUsername':False,'success':True,'editError':False,'confirmError':False,'student':student})