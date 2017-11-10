import logging
from datetime import datetime
from django.contrib import auth
from django.contrib.auth.models import User
from ..models import Timeslot, Confirmation
from django.utils import timezone

def manage():
	logger = logging.getLogger('django')
	logger.debug('Refreshing...')

	timeslots = Timeslot.objects.all()

	for timeslot in timeslots:
		# update states of timeslots
		if (not timeslot.is_finished) and ((datetime.now(timezone.utc) - timeslot.endTime).total_seconds() >= 0):
			timeslot.is_finished = True;
			if (timeslot.is_booked):
				# session finish tutor get money
				timeslot.tutor.balance += timeslot.fee
				# tutor receipt, student review notification
				Confirmation.clientCreateConfirmation("finished", timeslot, timeslot.fee)
				# Mytutor receive comission fee
				# ....

		if (timeslot.is_booked) and ((timeslot.startTime - datetime.now(timezone.utc)).total_seconds() >= 24 * 60 * 60):
			timeslot.available_for_cancelling = True
		else:
			timeslot.available_for_cancelling = False
		if (not timeslot.is_booked) and ((timeslot.startTime - datetime.now(timezone.utc)).total_seconds() >= 24 * 60 * 60):
			timeslot.available_for_booking = True
		else:
			timeslot.available_for_booking = False
		timeslot.save()
