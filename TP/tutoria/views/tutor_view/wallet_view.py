from ...models import Tutor
from django.http import HttpResponse
from django.shortcuts import render_to_response

def wallet(request):
	tutor = Tutor.objects.get(user=request.user)

	return render_to_response('tutoria/tutor/wallet.html', locals())

def withdraw(request):
    requestingTutor = Tutor.objects.get(user=request.user)
    if (requestingTutor.balance - int(request.POST['value']) >= 0):
        requestingTutor.balance = requestingTutor.balance - int(request.POST['value'])
    else:
        requestingTutor.balance = 0
    requestingTutor.save()

    return HttpResponse(requestingTutor.balance)