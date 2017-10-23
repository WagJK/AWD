from django.conf.urls import url, include
from .views import log_view, user_view
urlpatterns = [
    url(r'^$', log_view.login, name='login'),
    url(r'^registration/',log_view.registrate, name='registrate'),
    url(r'^home/', user_view.homepage, name='homepage'),
    url(r'^student/',include([
        url(r'^shortProfile/', user_view.shortProfile, name='shortProfile'),
        url(r'^detailedProfile/', user_view.detailedProfile, name='detailedProfile'),
        url(r'^availableSlot/', user_view.availableTimeSlot, name='availableSlot'),
        url(r'^bookSlot/', user_view.bookTimeSlot, name='bookSlot'),
        url(r'^schedule/', user_view.schedule, name='schedule'),
        url(r'^cancelSlot/', user_view.cancelTimeSlot, name='cancelSlot')
    ])),
]