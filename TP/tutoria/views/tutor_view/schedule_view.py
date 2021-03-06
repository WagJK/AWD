from django.shortcuts import render_to_response
from django.http import HttpResponse
from ...operations import *
from ...views.calendar import *
from ...models import Timeslot
from datetime import date

DEBUG = False

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def schedule(request):
	offset = int(request.POST['offset'])
	tutor = Tutor.objects.get(user=request.user)

	today = date.today()
	start_date = today - timedelta(days=today.weekday()+1, weeks=-offset)
	end_date = start_date + timedelta(weeks=1)
	date_range = list(daterange(start_date, end_date))
	calendar = Calendar(date_range, range(8, 20), private_tutor=(tutor.tutor_type == "Private"))
	weekday = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

	if (DEBUG):
		print("[DEBUG] offset = " + offset)
		print("[DEBUG] today = " + str(today))
		print("[DEBUG] weekday = " + str(today.weekday()))
		print("[DEBUG] start = " + str(start_date))
		print("[DEBUG] end = " + str(end_date))
	
	all_timeslots = get_all_timeslots_interval(tutor, start_date, end_date)

	for timeslot in all_timeslots:
		d = (timeslot.startTime.weekday() + 1) % 7
		h = (timeslot.startTime.hour + 8) % 24
		m = timeslot.startTime.minute

		calendar.timeslots[d][h][m].state = True
		calendar.timeslots[d][h][m].timeslot = timeslot

		if (timeslot.endTime - timeslot.startTime).total_seconds() > 2700:
			calendar.next(calendar.timeslots[d][h][m]).state = True
			calendar.next(calendar.timeslots[d][h][m]).timeslot = timeslot

			calendar.timeslots[d][h][m].extend = True
			calendar.next(calendar.timeslots[d][h][m]).disable = True

	return render_to_response('tutoria/tutor/schedule.html', locals())

def bookingInfo(request):
	slot_id = request.POST['slotID']
	timeslot = Timeslot.objects.get(id=slot_id)
	return render_to_response('tutoria/tutor/booking_info.html', locals())

def deactivate(request):
	slotID = int(request.POST['slotID'])
	timeslot = Timeslot.objects.get(id = slotID)
	time_str = (timeslot.startTime + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
	timeslot.delete()
	return HttpResponse(time_str)


def activate(request):
	tutor = Tutor.objects.get(user=request.user)
	time_str = request.POST['time']
	startTime = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
	if tutor.tutor_type == "Contract":
		endTime = startTime + timedelta(minutes = 30)
	else:
		endTime = startTime + timedelta(hours = 1)
	within_week = (datetime.now() + timedelta(weeks = 1) > startTime)
	new_timeslot = Timeslot.objects.create(
		bookable = True,
		cancellable = False,
		is_booked = False,
		is_finished = False,
		within_week = within_week,
		startTime = startTime,
		endTime = endTime,
		tutor = tutor,
		student = None,
		fee = tutor.profile.hourly_rate
	)
	return HttpResponse(new_timeslot.id)