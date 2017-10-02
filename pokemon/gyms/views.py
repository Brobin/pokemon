from datetime import timedelta

from django.core import serializers
from django.db.models import Avg, Max, Min
from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import TemplateView, View

from rest_framework.viewsets import ModelViewSet

from .models import GymLog
from .serializers import GymLogSerializer


class GymLogData(ModelViewSet):
    model = GymLog
    queryset = GymLog.objects.order_by('created_at')
    serializer_class = GymLogSerializer


class GymView(TemplateView):
    template_name = 'gyms/gyms.html'
