from django.shortcuts import render_to_response
from tutoria.models import Tutor, Confirmation
from tutoria.operations import *

def confirmation (request):

    requestingTutor = Tutor.objects.get(user=request.user)
    all_confirmations = clientGetAllConfirmations(requestingTutor)

    output = reversed(all_confirmations)
    return render_to_response('tutoria/tutor/tutor_confirmation.html', locals())