from django.shortcuts import render_to_response
from ...models import Tutor

def homepage(request):
    print('this is both')
    both = Tutor.objects.get(user=request.user)
    return render_to_response('tutoria/both/homepage.html',locals())