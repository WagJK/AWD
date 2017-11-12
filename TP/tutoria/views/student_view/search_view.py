from django.shortcuts import render_to_response
from django.http import HttpResponse
from ...operations import *

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

    tutor_id = request.POST['tutorID']
    selectedTutor = Tutor.objects.get(id=tutor_id)
    all_slots = all_slots_to_book(selectedTutor)
    return render_to_response('tutoria/student/availableTimeSlot.html', locals())


def bookTimeSlot(request):
    slot_id = request.POST['slotID']
    selectedSlot = Timeslot.objects.get(id=slot_id)
    bookingStudent = Student.objects.get(user=request.user)
    if book(bookingStudent, selectedSlot):
        return HttpResponse("Timeslot Successfully Booked!")
    else:
        return HttpResponse("Booking Rejected Due to Insufficient Balance!")


def sort(request):
    all_tutors = Tutor.objects.none()
    id_result = request.POST.getlist('id_list[]', [])
    if id_result:
        all_tutors = Tutor.objects.filter(id__in=id_result)


    if all_tutors:
        if request.POST['option'] == "1":
            all_tutors = all_tutors.order_by('profile__hourly_rate')
        elif request.POST['option'] == "2":
            all_tutors = all_tutors.order_by('-profile__hourly_rate')
        elif request.POST['option'] == "3":
            all_tutors = all_tutors.order_by('profile__average_review')
        elif request.POST['option'] == "4":
            all_tutors = all_tutors.order_by('-profile__average_review')

        return render_to_response('tutoria/student/shortProfile.html', locals())
    else:
        return HttpResponse("No Matching result")