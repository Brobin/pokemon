from django.conf.urls import url

from .views import  GymView


urlpatterns = [
    url(r'^$', GymView.as_view(), name='gyms'),
]
