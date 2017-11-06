from ...models import Tutor
from django.http import HttpResponse


def withdraw(request):
    requestingTutor = Tutor.objects.get(user=request.user)
    if (requestingTutor.balance - int(request.POST['value']) >= 0):
        requestingTutor.balance = requestingTutor.balance - int(request.POST['value'])
    else:
        requestingTutor.balance = 0
    requestingTutor.save()

    return HttpResponse(requestingTutor.balance)