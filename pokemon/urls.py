from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView

from .views import StatsView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('allauth.urls')),
    url(r'^trainers/', include('pokemon.trainers.urls')),
    url(r'^legal/$', TemplateView.as_view(template_name='legal.html'), name='legal'),
    url(r'^$', StatsView.as_view(), name='index'),
]

if settings.DEBUG:
    from django.views.static import serve
    import debug_toolbar

    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),

        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
