from django.conf.urls import url

from .views import (
    PvPView
)


urlpatterns = [
    url(r'^$', PvPView.as_view(), name='pvp'),
]
