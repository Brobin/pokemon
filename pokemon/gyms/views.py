import cfscrape
import datetime

from datetime import timedelta

from django.conf import settings
from django.db.models import Min, Max
from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import TemplateView, View

from rest_framework.viewsets import ModelViewSet

from .models import GymLog
from .serializers import GymLogSerializer


class GymLogData(ModelViewSet):
    model = GymLog
    queryset = GymLog.objects.filter(
        created_at__gte=timezone.now() - timedelta(days=30)
    ).order_by('created_at')
    serializer_class = GymLogSerializer


class GymView(TemplateView):
    template_name = 'gyms/gyms.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['min_mystic'] = GymLog.objects.aggregate(m=Min('mystic'))['m']
        context['max_mystic'] = GymLog.objects.aggregate(m=Max('mystic'))['m']
        context['min_valor'] = GymLog.objects.aggregate(m=Min('valor'))['m']
        context['max_valor'] = GymLog.objects.aggregate(m=Max('valor'))['m']
        context['min_instinct'] = GymLog.objects.aggregate(m=Min('instinct'))['m']
        context['max_instinct'] = GymLog.objects.aggregate(m=Max('instinct'))['m']
        return context


class GymApiView(View):

    def get(self, request, *args, **kwargs):
        scraper = cfscrape.create_scraper()
        scraper.headers.update({'referer': settings.API_REFERER})
        data = scraper.get(settings.API_URL).json()
        return JsonResponse(data, safe=False)
