from django.shortcuts import render_to_response
from ...operations import *
from django.http import HttpResponse


def schedule(request):

    bookingStudent = Student.objects.get(user=request.user)
    all_bookings = all_slots_to_cancel(bookingStudent)
    return render_to_response('tutoria/student/schedule.html', locals())

def cancelTimeSlot(request):
    slot_id = request.POST['slotID']
    cancelledSlot = Timeslot.objects.get(id=slot_id)
    cancellingStudent = Student.objects.get(user=request.user)

    cancel(cancellingStudent, cancelledSlot)

    return HttpResponse("Timeslot Successfully Cancelled!")
