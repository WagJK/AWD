from django.shortcuts import render_to_response
from ..models import Tutor, Timeslot, Client, Student
from django.http import HttpResponse

def homepage(request):
    student = Student.objects.get(user=request.user)
    return render_to_response('tutoria/home.html',locals())

def test(request):
    return render_to_response('tutoria/home.html')


def shortProfile(request):
    all_tutors = []
    for tutor in Tutor.objects.all():
        all_tutors.append(tutor)

    return render_to_response('tutoria/shortProfile.html', locals())


def detailedProfile(request):
    tutor_id = request.POST['tutorID']
    print(tutor_id)
    selectedTutor = Tutor.objects.get(id=tutor_id)
    print(selectedTutor.profile.university)
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
    selectedSlot.student = Student.objects.get(user=request.user)
    selectedSlot.student.balance -= 50
    selectedSlot.save()
    return HttpResponse("Timeslot Successfully Booked!")
