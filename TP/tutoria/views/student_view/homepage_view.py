from django.shortcuts import render_to_response
from django.http import HttpResponse
from tutoria.models import Student, Message, Notification

def homepage(request):
	student = Student.objects.get(user=request.user)
	num_unread_msg = len(Message.objects.filter(
		receiver = request.user,
		unread = True,
	))
	num_unread_notf = len(Notification.objects.filter(
		user = request.user,
		unread = True,
	))
	return render_to_response('tutoria/student/homepage.html',locals())