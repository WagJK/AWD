from ...models import Student, Tutor
from django.http import HttpResponse


def addValue(request):

    requestingStudent = Student.objects.get(user=request.user)
    requestingTutor = Tutor.objects.get(user=request.user)

    requestingStudent.balance += int(request.POST['value'])
    requestingTutor.balance += int(request.POST['value'])

    requestingStudent.save()
    requestingTutor.save()

    return HttpResponse(requestingStudent.balance)


def withdraw(request):

    requestingStudent = Student.objects.get(user=request.user)
    requestingTutor = Tutor.objects.get(user=request.user)

    if (requestingTutor.balance - int(request.POST['value']) >= 0):
        requestingTutor.balance -= int(request.POST['value'])
        requestingStudent.balance -= int(request.POST['value'])

    else:
        requestingTutor.balance = 0
        requestingStudent.balance = 0

    requestingTutor.save()
    requestingStudent.save()

    return HttpResponse(requestingTutor.balance)
