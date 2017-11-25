from django.shortcuts import render_to_response
from django.http import HttpResponse
from ...operations import *
from ...views.calendar import *
from ...models import Tutor, Timeslot, Student, Review
from datetime import date

DEBUG = False

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def searchOption(request):
	all_university = TutorProfile.objects.order_by('university').values_list('university', flat=True).distinct()
	all_course = Course.objects.order_by('code').values_list('code', flat=True).distinct()
	all_tag = Tag.objects.order_by('content').values_list('content', flat=True).distinct()
	return render_to_response('tutoria/student/searchpage.html', locals())

def shortProfile(request):
	all_tutors = Tutor.objects.filter(profile__availability=True)

	univ_list = request.POST.getlist('university_list[]',[])
	if univ_list:
		temp = Tutor.objects.none()
		for univ in univ_list:
			temp = temp.union(Tutor.objects.filter(profile__university=univ))

		all_tutors = set(all_tutors) & set(temp)

	#cour_list = request.POST.getlist('course_list[]',[])
	cour_list = request.POST['course_list'].split(';')
	cour_list = cour_list[0:len(cour_list)]
	if (len(cour_list) == 1 and cour_list[0] == ''):
		cour_list = []
	
	if cour_list:
		temp = Tutor.objects.none()
		for cour in cour_list:
			temp = temp.union(Tutor.objects.filter(course__code=cour))
		
		all_tutors = set(all_tutors) & set(temp)

	#tag_list = request.POST.getlist('tag_list[]',[])
	tag_list = request.POST['tag_list'].split(';')
	tag_list = tag_list[0:len(tag_list)]
	if (len(tag_list) == 1 and tag_list[0] == ''):
		tag_list = []

	if tag_list:
		temp = Tutor.objects.none()
		for tag in tag_list:
			temp = temp.union(Tutor.objects.filter(tag__content=tag))

		all_tutors = set(all_tutors) & set(temp)

	min = request.POST.get('min_rate','')
	if min != '':
		temp = Tutor.objects.filter(profile__hourly_rate__gte=(int)(min))
		all_tutors = set(all_tutors) & set(temp)

	max = request.POST.get('max_rate','')
	if max != '':
		temp = Tutor.objects.filter(profile__hourly_rate__lte=(int)(max))
		all_tutors= set(all_tutors) & set(temp)

	type = request.POST.getlist('type[]',[])
	if type:
		temp = Tutor.objects.none()
		for ty in type:
			temp = temp.union(Tutor.objects.filter(tutor_type=str(ty)))
		all_tutors= set(all_tutors) & set(temp)

	# Within seven days, to be added
	limited = request.POST.get('limited[]',[])
	list_of_ids = []
	if limited:
		slot_in_week = Timeslot.objects.filter(within_week=True)
		for slot in slot_in_week:
			list_of_ids.append(slot.tutor.id)
		temp = Tutor.objects.filter(id__in=list_of_ids)
		all_tutors= set(all_tutors) & set(temp)

	last = request.POST.get('last_name')
	if last != '':
		temp = Tutor.objects.filter(user__last_name=last)
		all_tutors= set(all_tutors) & set(temp)

	first = request.POST.get('first_name')
	if first != '':
		temp = Tutor.objects.filter(user__first_name=first)
		all_tutors= set(all_tutors) & set(temp)

	if (all_tutors):
		tutor_tags = []
		for tut in all_tutors:
			tags = Tag.objects.filter(tutor=tut)
			tutor_tags.append((tut, tags))

		return render_to_response('tutoria/student/shortProfile.html', locals())
	else:
		return HttpResponse("No Matching Result!")

def detailedProfile(request):
	tutor_id = request.POST['tutorID']
	student = Student.objects.get(user=request.user)
	selectedTutor = Tutor.objects.get(id=tutor_id)
	all_reviews = Review.objects.filter(tutor=selectedTutor).order_by('-createTime', '-id')
	tags = Tag.objects.filter(tutor=selectedTutor)
	courses = Course.objects.filter(tutor=selectedTutor)

	has_booking_between = (len(Timeslot.objects.filter(
		tutor = selectedTutor,
		student = student,
		is_booked = True
	)) > 0)
	return render_to_response('tutoria/student/detailedProfile.html', locals())

