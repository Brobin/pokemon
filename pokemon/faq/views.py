from django.views.generic import ListView

from .models import Faq


class FaqView(ListView):
    model = Faq
    template_name = 'faq/list.html'
