from django.conf.urls import url, include
from .views import log_view
urlpatterns = [
    url('^$', log_view.login, name='login')
]