from django.shortcuts import render_to_response
from django.http import HttpResponse
from ...operations import *
from ...views.calendar import *
from datetime import date

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

def bookingInfo(request):
	slot_id = request.POST['slotID']
	timeslot = Timeslot.objects.get(id=slot_id)
	return render_to_response('tutoria/student/booking_info.html', locals())

def cancelTimeSlot(request):
	slot_id = request.POST['slotID']
	cancelledSlot = Timeslot.objects.get(id=slot_id)
	cancellingStudent = Student.objects.get(user=request.user)
	if cancel(cancellingStudent, cancelledSlot):
		return HttpResponse('<div class="alert alert-success" role="alert"> Cancelling Successful: Timeslot Successfully Cancelled! </div>')
	else:
		return HttpResponse('<div class="alert alert-danger" role="alert"> Cancelling Rejected: Timeslot is not available for cancelling now! </div>')

def reviewTimeSlot(request):
	slot_id = request.POST['slotID']
	reviewedSlot = Timeslot.objects.get(id=slot_id)
	reviewingStudent = Student.objects.get(user=request.user)
	return render_to_response('tutoria/student/reviewpage.html', locals())

def submitReview(request):
	slot_id = request.POST['slotID']
	star_num = int(request.POST['star'])
	comment_content = request.POST.get('comment','')

	slot_reviewed = Timeslot.objects.get(id=slot_id)
	slot_reviewed.is_reviewed = True
	slot_reviewed.save()

	tutor_reviewed = slot_reviewed.tutor
	student_reviewing = Student.objects.get(user=request.user)

	anonymous = request.POST.getlist('anonymous[]', [])
	anonymousOrNot =False
	if anonymous:
		anonymousOrNot = True

	newReview = Review(
		star=star_num,
		comment=comment_content,
		tutor=tutor_reviewed,
		student=student_reviewing,
		anonymous=anonymousOrNot
	)
	newReview.save()

	# Update the average review for the current tutor
	starOfReview = 0.0
	numOfReview = 0
	for review in Review.objects.filter(tutor=tutor_reviewed):
		numOfReview += 1
		starOfReview += review.star

	if numOfReview<3:
		tutor_reviewed.profile.average_review = -1
	else:
		tutor_reviewed.profile.average_review = float(starOfReview/numOfReview)

	tutor_reviewed.profile.save()
	tutor_reviewed.save()

	return HttpResponse('<div class="alert alert-success" role="alert">  Review Successfully submitted! </div>')