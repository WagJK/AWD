import logging
import pytz
from datetime import datetime
from datetime import timedelta
from django.contrib import auth
from django.contrib.auth.models import User
from ..models import Timeslot, Confirmation
from django.utils import timezone

DEBUG = False

def manage():
	
	if (DEBUG):
		print("[DEBUG] scheduler start")

	tz_hkt = pytz.timezone("Asia/Hong_Kong")
	# update is_finished state of timeslots
	finished_timeslots = Timeslot.objects.filter(
		is_finished = False,
		endTime__lte = datetime.now(tz=tz_hkt)
	)
	finished_timeslots.update(is_finished=True)
	
	# filter booked timeslots among just-finished timeslots
	finished_booked_timeslots = Timeslot.objects.filter(
		is_booked = True,
		is_finished = False,
		endTime__lte = datetime.now(tz=tz_hkt)
	)
	for timeslot in finished_timeslots:
		# session finish tutor get money
		timeslot.tutor.balance += timeslot.fee
		# tutor receipt, student review notification
		Confirmation.clientCreateConfirmation("finished", timeslot, timeslot.fee)
		# Mytutor receive comission fee
		Mytutor.balance += timeslot.fee * Mytutor.commission_rate
	
	# update cancellable status
	cancellable_timeslots = Timeslot.objects.filter(
		is_booked = True,
		startTime__gte = datetime.now(tz=tz_hkt) + timedelta(days=1)
	)

	non_cancellable_timeslots = Timeslot.objects.exclude(
		is_booked = True,
		startTime__gte = datetime.now(tz=tz_hkt) + timedelta(days=1)
	)
	non_cancellable_timeslots.update(cancellable = False)
	cancellable_timeslots.update(cancellable = True)

	# update bookable status
	bookable_timeslots = Timeslot.objects.filter(
		is_booked = False,
		startTime__gte = datetime.now(tz=tz_hkt) + timedelta(days=1)
	)
	
	non_bookable_timeslots = Timeslot.objects.exclude(
		is_booked = False,
		startTime__gte = datetime.now(tz=tz_hkt) + timedelta(days=1)
	)
	
	bookable_timeslots.update(bookable=True)
	non_bookable_timeslots.update(bookable=False)
	
	if (DEBUG):
		print("[DEBUG] finished = " + str(len(Timeslot.objects.filter(is_finished=True))))
		print("[DEBUG] bookable = " + str(len(bookable_timeslots)))
		print("[DEBUG] not bookable = " + str(len(non_bookable_timeslots)))
		print("[DEBUG] cancellable = " + str(len(cancellable_timeslots)))
		print("[DEBUG] not cancellable = " + str(len(non_cancellable_timeslots)))
		print("[DEBUG] now = " + str(datetime.now(tz=tz_hkt)))
		print("[DEBUG] scheduler end processing")