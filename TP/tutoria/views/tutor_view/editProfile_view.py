from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash
from django.contrib import auth,messages
from ...models import Tutor,Tag,Course,TutorProfile

def editProfile(request):
    if request.method == 'GET':
        tutor = Tutor.objects.get(user=request.user)
        tag = Tag.objects.all()
        university_course_list = Course.objects.filter(university=tutor.profile.university)
        tutor_course_list = Course.objects.filter(tutor=tutor)
        all_tags = Tag.objects.all()
        tag_list = Tag.objects.filter(tutor=tutor)
        university_list = TutorProfile.objects.values_list('university',flat=True).distinct()
        return render_to_response('tutoria/tutor/editProfile.html',locals())
    
    elif request.method == 'POST':
        tutor = Tutor.objects.get(user=request.user)
        tutor_course = Course.objects.filter(tutor=tutor)
        tutor_tag = Tag.objects.filter(tutor=tutor)
        
        university_list = TutorProfile.objects.values_list('university',flat=True).distinct()
        university_course_list = Course.objects.filter(university=tutor.profile.university)
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
            tutor.phone = phone
        
        tutor_type = request.POST['tutortype']
        if tutor_type:
            tutor.tutor_type = tutor_type
            if tutor_type == 'Contract':
                tutor.profile.hourly_rate = 0

        hourly_rate = request.POST['hourlyrate']
        if hourly_rate:
            if tutor_type == 'Contract':
                tutor.profile.hourly_rate = 0
            else:
                tutor.profile.hourly_rate = hourly_rate

        university = request.POST['university']
        if university:
            tutor.profile.university = university
        
        biography = request.POST['biography']
        if biography:
            tutor.profile.introduction = biography
        
        temp = request.POST.getlist('course_list[]',[])
        course_list = Course.objects.filter(code__in=temp)
        for course in tutor_course:
            if course in course_list:
                pass
            else:
                tutor.course.remove(course)
        for course in course_list:
            if course in tutor_course:
                pass
            else:
                tutor.course.add(course)

        tmp = request.POST.getlist('tag_list[]',[])
        tag_list = Tag.objects.filter(content__in=tmp)
        for tag in tutor_tag:
            if tag in tag_list:
                pass
            else:
                tutor.tag.remove(tag)
        for tag in tag_list:
            if tag in tutor_tag:
                pass
            else:
                tutor.tag.add(tag) 
        
        username = request.POST['username']
        if username:
            request.user.username = username
        
        request.user.save()
        tutor.profile.save()
        tutor.save()
        
        #perform reset password, need login again.
        old_password = request.POST['oldpassword']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']

        #need for re-render the editProfile.html
        tag = Tag.objects.all()
        university_course_list = Course.objects.filter(university=tutor.profile.university)
        tutor_course_list = Course.objects.filter(tutor=tutor)
        all_tags = Tag.objects.all()
        tag_list = Tag.objects.filter(tutor=tutor)
        university_list = TutorProfile.objects.values_list('university',flat=True).distinct()
        #only perform a reset when user enter 3 passwords
        if old_password and password and confirm_password:
            user = auth.authenticate(username=username,password=old_password)
            if  user is not None:
                if password == confirm_password:
                    request.user.set_password(password)
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                else:
                    success = False
                    editError = False
                    confirmError = True
                    return render_to_response('tutoria/tutor/editProfile.html',locals())
            else:
                success = False
                editError = True
                confirmError = False
                return render_to_response('tutoria/tutor/editProfile.html', locals())
        success = True
        return render_to_response('tutoria/tutor/editProfile.html', locals())
        
        #render_to_response('tutoria/tutor/editProfile.html',{'success':True,'tutor':tutor})


def flushCourse(request):
    tutor = Tutor.objects.get(user=request.user)
    university = request.POST['university']
    university_course_list = Course.objects.filter(university=university)
    tutor_course_list = Course.objects.filter(tutor=tutor)
    return render_to_response('tutoria/tutor/flushCourse.html',locals())