from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import timezone
from tutoria.operations import *
from tutoria.views.calendar import *
from tutoria.models import Timeslot, Student

DEBUG = False

def schedule(request):
	offset = int(request.POST['offset'])
	calendar = Calendar(range(0, 7), range(8, 20), [0, 30])
	weekday = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
	
	today = date.today()
	start_date = today - timedelta(days=today.weekday()+1, weeks=-offset)
	end_date = start_date + timedelta(weeks=1)
	
	if (DEBUG):
		print("[Debug] today = " + str(today))
		print("[Debug] weekday = " + str(today.weekday()))
		print("[Debug] start = " + str(start_date))
		print("[Debug] end = " + str(end_date))
		print("[Debug] offset = " + str(offset))

	tutor = Tutor.objects.get(user=request.user)
	booked_timeslots = get_booked_timeslots_interval(student, start_date, end_date)

	for timeslot in booked_timeslots:
		d = (timeslot.startTime.weekday() + 1) % 7
		h = timeslot.startTime.hour + 8
		m = timeslot.startTime.minute

		calendar.timeslots[d][h][m].state = True
		calendar.timeslots[d][h][m].timeslot = timeslot

		if (timeslot.endTime - timeslot.startTime).total_seconds() > 2700:
			calendar.next(calendar.timeslots[d][h][m]).state = True
			calendar.next(calendar.timeslots[d][h][m]).timeslot = timeslot

			calendar.timeslots[d][h][m].extend = True
			calendar.next(calendar.timeslots[d][h][m]).disable = True

	return render_to_response('tutoria/student/schedule.html', locals())