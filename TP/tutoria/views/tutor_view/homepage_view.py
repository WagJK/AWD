from django.shortcuts import render_to_response
from ...models import Tutor

def homepage(request):
    tutor = Tutor.objects.get(user=request.user)
    return render_to_response('tutoria/tutor/homepage.html',locals())