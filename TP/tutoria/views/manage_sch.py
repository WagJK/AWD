import pytz
from datetime import timedelta
from ..notification_create import *

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
		# calculate the fee to go to the tutor
		fee = timeslot.fee

		# session finish tutor get money
		wallet = Wallet.object.get(user=timeslot.tutor.user)
		wallet.balance += fee

		# tutor receipt, student review notification
		createReviewNotification(timeslot)
		createTransactionNotification(timeslot, fee, 'end')
		createTransactionRecord(timeslot, fee, 'end', None)

		# Mytutor receive comission fee
		mytutors = MyTutors.objects.all()[0]
		mytutors.balance += fee * 0.05
		mytutors.save()
	
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
		startTime__gte = datetime.now(tz=tz_hkt) + timedelta(days=1),
	)
	
	non_bookable_timeslots = Timeslot.objects.exclude(
		is_booked = False,
		startTime__gte = datetime.now(tz=tz_hkt) + timedelta(days=1),
	)
	bookable_timeslots.update(bookable=True)
	non_bookable_timeslots.update(bookable=False)


	# update within_week status
	within_week_timeslots = Timeslot.objects.filter(
		bookable = True,
		startTime__lte = datetime.now(tz=tz_hkt) + timedelta(weeks=1),
		startTime__gte = datetime.now(tz=tz_hkt)
	)
	not_within_week_timeslots = Timeslot.objects.exclude(
		bookable = True,
		startTime__lte = datetime.now(tz=tz_hkt) + timedelta(weeks=1),
		startTime__gte = datetime.now(tz=tz_hkt)
	)
	within_week_timeslots.update(within_week=True)
	not_within_week_timeslots.update(within_week=False)
	
	if (DEBUG):
		print("[DEBUG] finished = " + str(len(Timeslot.objects.filter(is_finished=True))))
		print("[DEBUG] bookable = " + str(len(bookable_timeslots)))
		print("[DEBUG] not bookable = " + str(len(non_bookable_timeslots)))
		print("[DEBUG] cancellable = " + str(len(cancellable_timeslots)))
		print("[DEBUG] not cancellable = " + str(len(non_cancellable_timeslots)))
		print("[DEBUG] now = " + str(datetime.now(tz=tz_hkt)))
		print("[DEBUG] scheduler end processing")