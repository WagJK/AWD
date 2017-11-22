from django.shortcuts import render_to_response
from django.http import HttpResponse
from tutoria.operations import *


def message(request):
    inbox_messages = get_inbox_message(request.user)
    sent_messages = get_sent_message(request.user)
    return render_to_response('tutoria/message.html', locals())

def clearUnread(request):
	inbox_messages = get_inbox_message(request.user)
	inbox_messages.update(unread=False)
	return HttpResponse("success")

def write(request):
	target = User.objects.get(username=request.POST['target'])
	return render_to_response('tutoria/write_message.html', locals())

def send(request):
	target = User.objects.get(username=request.POST['target'])
	content = request.POST['content']
	Message.objects.create(
		unread = True,
		sender = request.user,
		receiver = target,
		content = content,
	)
	return HttpResponse("Message is successfully sent!")