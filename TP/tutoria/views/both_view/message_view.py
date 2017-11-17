from django.shortcuts import render_to_response
from ...operations import *


def confirmation(request):

    requestingStudent = Student.objects.get(user=request.user)
    all_confirmations = all_notification(requestingStudent)

    return render_to_response('tutoria/student/notification.html', locals())
