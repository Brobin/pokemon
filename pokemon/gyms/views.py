from datetime import timedelta

from django.db.models import Avg, Max, Min
from django.utils import timezone
from django.views.generic import TemplateView

from .models import GymLog


class GymView(TemplateView):
    template_name = 'gyms/gyms.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        yesterday = timezone.now() - timedelta(days=1)
        queryset = GymLog.objects.filter(created_at__gte=yesterday).order_by('created_at')
        context['labels'] = list(queryset.values_list('created_at', flat=True))
        context['mystic'] = list(queryset.values_list('mystic', flat=True))
        context['valor'] = list(queryset.values_list('valor', flat=True))
        context['instinct'] = list(queryset.values_list('instinct', flat=True))
        stats = GymLog.objects.aggregate(
            mystic_max=Max('mystic'),
            mystic_min=Min('mystic'),
            mystic_avg=Avg('mystic'),
            valor_max=Max('valor'),
            valor_min=Min('valor'),
            valor_avg=Avg('valor'),
            instinct_max=Max('instinct'),
            instinct_min=Min('instinct'),
            instinct_avg=Avg('instinct'),
        )
        total = (
            stats['mystic_avg'] +
            stats['valor_avg'] +
            stats['instinct_avg']
        )
        stats['mystic_pct'] = stats['mystic_avg'] / total * 100
        stats['valor_pct'] = stats['valor_avg'] / total * 100
        stats['instinct_pct'] = stats['instinct_avg'] / total * 100
        context['stats'] = stats
        return context
