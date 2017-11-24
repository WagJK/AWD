from django.shortcuts import render_to_response
from ...models import Tutor, Message, Notification, Course, Tag

def homepage(request):
	tutor = Tutor.objects.get(user=request.user)
	num_unread_notf = len(Notification.objects.filter(
		user = request.user,
		unread = True,
	))
	num_unread_msg = len(Message.objects.filter(
		receiver = request.user,
		unread = True,
	))
	courses = Course.objects.filter(tutor=tutor)
	tags = Tag.objects.filter(tutor=tutor)
	return render_to_response('tutoria/tutor/homepage.html',locals())