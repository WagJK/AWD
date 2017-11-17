from django.shortcuts import render_to_response
from django.http import HttpResponse
from ...operations import *
from ...views.calendar import *
from ...models import Tutor, Timeslot, Student
from datetime import timedelta,date

DEBUG = False

def searchOption(request):
	all_university = TutorProfile.objects.order_by('university').values_list('university', flat=True).distinct()
	all_course = Course.objects.order_by('code').values_list('code', flat=True).distinct()
	all_tag = Tag.objects.order_by('content').values_list('content', flat=True).distinct()

	return render_to_response('tutoria/student/searchpage.html', locals())

def shortProfile(request):
	all_tutors = Tutor.objects.all()

	univ_list = request.POST.getlist('university_list[]',[])
	if univ_list:
		temp = Tutor.objects.none()
		for univ in univ_list:
			temp = temp.union(Tutor.objects.filter(profile__university=univ))

		all_tutors = all_tutors.intersection(temp)

	cour_list = request.POST.getlist('course_list[]',[])
	if cour_list:
		temp = Tutor.objects.none()
		for cour in cour_list:
			temp = temp.union(Tutor.objects.filter(course__code=cour))

		all_tutors = all_tutors.intersection(temp)

	tag_list = request.POST.getlist('tag_list[]',[])
	if tag_list:
		temp = Tutor.objects.none()
		for tag in tag_list:
			temp = temp.union(Tutor.objects.filter(tag__content=tag))
		all_tutors = all_tutors.intersection(temp)

	min = request.POST.get('min_rate','')
	if min != '':
		all_tutors = all_tutors.filter(profile__hourly_rate__gte=(int)(min)).distinct()

	max = request.POST.get('max_rate','')
	if max != '':
		all_tutors = all_tutors.filter(profile__hourly_rate__lte=(int)(max)).distinct()

	type = request.POST.getlist('type[]',[])
	if type:
		temp = Tutor.objects.none()
		for ty in type:
			temp = temp.union(Tutor.objects.filter(tutor_type=str(ty)))

		all_tutors = all_tutors.intersection(temp)

	# Within seven days, to be added
	limited = request.POST.getlist('limited[]',[])
	list_of_ids = []
	if limited:
		slot_in_week = Timeslot.objects.filter(within_week=True)
		for slot in slot_in_week:
			list_of_ids.append(slot.tutor.id)

		all_tutors = all_tutors.filter(id__in=list_of_ids)

	last = request.POST.get('last_name')
	if last != '':
		all_tutors= all_tutors.filter(user__last_name=last)

	first = request.POST.get('first_name')
	if first != '':
		all_tutors = all_tutors.filter(user__first_name=first)

	if (all_tutors):
		return render_to_response('tutoria/student/shortProfile.html', locals())
	else:
		return HttpResponse("No Matching Result!")

def detailedProfile(request):

	tutor_id = request.POST['tutorID']
	selectedTutor = Tutor.objects.get(id=tutor_id)
	return render_to_response('tutoria/student/detailedProfile.html', locals())


def availableTimeSlot(request):
	offset = int(request.POST['offset'])
	calendar = Calendar(range(0, 7), range(8, 20), [0, 30])
	weekday = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
	
	today = date.today()
	start_date = today - timedelta(days=today.weekday()+1, weeks=-offset)
	end_date = start_date + timedelta(weeks=1)

	tutor_id = request.POST['tutorID']
	tutor = Tutor.objects.get(id=tutor_id)
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

def bookTimeSlot(request):
	slot_id = request.POST['slotID']
	selected_slot = Timeslot.objects.get(id=slot_id)
	student = Student.objects.get(user=request.user)
	if book(student, selected_slot):
		return HttpResponse("Timeslot Successfully Booked!")
	else:
		return HttpResponse("Booking Rejected Due to Insufficient Balance!")


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

		return render_to_response('tutoria/student/shortProfile.html', locals())
	else:
		return HttpResponse("No Matching result")