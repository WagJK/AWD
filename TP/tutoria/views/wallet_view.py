from tutoria.operations import *
from django.http import HttpResponse
from django.shortcuts import render_to_response

def wallet(request):
    wallet = Wallet.objects.get(user=request.user)
    transaction_history = get_all_transaction_record(request.user)
    return render_to_response('tutoria/wallet.html', locals())

def addValue(request):
    wallet = Wallet.objects.get(user=request.user)
    wallet.balance = wallet.balance + int(request.POST['value'])
    wallet.save()
    return HttpResponse(wallet.balance)
	
def withdraw(request):
    wallet = Wallet.objects.get(user=request.user)
    if (wallet.balance - int(request.POST['value']) >= 0):
        wallet.balance = wallet.balance - int(request.POST['value'])
    else:
        wallet.balance = 0
    wallet.save()
    return HttpResponse(wallet.balance)
