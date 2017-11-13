from datetime import timedelta

from django.utils import timezone
from django.views.generic import TemplateView

from rest_framework.viewsets import ModelViewSet

from .models import GymLog
from .serializers import GymLogSerializer


class GymLogData(ModelViewSet):
    model = GymLog
    queryset = GymLog.objects.filter(
        created_at__gte=timezone.now() - timedelta(30)
    ).order_by('created_at')
    serializer_class = GymLogSerializer


class GymView(TemplateView):
    template_name = 'gyms/gyms.html'
