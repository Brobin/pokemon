from django.contrib import messages
from django.shortcuts import redirect

from django.views.generic.edit import CreateView
from django.views.generic import TemplateView

from .forms import RaidRecordForm
from .models import Raid, RaidRecord

from ..trainers.mixins import LoginMixin

class RaidRecordCreate(LoginMixin, CreateView):
    template_name = 'raids/create.html'
    model = RaidRecord
    form_class = RaidRecordForm

    def form_valid(self, form):
        record = form.save(commit=False)
        record.trainer = self.request.user.trainer
        record.save()
        messages.success(self.request, 'Raid Time addded successfully!')
        return redirect('raid-detail', number=record.raid.pokemon)


class RaidDetail(TemplateView):
    template_name = 'raids/detail.html'

    def get_context_data(self,  *args, **kwargs):
        context= super().get_context_data(*args, **kwargs)
        context['raid'] = Raid.objects.get(pokemon=kwargs.get('number'))
        return context


class RaidList(TemplateView):
    template_name = 'raids/list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['raids'] = Raid.objects.order_by('-tier', 'pokemon')
        return context
