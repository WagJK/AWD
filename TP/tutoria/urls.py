from django.conf.urls import url, include
from .views import *

urlpatterns = [
    #shared log urls
    url(r'^$', log_view.login, name='login'),
    url(r'^registration/',log_view.registrate, name='registration'),
    url(r'^logout/',log_view.logout, name='logout'),
    #student urls
    url(r'^student/',include([
        #student homepage
        url(r'^homepage/', student_view, name='student_homepage'),
        #student search
        url(r'^search/', include([
            url(r'^shortProfile/', user_view.shortProfile, name='shortProfile'),
            url(r'^detailedProfile/', user_view.detailedProfile, name='detailedProfile'),
            url(r'^availableSlot/', user_view.availableTimeSlot, name='availableSlot'),
            url(r'^bookSlot/', user_view.bookTimeSlot, name='bookSlot'),
            url(r'^sort/', user_view.sort, name='sort')
        ])),
        #student upcoming tutorials in 7 days
        url(r'^schedule/', include([
            url(r'^schedule/', user_view.schedule, name='schedule'),
            url(r'^cancelSlot/', user_view.cancelTimeSlot, name='cancelSlot'),
        ])),
        #student wallet
        url(r'^wallet/', include([
            url(r'^addValue/', user_view.addValue, name='addValue'),
        ])),
        #student messages
        url(r'^message/', include([
            url(r'^confirmation/', user_view.confirmation, name='confirmation'),
        ])),    
    ])),
    #tutor urls
    url(r'^tutor/',include([
        #tutor homepage
        url(r'^homepage/',tutor_view.homepage, name="tutorhome"),
        #To be added ..... 

        #tutor wallet
        url(r'^wallet/', include([
            url(r'^withdraw/', tutor_view.withdraw, name="withdraw"),
        ])),
        #tutor messages
        url(r'^messages/', include([
            url(r'^confirmation/',tutor_view.confirmation, name="tutorConfirmation"),
        ])),
    ]))
]