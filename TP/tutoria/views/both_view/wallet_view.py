from ...models import Student
from django.http import HttpResponse


def addValue(request):
    requestingStudent = Student.objects.get(user=request.user)
    requestingStudent.balance = requestingStudent.balance + int(request.POST['value'])
    requestingStudent.save()

    return HttpResponse(requestingStudent.balance)
