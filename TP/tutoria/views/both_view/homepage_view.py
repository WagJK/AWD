from django.shortcuts import render_to_response
from ...models import Tutor, Student

def homepage(request):
    student = Student.objects.get(user=request.user)
    tutor = Tutor.objects.get(user=request.user)
    return render_to_response('tutoria/both/homepage.html',locals())