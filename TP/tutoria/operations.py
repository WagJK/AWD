from .notification_create import *
from .views.manage_sch import manage

from datetime import datetime
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
				startTime__range=(start_date, end_date),
				within_week=True)
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
def get_all_transaction_record(user):
	try:
		currentTime = datetime.now()
		earliestTime = currentTime - timedelta(days=30)
		return TransactionRecord.objects.filter(user=user, createTime__gte=earliestTime).order_by('-createTime', '-id')
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
	wallet = Wallet.objects.get(user = booking_student.user)
	if wallet.balance < fee:
		return "insufficient balance"

	# modify student wallet
	wallet.balance -= fee
	wallet.save()

	# modify timeslot status
	timeslot.is_booked = True
	timeslot.bookable = False
	timeslot.cancellable = True
	timeslot.student = booking_student
	timeslot.save()

	# sending notification
	createBookNotification(timeslot)
	createTransactionNotification(timeslot, fee, "book")
	createTransactionRecord(timeslot, fee, "book", None)

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

	manage()
	if not timeslot.cancellable:
		return False

	# modify timeslot status
	timeslot.is_booked = False
	timeslot.bookable = True
	timeslot.cancellable = False
	timeslot.save()

	# modify student wallet
	refund = timeslot.fee * 1.05
	wallet = Wallet.objects.get(user = cancelling_student.user)
	wallet.balance += refund
	wallet.save()
	cancelling_student.timeslot_set.remove(timeslot)

	# sending notification
	createCancelNotification(timeslot)
	createTransactionNotification(timeslot, refund, "cancel")
	createTransactionRecord(timeslot, refund, "cancel", None)
	return True
# ==========================================================================