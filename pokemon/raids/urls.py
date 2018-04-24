from django.conf.urls import url

from .views import (
    RaidRecordCreate,
    RaidDetail,
    RaidList
)


urlpatterns = [
    url(r'^create/$', RaidRecordCreate.as_view(), name='raid-record-create'),
    url(r'^(?P<number>\d+)/$', RaidDetail.as_view(), name='raid-detail'),
    url(r'^$', RaidList.as_view(), name='raids'),
]
