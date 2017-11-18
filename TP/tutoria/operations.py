import logging
from django.db import models
from django.contrib.auth.models import User
from .models import *
from .views.manage_sch import manage

from datetime import datetime
from datetime import date
from datetime import timedelta

def all_booked_timeslots(client):
	try:
		if client.login_type == "Student":
			return Timeslot.objects.filter(is_booked=True, student=client)
	except Timeslot.DoesNotExist:
		return None

def get_booked_timeslots_interval(client, start_date, end_date):
	try:
		if client.login_type == "Student":
			return Timeslot.objects.filter(
				is_booked=True, 
				student=client, 
				startTime__range=(start_date, end_date))
	except Timeslot.DoesNotExist:
		return None

def all_bookable_timeslots(client):
	try:
		if client.login_type == "Tutor":
			return Timeslot.objects.filter(
				bookable=True, 
				is_booked=False, 
				is_finished=False, 
				tutor=client)
	except Timeslot.DoesNotExist:
		return None


def get_bookable_timeslots_interval(client, start_date, end_date):
	try:
		if client.login_type == "Tutor":
			return Timeslot.objects.filter(
				bookable=True,
				is_booked=False, 
				is_finished=False, 
				tutor=client, 
				startTime__range=(start_date, end_date))
	except Timeslot.DoesNotExist:
		return None

def get_all_timeslots_interval(client, start_date, end_date):
	try:
		if client.login_type == "Tutor":
			return Timeslot.objects.filter(
				tutor=client, 
				startTime__range=(start_date, end_date))
	except Timeslot.DoesNotExist:
		return None

def all_cancellable_timeslots(client):
	try:
		if client.login_type == "Student":
			return Timeslot.objects.filter(
				cancellable=True, 
				is_booked=True, 
				student=client)
	except Timeslot.DoesNotExist:
		return None

def all_notification(requestingClient):
	try:
		return Notification.objects.filter(user=requestingClient.user).exclude(category="history").order_by('-createTime', '-id')

	except Notification.DoesNotExist:
		return None


def all_transaction_history(requestingClient):
	try:
		return Notification.objects.filter(category="history", user=requestingClient.user).order_by('-createTime', '-id')

	except Notification.DoesNotExist:
		return None

def createBookNotification(slot, fee):
	studentContent = "You have successfully booked the tutorial session scheduled at "+ str(slot) \
					 + " given by tutor "+ (str)(slot.tutor) + "."
	studentBookNotification = Notification(
		category="book",
		content=studentContent,
		user=slot.student.user,
		fee=fee)
	studentBookNotification.save()
	tutorContent = "Your tutorial session scheduled at "+ str(slot) + " has been booked by student " \
				   + (str)(slot.student) + "."
	tutorBookNotification = Notification(
		category="book",
		content=tutorContent,
		user=slot.tutor.user,
		fee=fee)
	tutorBookNotification.save()
	return

def createCancelNotification(slot, refund):
	studentContent = "You have successfully cancelled the tutorial session scheduled at " + str(slot) \
					 + " given by tutor " + (str)(slot.tutor) + "."
	studentCancelNotification = Notification(
		category="cancel",
		content=studentContent,
		user=slot.student.user,
		fee=refund)
	studentCancelNotification.save()
	tutorContent = "Your tutorial session scheduled at " + str(slot) + " has been cancelled by student " \
				   + (str)(slot.student) + "."
	tutorCancelNotification = Notification(
		category="cancel",
		content=tutorContent,
		user=slot.tutor.user,
		fee=refund)
	tutorCancelNotification.save()
	return

