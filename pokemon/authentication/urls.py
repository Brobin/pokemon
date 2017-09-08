from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView

from .views import signup


urlpatterns = [
    url(r'^signup/$', signup, name='signup'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^login/$', LoginView.as_view(), name='login'),
]
