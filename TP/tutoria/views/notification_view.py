from django.shortcuts import render_to_response
from django.http import HttpResponse
from tutoria.operations import *


def notification(request):
    notifications = get_all_notification(request.user)
    return render_to_response('tutoria/notification.html', locals())

def clearUnread(request):
	notifications = get_all_notification(request.user)
	notifications.update(unread=False)
	return HttpResponse("success")

def getNumOfUnreadNotf(request):
	num_unread_notf = len(Notification.objects.filter(
		user = request.user,
		unread = True,
	))
	return HttpResponse(str(num_unread_notf))