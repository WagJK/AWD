from django.shortcuts import render_to_response
from ..models import Tutor, Timeslot, Client, Student
from django.http import HttpResponse

def homepage(request):
    student = Student.objects.get(user=request.user)
    return render_to_response('tutoria/home.html',locals())


def shortProfile(request):
    all_tutors = []
    for tutor in Tutor.objects.all():
        all_tutors.append(tutor)

    return render_to_response('tutoria/shortProfile.html', locals())


def detailedProfile(request):
    tutor_id = request.POST['tutorID']
    selectedTutor = Tutor.objects.get(id=tutor_id)
    return render_to_response('tutoria/detailedProfile.html', locals())

def availableTimeSlot(request):
    tutor_id = request.POST['tutorID']
    selectedTutor = Tutor.objects.get(id=tutor_id)
    all_slots = []
    for slot in Timeslot.objects.filter(is_booked = False, is_finished = False, tutor=selectedTutor):
        all_slots.append(slot)

    return render_to_response('tutoria/availableTimeSlot.html', locals())

def bookTimeSlot(request):
    slot_id = request.POST['slotID']
    selectedSlot = Timeslot.objects.get(id=slot_id)
    selectedSlot.is_booked = True
    bookingStudent = Student.objects.get(user=request.user)
    bookingStudent.balance -= 50
    selectedSlot.student = bookingStudent

    bookingStudent.save()
    selectedSlot.save()
    return HttpResponse("Timeslot Successfully Booked!")

def schedule(request):
    all_bookings = []
    bookingStudent = Student.objects.get(user=request.user)
    for booking in Timeslot.objects.filter(is_booked = True, student = bookingStudent):
        all_bookings.append(booking)

    return render_to_response('tutoria/schedule.html', locals())

def cancelTimeSlot(request):
    slot_id = request.POST['slotID']
    cancelledSlot = Timeslot.objects.get(id=slot_id)
    cancelledSlot.is_booked = False
    cancellingStudent = Student.objects.get(user=request.user)
    cancellingStudent.balance += 50
    cancellingStudent.timeslot_set.remove(cancelledSlot)

    cancellingStudent.save()
    cancelledSlot.save()
    return HttpResponse("Timeslot Successfully Cancelled!")

