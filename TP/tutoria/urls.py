from django.conf.urls import url, include
from .views import log_view, user_view
urlpatterns = [
    url('^$', log_view.login, name='login'),
    url('^registration/',log_view.registrate, name='registrate'),
    url('^home/', user_view.homepage, name='homepage')
]