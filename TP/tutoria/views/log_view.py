from django.shortcuts import render_to_response
from django.http import HttpResponse
from . import user_view
def login(request):
    return render_to_response('tutoria/login.html')