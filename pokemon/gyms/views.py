import cfscrape
import datetime

from datetime import timedelta

from django.conf import settings
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


class GymApiView(View):

    def get(self, request, *args, **kwargs):
        scraper = cfscrape.create_scraper()
        scraper.headers.update({'referer': settings.API_REFERER})
        data = scraper.get(settings.API_URL).json()
        return JsonResponse(data, safe=False)


class GymTrainerView(TemplateView):
    template_name = 'gyms/trainers.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        scraper = cfscrape.create_scraper()
        scraper.headers.update({'referer': settings.API_REFERER})
        data = scraper.get(settings.API_URL).json()

        trainers = {}

        for _gym in data['gyms']:
            gym = data['gyms'][_gym]
            for pokemon in gym['pokemon']:
                name = pokemon['trainer_name']
                if name not in trainers.keys():
                    trainers[name] = []
                trainers[name].append(
                    [datetime.datetime.fromtimestamp(pokemon['deployment_time']/1000), gym['name']]
                )

        for key, value in trainers.items():
            value.sort(key=lambda x: x[0])

        result = [{'username': key, 'gyms': value} for key, value in trainers.items() if len(value) > 1]
        result.sort(key=lambda x: len(x['gyms']), reverse=True)
            
        context['trainers'] = result
        return context