def createTransactionNotification(slot, money, type):
	if money == 0:
		return
	if type == 'book':
		studentContent = (str)(money) + " HKD has been deducted from your wallet."
		studentNotification = Notification(
			category="transaction",
			content=studentContent,
			user=slot.student.user,
			fee=money)
		studentNotification.save()
	elif type == 'cancel':
		studentContent = (str)(money) + " HKD has been returned to your wallet."
		studentNotification = Notification(
			category="transaction",
			content=studentContent,
			user=slot.student.user,
			fee=money)
		studentNotification.save()
	elif type == 'end':
		tutorContent = (str)(money) + " HKD has been transferred to your wallet."
		tutorNotification = Notification(
			category="transaction",
			content=tutorContent,
			user=slot.student.tutor,
			fee=money)
		tutorNotification.save()
	return

def createTransactionHistory (slot, money, type):
	if money == 0:
		return
	usr = User.objects.none()
	status = ""
	studentMoney = tutorMoney = myTutorMoney = 0
	if type == 'book':
		usr = slot.student.user
		status = "Outgoing"
		studentMoney = money
		tutorMoney = money / 1.05
		myTutorMoney = studentMoney - tutorMoney
	elif type == 'cancel':
		usr = slot.student.user
		status = "Incoming"
		studentMoney = money
		tutorMoney = money / 1.05
		myTutorMoney = studentMoney - tutorMoney
	elif type == 'end':
		usr = slot.tutor.user
		status = "Incoming"
		studentMoney = money * 1.05
		tutorMoney = money
		myTutorMoney = money * 0.05
	transferContent = "Amount: " + str(money) + " HKD\n" \
					  + "Status: " + status + "\n" \
					  + "Related Timeslot: " + str(slot) + "\n" \
					  + "Other Parties Involved: "
	if type == 'book':
		transferContent += ("Tutor "+ (str)(slot.tutor) + " (" + str(tutorMoney) + " HKD Pending Income); MyTutors ("
						   + str(myTutorMoney) + " HKD Pending Income)")
	elif type == 'cancel':
		transferContent += ("Tutor " + (str)(slot.tutor) + " (" + str(tutorMoney) + " HKD Pending Refunded); MyTutors ("
							+ str(myTutorMoney) + " HKD Pending Refunded)")
	elif type == 'end':
		transferContent += ("Student " + (str)(slot.student) + " (" + str(studentMoney) + " HKD Paid); MyTutors ("
							+ str(myTutorMoney) + " HKD Received)")
	transactionHistory = Notification(
		category="history",
		content=transferContent,
		user=usr,
		fee=money)
	transactionHistory.save()
	return

def createReviewNotification (slot):
	requestContent = "You are invited to post your review on the ended tutorial session at " + str(slot) \
					 + " conducted by tutor " + (str)(slot.tutor)\
					 + ". Please go to your schedule and find your finished tutorial to make a review."
	reviewNotification = Notification(
		category="review",
		content=requestContent,
		user=slot.student.user)
	reviewNotification.save()
	return

def book(booking_student, timeslot):
	fee = timeslot.fee * 1.05
	if booking_student.balance < fee:
		return False
	manage()
	if not timeslot.bookable:
		return False
	# modify student wallet
	booking_student.balance -= fee
	booking_student.save()
	# modify timeslot status
	timeslot.is_booked = True
	timeslot.bookable = False
	timeslot.cancellable = True
	timeslot.student = booking_student
	timeslot.save()
	# sending notification
	createBookNotification(timeslot, fee)
	createTransactionNotification(timeslot, fee, "book")
	createTransactionHistory(timeslot, fee, "book")
	return True

def cancel(cancelling_student, timeslot):
	refund = timeslot.fee * 1.05
	manage()
	if not timeslot.cancellable:
		return False
	# sending notification
	createCancelNotification(timeslot, refund)
	createTransactionNotification(timeslot, refund, "cancel")
	createTransactionHistory(timeslot, refund, "cancel")
	# modify timeslot status
	timeslot.is_booked = False
	timeslot.bookable = True
	timeslot.cancellable = False
	timeslot.save()
	# modify student wallet
	cancelling_student.balance += refund
	cancelling_student.timeslot_set.remove(timeslot)
	cancelling_student.save()
	return True