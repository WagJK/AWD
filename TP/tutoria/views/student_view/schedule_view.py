from django.shortcuts import render_to_response
from ...models import Timeslot, Operation, Student
from django.http import HttpResponse


def schedule(request):

    bookingStudent = Student.objects.get(user=request.user)
    all_bookings = Operation.all_slots_to_cancel(bookingStudent)
    return render_to_response('tutoria/student/schedule.html', locals())

def cancelTimeSlot(request):
    slot_id = request.POST['slotID']
    cancelledSlot = Timeslot.objects.get(id=slot_id)
    cancellingStudent = Student.objects.get(user=request.user)

    Operation.cancel(cancellingStudent, cancelledSlot)

    return HttpResponse("Timeslot Successfully Cancelled!")
