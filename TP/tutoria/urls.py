from django.conf.urls import url, include
from .views import log_view, user_view, tutor_view
urlpatterns = [
    url(r'^$', log_view.login, name='login'),
    url(r'^registration/',log_view.registrate, name='registrate'),
    url(r'^logout/',log_view.logout, name='logout'),
    url(r'^home/', user_view.homepage, name='homepage'),
    url(r'^student/',include([
        url(r'^shortProfile/', user_view.shortProfile, name='shortProfile'),
        url(r'^detailedProfile/', user_view.detailedProfile, name='detailedProfile'),
        url(r'^availableSlot/', user_view.availableTimeSlot, name='availableSlot'),
        url(r'^bookSlot/', user_view.bookTimeSlot, name='bookSlot'),
        url(r'^schedule/', user_view.schedule, name='schedule'),
        url(r'^cancelSlot/', user_view.cancelTimeSlot, name='cancelSlot'),
        url(r'^confirmation/', user_view.confirmation, name='confirmation'),
        url(r'^addValue/', user_view.addValue, name='addValue'),
        url(r'^sort/', user_view.sort, name='sort')
    ])),
    url(r'^tutor/',include([
        url(r'^home/',tutor_view.homepage, name="tutorhome"),
        url(r'^confirmation/',tutor_view.confirmation, name="tutorConfirmation"),
        url(r'^withdraw/', tutor_view.withdraw, name="withdraw")
    ]))
]