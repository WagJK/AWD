from django.shortcuts import render_to_response
from ...models import Confirmation, Student
from ...operations import *


def confirmation(request):

    requestingStudent = Student.objects.get(user=request.user)
    all_confirmations = Confirmation.clientGetAllConfirmations(requestingStudent)

    output = reversed(all_confirmations)
    return render_to_response('tutoria/student/studentConfirmation.html', locals())
