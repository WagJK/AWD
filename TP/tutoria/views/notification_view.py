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