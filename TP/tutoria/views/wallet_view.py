from tutoria.operations import *
from tutoria.models import *
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
    createTransactionRecord(None, int(request.POST['value']), 'add', request.user)
    return HttpResponse(wallet.balance)
	
def withdraw(request):
    wallet = Wallet.objects.get(user=request.user)
    money = 0
    if (wallet.balance - int(request.POST['value']) >= 0):
        wallet.balance = wallet.balance - int(request.POST['value'])
        money = int(request.POST['value'])
    else:
        money = wallet.balance
        wallet.balance = 0
    wallet.save()
    createTransactionRecord(None, money, 'withdraw', request.user)
    return HttpResponse(wallet.balance)
