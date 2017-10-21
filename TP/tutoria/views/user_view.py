from django.shortcuts import render_to_response
from django.http import HttpResponse

def test(request):
    return render_to_response('tutoria/home.html')