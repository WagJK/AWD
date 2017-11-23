from ...operations import*
from django.http import HttpResponse
from django.shortcuts import render_to_response

def wallet(request):
    student = Student.objects.get(user=request.user)
    transaction_history = get_all_transaction_record(student)

    return render_to_response('tutoria/student/wallet.html', locals())


def addValue(request):
    student = Student.objects.get(user=request.user)
    student.balance = student.balance + int(request.POST['value'])
    student.save()
    return HttpResponse(student.balance)
