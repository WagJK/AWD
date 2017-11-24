from django.shortcuts import render_to_response
from django.http import HttpResponse
from tutoria.models import Student, Tutor, Message, Notification, Course, Tag

def homepage(request):
	student = Student.objects.get(user=request.user)
	tutor = Tutor.objects.get(user=request.user)
	courses = Course.objects.filter(tutor=tutor)
	tags = Tag.objects.filter(tutor=tutor)
	num_unread_msg = len(Message.objects.filter(
		receiver = request.user,
		unread = True,
	))
	num_unread_notf = len(Notification.objects.filter(
		user = request.user,
		unread = True,
	))
	return render_to_response('tutoria/both/homepage.html',locals())