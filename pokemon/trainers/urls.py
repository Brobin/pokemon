from django.conf.urls import url

from .views import (
    BadgeList,
    PokemonList,
    TrainerCreate,
    TrainerDetail,
    TrainerEdit,
    TrainerList
)


urlpatterns = [
    url(r'^badges/$', BadgeList.as_view(), name='trainer-badges'),
    url(r'^create/$', TrainerCreate.as_view(), name='trainer-create'),
    url(r'^pokemon/$', PokemonList.as_view(), name='trainer-pokemon'),
    url(r'^(?P<username>.*)/edit/$', TrainerEdit.as_view(), name='trainer-edit'),
    url(r'^(?P<username>.*)/$', TrainerDetail.as_view(), name='trainer-detail'),
    url(r'^$', TrainerList.as_view(), name='trainers'),
]