def availableTimeSlot(request):
	offset = int(request.POST['offset'])
	tutor_id = request.POST['tutorID']
	tutor = Tutor.objects.get(id=tutor_id)

	today = date.today()
	start_date = today - timedelta(days=today.weekday()+1, weeks=-offset)
	end_date = start_date + timedelta(weeks=1)
	date_range = list(daterange(start_date, end_date))
	calendar = Calendar(date_range, range(8, 20))
	weekday = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

	bookable_timeslots = get_bookable_timeslots_interval(tutor, start_date, end_date)

	if (DEBUG):
		print("[DEBUG] start = " + str(start_date))
		print("[DEBUG] end = " + str(end_date))
		print("[DEBUG] bookable tutor = " + str(len(bookable_timeslots)))

	for timeslot in bookable_timeslots:
		d = (timeslot.startTime.weekday() + 1) % 7
		h = (timeslot.startTime.hour + 8) % 24
		m = timeslot.startTime.minute

		if (DEBUG):
			print("[DEBUG] startTime = " + str(timeslot.startTime))
			print("[DEBUG] weekday = " + str(d))

		calendar.timeslots[d][h][m].state = True
		calendar.timeslots[d][h][m].timeslot = timeslot

		if (timeslot.endTime - timeslot.startTime).total_seconds() > 2700:
			calendar.next(calendar.timeslots[d][h][m]).state = True
			calendar.next(calendar.timeslots[d][h][m]).timeslot = timeslot

			calendar.timeslots[d][h][m].extend = True
			calendar.next(calendar.timeslots[d][h][m]).disable = True

	return render_to_response('tutoria/student/availableTimeSlot.html', locals())

def timeslotInfo(request):
	slot_id = request.POST['slotID']
	timeslot = Timeslot.objects.get(id=slot_id)
	return render_to_response('tutoria/student/timeslot_info.html', locals())

def bookTimeSlot(request):
	slot_id = request.POST['slotID']
	selected_slot = Timeslot.objects.get(id=slot_id)
	student = Student.objects.get(user=request.user)
	result = book(student, selected_slot)
	if result == "success":
		return HttpResponse('<div class="alert alert-success" role="alert"> Booking Successful: Timeslot Successfully Booked! </div>')
	elif result == "not bookable":
		return HttpResponse('<div class="alert alert-danger" role="alert"> Booking Rejected: Timeslot is not available for booking now! </div>')
	elif result == "own timeslot":
		return HttpResponse('<div class="alert alert-danger" role="alert"> Booking Rejected: You cannot book your own timeslot! </div>')
	elif result == "two timeslots":
		return HttpResponse('<div class="alert alert-danger" role="alert"> Booking Rejected: You cannot book two timeslots from the same tutor in a day! </div>')
	elif result == "timeslot occupied":
		return HttpResponse('<div class="alert alert-danger" role="alert"> Booking Rejected: You cannot book this timeslot due to time clash with another timeslot you booked! </div>')
	else:
		return HttpResponse('<div class="alert alert-danger" role="alert"> Booking Rejected: Insufficient Balance! </div>')

def sort(request):
	all_tutors = Tutor.objects.none()
	id_result = request.POST.getlist('id_list[]', [])
	if id_result:
		all_tutors = Tutor.objects.filter(id__in=id_result)
	print("[DEBUG]" + request.POST['option'])

	if all_tutors:
		if request.POST['option'] == "Lowest Hourly Rate":
			all_tutors = all_tutors.order_by('profile__hourly_rate')
		elif request.POST['option'] == "Highest Hourly Rate":
			all_tutors = all_tutors.order_by('-profile__hourly_rate')
		elif request.POST['option'] == "Lowest Average Review":
			all_tutors = all_tutors.order_by('profile__average_review')
		elif request.POST['option'] == "Highest Average Review":
			all_tutors = all_tutors.order_by('-profile__average_review') 

		tutor_tags = []
		for tut in all_tutors:
			tags = Tag.objects.filter(tutor=tut)
			tutor_tags.append((tut, tags))

		return render_to_response('tutoria/student/shortProfile.html', locals())
	else:
		return HttpResponse("No Matching result")