from django.views.generic import TemplateView

from .models import GymLog


class GymView(TemplateView):
    template_name = 'gyms/gyms.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        queryset = GymLog.objects.order_by('created_at')
        context['labels'] = list(queryset.values_list('created_at', flat=True))
        context['mystic'] = list(queryset.values_list('mystic', flat=True))
        context['valor'] = list(queryset.values_list('valor', flat=True))
        context['instinct'] = list(queryset.values_list('instinct', flat=True))
        return context
