from django.shortcuts import render_to_response
from ...operations import *

def notification (request):

    requestingTutor = Tutor.objects.get(user=request.user)
    notifications = all_notification(requestingTutor)

    return render_to_response('tutoria/tutor/notification.html', locals())