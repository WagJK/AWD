from django.conf.urls import url, include
from .views import log_view

urlpatterns = [
    #shared log urls
    url(r'^$', log_view.login, name='login'),
    url(r'^registration/',log_view.registrate, name='registration'),
    url(r'^logout/',log_view.logout, name='logout'),
    #student urls
]