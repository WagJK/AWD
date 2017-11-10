from django.conf.urls import url, include
from .views import log_view
from .views.student_view import homepage_view as student_home, message_view as student_message
from .views.student_view import schedule_view as student_schedule, search_view as student_search
from .views.student_view import wallet_view as student_wallet
from .views.tutor_view import homepage_view as tutor_home, wallet_view as tutor_wallet, message_view as tutor_message
from .views.both_view import homepage_view as both_home, message_view as both_message, schedule_view as both_schedule
from .views.both_view import wallet_view as both_wallet

urlpatterns = [
    # shared log urls
    url(r'^$', log_view.login, name='login'),
    url(r'^registration/', log_view.registrate, name='registration'),
    url(r'^logout/', log_view.logout, name='logout'),

    # student urls
    url(r'^student/', include([
        # student homepage
        url(r'^homepage/', student_home.homepage, name='student_homepage'),

        # student search
        url(r'^search/', include([
            url(r'^shortProfile/', student_search.shortProfile, name='shortProfile'),
            url(r'^detailedProfile/', student_search.detailedProfile, name='detailedProfile'),
            url(r'^availableSlot/', student_search.availableTimeSlot, name='availableSlot'),
            url(r'^bookSlot/', student_search.bookTimeSlot, name='bookSlot'),
            url(r'^sort/', student_search.sort, name='sort')
        ])),

        # student upcoming tutorials in 7 days
        url(r'^schedule/', include([
            url(r'^$', student_schedule.schedule, name='schedule'),
            url(r'^cancelSlot/', student_schedule.cancelTimeSlot, name='cancelSlot'),
        ])),

        # student wallet
        url(r'^wallet/', include([
            url(r'^addValue/', student_wallet.addValue, name='addValue'),
        ])),

        # student messages
        url(r'^message/', include([
            url(r'^confirmation/', student_message.confirmation, name='studentConfirmation'),
        ])),
    ])),

    # tutor urls
    url(r'^tutor/', include([
        # tutor homepage
        url(r'^homepage/', tutor_home.homepage, name="tutor_homepage"),
        # To be added .....

        # tutor wallet
        url(r'^wallet/', include([
            url(r'^withdraw/', tutor_wallet.withdraw, name="withdraw"),
        ])),
        # tutor messages
        url(r'^messages/', include([
            url(r'^confirmation/', tutor_message.confirmation, name="tutorConfirmation"),
        ])),
    ])),

    # both urls
    url(r'^both/', include([
        # both homepage
        url(r'^homepage/', both_home.homepage, name='both_homepage'),

        # both search
        url(r'^search/', include([
            url(r'^shortProfile/', student_search.shortProfile, name='shortProfile'),
            url(r'^detailedProfile/', student_search.detailedProfile, name='detailedProfile'),
            url(r'^availableSlot/', student_search.availableTimeSlot, name='availableSlot'),
            url(r'^bookSlot/', student_search.bookTimeSlot, name='bookSlot'),
            url(r'^sort/', student_search.sort, name='sort')
        ])),

        # both upcoming tutorials in 7 days
        url(r'^schedule/', include([
            url(r'^$', student_schedule.schedule, name='schedule'),
            url(r'^cancelSlot/', student_schedule.cancelTimeSlot, name='cancelSlot'),
        ])),

        # both wallet
        url(r'^wallet/', include([
            url(r'^addValue/', both_wallet.addValue, name='addValue'),
            url(r'^withdraw/', both_wallet.withdraw, name="withdraw"),
        ])),

        # both messages
        url(r'^message/', include([
            url(r'^confirmation/', both_message.confirmation, name='bothConfirmation'),
        ])),
    ])),
]

import logging
from pytz import utc
from .views.manage_sch import manage
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor

scheduler = BackgroundScheduler()
job = scheduler.add_job(manage, 'interval', seconds=100)
scheduler.configure(timezone=utc)
scheduler.start()
