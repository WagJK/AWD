from django.shortcuts import render_to_response
from .. models import Student
def homepage(request):
    student = Student.objects.get(user=request.user)
    return render_to_response('tutoria/home.html',locals())