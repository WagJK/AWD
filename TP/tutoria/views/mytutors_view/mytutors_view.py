from django.shortcuts import render_to_response
from django.http import HttpResponse
from tutoria.models import MyTutors

def homepage(request):
	mytutors = MyTutors.objects.all()[0]
	return render_to_response('tutoria/MyTutors/homepage.html',locals())

def withdraw(request):
    mytutors = MyTutors.objects.all()[0]
    if (mytutors.balance - int(request.POST['value']) >= 0):
        mytutors.balance = mytutors.balance - int(request.POST['value'])
    else:
        mytutors.balance = 0.0
    mytutors.save()
    return HttpResponse(mytutors.balance)
