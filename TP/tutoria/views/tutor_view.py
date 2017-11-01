from django.shortcuts import render_to_response
from ..models import Tutor, Timeslot, Student
from django.http import HttpResponse

def homepage(request):
    tutor = Tutor.objects.get(user=request.user)
    return render_to_response('tutoria/tutor_home.html',locals())