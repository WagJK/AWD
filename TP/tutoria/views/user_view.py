from django.shortcuts import render_to_response
from ..models import Tutor, Timeslot, Student, Client, Confirmation
from django.contrib.auth.models import User
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
    all_slots = Timeslot.tutorGetAllSlots(selectedTutor)

    return render_to_response('tutoria/availableTimeSlot.html', locals())

def bookTimeSlot(request):

    slot_id = request.POST['slotID']
    selectedSlot = Timeslot.objects.get(id=slot_id)
    bookingStudent = Student.objects.get(user=request.user)
    
    if (selectedSlot.tutor.profile.tutor_type == "Contract"):
        fee = 0
    else:
        fee = selectedSlot.tutor.profile.hourly_rate * 1.05

    if bookingStudent.balance >= fee:
        bookingStudent.studentModifyBooking(fee)
        selectedSlot.slotModifyBooking(bookingStudent)
        Confirmation.clientCreateConfirmation("booking", selectedSlot, fee)
        return HttpResponse("Timeslot Successfully Booked!")
    else:
        return HttpResponse("Booking Rejected Due to Insufficient Balance!")

def schedule(request):

    bookingStudent = Student.objects.get(user=request.user)
    all_bookings = Timeslot.studentGetAllSlots(bookingStudent)
    return render_to_response('tutoria/schedule.html', locals())

def cancelTimeSlot(request):
    slot_id = request.POST['slotID']
    cancelledSlot = Timeslot.objects.get(id=slot_id)
    cancellingStudent = Student.objects.get(user=request.user)

    Confirmation.clientCreateConfirmation("cancellation", cancelledSlot)

    cancelledSlot.slotModifyCancelling()
    cancellingStudent.studentModifyCancelling(50, cancelledSlot)

    return HttpResponse("Timeslot Successfully Cancelled!")

def confirmation(request):

    requestingStudent = Student.objects.get(user=request.user)
    all_confirmations = Confirmation.clientGetAllConfirmations(requestingStudent)

    output = reversed(all_confirmations)
    return render_to_response('tutoria/confirmation.html', locals())

def addValue(request):
    requestingStudent = Student.objects.get(user=request.user)
    requestingStudent.balance = requestingStudent.balance + int(request.POST['value'])
    requestingStudent.save()

    return HttpResponse(requestingStudent.balance)