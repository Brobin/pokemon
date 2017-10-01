from django.conf.urls import url

from .views import  GymView, GymLogData


urlpatterns = [
    url(r'^data/$', GymLogData.as_view({'get': 'list'}), name='gym-data'),
    url(r'^$', GymView.as_view(), name='gyms'),
]
