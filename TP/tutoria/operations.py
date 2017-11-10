import logging
from django.db import models
from django.contrib.auth.models import User
from .models import *
from .views.manage_sch import manage

def all_slots_to_book(client):
	try:
		if client.login_type == "Tutor":
			return Timeslot.objects.filter(available_for_booking=True, is_booked=False, is_finished=False, tutor=client)
	except Timeslot.DoesNotExist:
		return None

def all_slots_to_cancel(client):
	try:
		if client.login_type == "Student":
			return Timeslot.objects.filter(available_for_cancelling=True, is_booked=True, student=client)
	except Timeslot.DoesNotExist:
		return None

def book(booking_student, timeslot):
	fee = timeslot.fee * 1.05
	if booking_student.balance < fee:
		return False
	# manage()
	if not timeslot.available_for_booking:
		return False
	# modify student wallet
	booking_student.balance -= fee
	booking_student.save()
	# modify timeslot status
	timeslot.is_booked = True
	timeslot.available_for_booking = False
	timeslot.available_for_cancelling = True
	timeslot.student = booking_student
	timeslot.save()
	# sending confirmation
	Confirmation.clientCreateConfirmation("booking", timeslot, fee)
	return True

def cancel(cancelling_student, timeslot):
	refund = timeslot.fee * 1.05
	manage()
	if not timeslot.available_for_cancelling:
		return False
	# modify timeslot status
	timeslot.is_booked = False
	timeslot.available_for_booking = True
	timeslot.available_for_cancelling = False
	timeslot.save()
	# modify student wallet
	cancelling_student.balance += refund
	cancelling_student.timeslot_set.remove(timeslot)
	cancelling_student.save()
	# sending confirmation
	Confirmation.clientCreateConfirmation("cancellation", timeslot, refund)
