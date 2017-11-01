from django.shortcuts import render_to_response
from ..models import Tutor, Timeslot, Student, Confirmation
from django.http import HttpResponse

def homepage(request):
    tutor = Tutor.objects.get(user=request.user)
    return render_to_response('tutoria/tutor_home.html',locals())

def confirmation (request):

    requestingTutor = Tutor.objects.get(user=request.user)
    all_confirmations = Confirmation.clientGetAllConfirmations(requestingTutor)

    output = reversed(all_confirmations)
    return render_to_response('tutoria/tutor_confirmation.html', locals())