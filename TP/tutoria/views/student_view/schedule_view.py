from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import timezone
from tutoria.operations import *
from tutoria.views.calendar import *
from tutoria.models import Timeslot, Student

DEBUG = False

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def schedule(request):
	offset = int(request.POST['offset'])
	student = Student.objects.get(user=request.user)

	today = date.today()
	start_date = today - timedelta(days=today.weekday()+1, weeks=-offset)
	end_date = start_date + timedelta(weeks=1)
	date_range = list(daterange(start_date, end_date))
	calendar = Calendar(date_range, range(8, 20))
	weekday = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
	
	if (DEBUG):
		print("[DEBUG] offset = " + offset)
		print("[DEBUG] today = " + str(today))
		print("[DEBUG] weekday = " + str(today.weekday()))
		print("[DEBUG] start = " + str(start_date))
		print("[DEBUG] end = " + str(end_date))

	booked_timeslots = get_booked_timeslots_interval(student, start_date, end_date)

	for timeslot in booked_timeslots:
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

	return render_to_response('tutoria/student/schedule.html', locals())


def cancelTimeSlot(request):
	slot_id = request.POST['slotID']
	cancelledSlot = Timeslot.objects.get(id=slot_id)
	cancellingStudent = Student.objects.get(user=request.user)
	cancel(cancellingStudent, cancelledSlot)
	return HttpResponse("Timeslot Successfully Cancelled!")
