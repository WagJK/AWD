from django.shortcuts import render_to_response
from tutoria.operations import *


def notification(request):
    notifications = get_all_notification(request.user)
    notifications.update(unread=False);
    return render_to_response('tutoria/notification.html', locals())
