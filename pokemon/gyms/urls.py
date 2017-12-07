from django.conf.urls import url

from .views import  GymView, GymLogData, GymApiView, GymTrainerView


urlpatterns = [
    url(r'^trainers/$', GymTrainerView.as_view(), name='gym-trainers'),
    url(r'^data/$', GymLogData.as_view({'get': 'list'}), name='gym-data'),
    url(r'^api/$', GymApiView.as_view(), name='gym-api'),
    url(r'^$', GymView.as_view(), name='gyms'),
]
