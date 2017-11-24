from tutoria.operations import *
from django.http import HttpResponse
from django.shortcuts import render_to_response

def wallet(request):
    transaction_history = get_all_transaction_record(request.user)
    return render_to_response('tutoria/wallet.html', locals())

def addValue(request):
    student = Student.objects.get(user=request.user)
    student.balance = student.balance + int(request.POST['value'])
    student.save()
    return HttpResponse(student.balance)
	
def withdraw(request):
    tutor = Tutor.objects.get(user=request.user)
    if (tutor.balance - int(request.POST['value']) >= 0):
        tutor.balance = tutor.balance - int(request.POST['value'])
    else:
        tutor.balance = 0
    tutor.save()
    return HttpResponse(tutor.balance)
