from django.conf.urls import url

from .views import (
    PvPStatView,
    PvPTeamView
)


urlpatterns = [
    url(r'^team/$', PvPTeamView.as_view(), name='pvp-team'),
    url(r'^$', PvPStatView.as_view(), name='pvp-stat'),
]
