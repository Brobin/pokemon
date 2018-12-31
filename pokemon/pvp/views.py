from django.shortcuts import render

from django.views.generic import TemplateView


class PvPView(TemplateView):
    template_name = 'pvp/index.html'
