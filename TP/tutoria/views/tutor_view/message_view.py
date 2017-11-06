from django.shortcuts import render_to_response
from ...models import Tutor, Confirmation

def confirmation (request):

    requestingTutor = Tutor.objects.get(user=request.user)
    all_confirmations = Confirmation.clientGetAllConfirmations(requestingTutor)

    output = reversed(all_confirmations)
    return render_to_response('tutoria/tutor/tutor_confirmation.html', locals())