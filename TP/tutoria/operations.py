import logging
from django.db import models
from django.contrib.auth.models import User
from .models import *
from .views.manage_sch import manage

from datetime import datetime
from datetime import date
from datetime import timedelta
from django.core.mail import send_mail
# ==========================================================================
# ========================== Get ===========================================
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

# Added the limit of 30 days before
def get_all_transaction_record(client):
	try:
		currentTime = datetime.now()
		earliestTime = currentTime - timedelta(days=30)
		return TransactionRecord.objects.filter(user=client.user, createTime__gte=earliestTime).order_by('-createTime', '-id')

	except TransactionRecord.DoesNotExist:
		return None
		
# ==========================================================================
# ========================== Messages Related ==============================

def get_inbox_message(user):
	try:
		return Message.objects.filter(receiver=user).order_by('-createTime', '-id')
	except Message.DoesNotExist:
		return None

def get_sent_message(user):
	try:
		return Message.objects.filter(sender=user).order_by('-createTime', '-id')
	except Message.DoesNotExist:
		return None

# ===========================================================================
# ========================== Notifications Related ==========================
def get_all_notification(user):
	try:
		return Notification.objects.filter(user=user).order_by('-createTime', '-id')
	except Notification.DoesNotExist:
		return None

def createBookNotification(slot):
	studentContent = "You have successfully booked the tutorial session scheduled at "+ str(slot) \
					 + " given by tutor "+ (str)(slot.tutor) + "."
	studentBookNotification = Notification(
		category="book",
		content=studentContent,
		user=slot.student.user
	)
	studentBookNotification.save()
	tutorContent = "Your tutorial session scheduled at "+ str(slot) + " has been booked by student " \
				   + (str)(slot.student) + "."
	tutorBookNotification = Notification(
		category="book",
		content=tutorContent,
		user=slot.tutor.user
	)
	tutorBookNotification.save()
	return

def createCancelNotification(slot):
	studentContent = "You have successfully cancelled the tutorial session scheduled at " + str(slot) \
					 + " given by tutor " + (str)(slot.tutor) + "."
	studentCancelNotification = Notification(
		category="cancel",
		content=studentContent,
		user=slot.student.user,
	)
	studentCancelNotification.save()
	tutorContent = "Your tutorial session scheduled at " + str(slot) + " has been cancelled by student " \
				   + (str)(slot.student) + "."
	tutorCancelNotification = Notification(
		category="cancel",
		content=tutorContent,
		user=slot.tutor.user,
	)
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
		)
		studentNotification.save()
	elif type == 'cancel':
		studentContent = (str)(money) + " HKD has been returned to your wallet."
		studentNotification = Notification(
			category="transaction",
			content=studentContent,
			user=slot.student.user,
		)
		studentNotification.save()
	elif type == 'end':
		tutorContent = (str)(money) + " HKD has been transferred to your wallet."
		tutorNotification = Notification(
			category="transaction",
			content=tutorContent,
			user=slot.student.tutor,
		)
		tutorNotification.save()
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

def createTransactionRecord(slot, money, type):
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
	transferContent = "Amount: " + str(money) + " HKD" \
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
	transactionHistory = TransactionRecord(
		content=transferContent,
		user=usr,
		fee=money
	)
	transactionHistory.save()
	return

# ==========================================================================
# ========================== Operations ====================================
def book(booking_student, timeslot):

	manage()
	# one cannot book the timeslot if it is not bookable
	if not timeslot.bookable:
		return "not bookable"

	# one cannot book his own timeslot
	if timeslot.tutor.user.username == booking_student.user.username:
		return "own timeslot"

	# one cannot book two timeslots from one tutor in a day
	start_date = timeslot.startTime.date()
	same_tutor_same_day_timeslots = Timeslot.objects.filter(
		tutor = timeslot.tutor,
		student = booking_student,
		is_booked = True,
		startTime__range = (start_date, start_date + timedelta(days = 1)),
	)
	if (len(same_tutor_same_day_timeslots) > 0):
		return "two timeslots"

	# one cannot book the timeslot if the timeslot is occupied in another booking by the student
	same_start_time_timeslots = Timeslot.objects.filter(
		student = booking_student,
		is_booked = True,
		startTime = timeslot.startTime,
	)
	same_end_time_timeslots = Timeslot.objects.filter(
		student = booking_student,
		is_booked = True,
		endTime = timeslot.endTime,
	)
	if (len(same_start_time_timeslots) > 0 or len(same_end_time_timeslots) > 0):
		return "timeslot occupied"

	# one cannot book if he doesn't have enough money
	fee = timeslot.fee * 1.05
	if booking_student.balance < fee:
		return "insufficient balance"

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
	createBookNotification(timeslot)
	createTransactionNotification(timeslot, fee, "book")
	createTransactionRecord(timeslot, fee, "book")

	# sending email
	send_mail(
		'Tutoria Booking Notification',
		"Your tutorial session scheduled at " + str(timeslot) + " has been booked by student " + (str)(timeslot.student) + ".",
		str('tutoria@example.com'),
		[str(timeslot.tutor.user.email)],
		fail_silently=False,
	)
	return "success"

def cancel(cancelling_student, timeslot):
	refund = timeslot.fee * 1.05
	manage()
	if not timeslot.cancellable:
		return False
	# modify timeslot status
	timeslot.is_booked = False
	timeslot.bookable = True
	timeslot.cancellable = False
	timeslot.save()
	# modify student wallet
	cancelling_student.balance += refund
	cancelling_student.timeslot_set.remove(timeslot)
	cancelling_student.save()
	# sending notification
	createCancelNotification(timeslot)
	createTransactionNotification(timeslot, refund, "cancel")
	createTransactionRecord(timeslot, refund, "cancel")
	return True
# ==========================================================================