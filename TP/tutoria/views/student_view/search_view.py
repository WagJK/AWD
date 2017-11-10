from django.shortcuts import render_to_response
from ...models import Tutor, Timeslot, Operation, Student
from django.http import HttpResponse


def shortProfile(request):
    all_tutors = Tutor.objects.all()
    sortedList = sorted(all_tutors, key=lambda x: x.profile.hourly_rate, reverse=False)
    return render_to_response('tutoria/student/shortProfile.html', locals())


def detailedProfile(request):

    tutor_id = request.POST['tutorID']
    selectedTutor = Tutor.objects.get(id=tutor_id)
    return render_to_response('tutoria/student/detailedProfile.html', locals())


def availableTimeSlot(request):

    tutor_id = request.POST['tutorID']
    selectedTutor = Tutor.objects.get(id=tutor_id)
    all_slots = Operation.all_slots_to_book(selectedTutor)

    return render_to_response('tutoria/student/availableTimeSlot.html', locals())


def bookTimeSlot(request):

    slot_id = request.POST['slotID']
    selectedSlot = Timeslot.objects.get(id=slot_id)
    bookingStudent = Student.objects.get(user=request.user)

    if Operation.book(bookingStudent, selectedSlot):
        return HttpResponse("Timeslot Successfully Booked!")
    else:
        return HttpResponse("Booking Rejected Due to Insufficient Balance!")


def sort(request):
    all_tutors = Tutor.objects.all()

    if request.POST['option'] == "1":
        sortedList = sorted(all_tutors, key=lambda x: x.profile.hourly_rate, reverse=False)
    elif request.POST['option'] == "2":
        sortedList = sorted(all_tutors, key=lambda x: x.profile.hourly_rate, reverse=True)
    elif request.POST['option'] == "3":
        sortedList = sorted(all_tutors, key=lambda x: x.profile.average_review, reverse=False)
    else:
        sortedList = sorted(all_tutors, key=lambda x: x.profile.average_review, reverse=True)

    return render_to_response('tutoria/student/shortProfile.html', locals())
