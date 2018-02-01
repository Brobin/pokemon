from django.conf import settings
from django.contrib import messages
from django.db.models import Count, Case, When, Q, F, FloatField, Value
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView

from .forms import TrainerForm, PokemonForm
from .mixins import LoginMixin
from .models import Badge, BadgeApplication, FavoritePokemon, Trainer


class BadgeApplicationView(LoginMixin, CreateView):
    model = BadgeApplication
    fields = ['badge', 'screenshot', 'screenshot2', 'note']
    template_name = 'badges/application.html'

    def form_valid(self, form):
        application = form.save(commit=False)
        application.trainer = self.request.user.trainer
        application.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        messages.success(
            self.request,
            'Badge Application submitted! A Mod will review it ASAP.'
        )
        username = self.request.user.trainer.username
        return reverse('trainer-detail', kwargs={'username': username})


class BadgeList(LoginMixin, ListView):
    template_name = 'badges/list.html'
    queryset = Badge.objects.annotate(awarded=Count('trainer_badges')).order_by('-awarded')


class PokemonList(LoginMixin, ListView):
    template_name = 'pokemon/list.html'
    queryset = FavoritePokemon.objects.select_related('trainer').annotate(
        iv_pct=Case(
            When(
                Q(attack__isnull=False) &
                Q(defense__isnull=False) &
                Q(hp__isnull=False),
                then=(F('attack') + F('defense') + F('hp')) / Value(45/100)
            ),
            default=None,
            output_field=FloatField()
        )
    )
    paginate_by = 40

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['orderings'] = [
            ('-cp', 'Highest CP'),
            ('cp', 'Lowest CP'),
            ('-iv_pct', 'Highest IV%'),
            ('iv_pct', 'Lowest IV%'),
            ('number', 'Number (Ascending)'),
            ('-number', 'Number (Descending)'),
        ]
        return context

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', '-cp')
        return [ordering, '-cp']


class TrainerCreate(LoginMixin, CreateView):
    model = Trainer
    form_class = TrainerForm
    template_name = 'trainers/edit.html'

    def form_valid(self, form):
        trainer = form.save(commit=False)
        trainer.user = self.request.user
        trainer.save()
        return redirect(trainer.url)


class TrainerEdit(LoginMixin, UpdateView):
    model = Trainer
    form_class = TrainerForm
    pokemon_form_class = PokemonForm
    template_name = 'trainers/edit.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return redirect('/auth/facebook/login/?next=' + request.path)
        obj = self.get_object()
        if obj.user != self.request.user:
            messages.warning(
                self.request,
                'You do no have permission to edit this trainer'
            )
            return redirect('trainers')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(Trainer, username__iexact=self.kwargs['username'])

    def get(self, request, username, *args, **kwargs):
        trainer = self.get_object()
        form = self.form_class(instance=trainer)
        pokemon_form = self.pokemon_form_class(instance=trainer)
        return self.render_to_response({
            'form': form,
            'pokemon_form': pokemon_form
        })

    def post(self, request, username, *args, **kwargs):
        trainer = self.get_object()
        form = self.form_class(request.POST, instance=trainer)
        pokemon_form = self.pokemon_form_class(request.POST, instance=trainer)
        if form.is_valid() and pokemon_form.is_valid():
            return self.form_valid(form, pokemon_form)
        return self.render_to_response({
            'form': form,
            'pokemon_form': pokemon_form
        })

    def form_valid(self, form, pokemon_form):
        trainer = form.save()
        if pokemon_form.has_changed():
            pokemon_form.save()
        messages.success(self.request, 'Trainer Stats Updated')
        return redirect(trainer.url)


class TrainerDetail(LoginMixin, DetailView):
    model = Trainer
    template_name = 'trainers/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        trainers = Trainer.objects.count()
        t = context['object']
        # Get all the percentiles for the radar chart
        context['xp'] = Trainer.objects.filter(xp__lte=t.xp).count() / trainers
        context['pc'] = Trainer.objects.filter(pokemon_caught__lte=t.pokemon_caught).count() / trainers
        context['ps'] = Trainer.objects.filter(pokestops_spun__lte=t.pokestops_spun).count() / trainers
        context['pn'] = Trainer.objects.filter(pokedex_number__lte=t.pokedex_number).count() / trainers
        context['kw'] = Trainer.objects.filter(kilometers_walked__lte=t.kilometers_walked).count() / trainers
        context['bw'] = Trainer.objects.filter(battles_won__lte=t.battles_won).count() / trainers
        context['updates'] = t.updates.order_by('created_at')
        return context

    def get_object(self):
        return get_object_or_404(Trainer, username__iexact=self.kwargs['username'])


class TrainerList(LoginMixin, ListView):
    template_name = 'trainers/list.html'
    queryset = Trainer.objects.prefetch_related('favorite_pokemon').order_by('-xp')
    paginate_by = settings.PAGINATE_BY

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['orderings'] = [
            ('-xp', 'XP'),
            ('-pokemon_caught', 'Pokemon Caught'),
            ('-pokedex_number', 'Pokedex Entries'),
            ('-battles_won', 'Battles Won'),
            ('-pokestops_spun', 'Pokestops Spun'),
            ('-kilometers_walked', 'Kilometers Walked'),
        ]
        return context

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', '-xp')
        return [ordering, '-xp']

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            if hasattr(self.request.user, 'trainer'):
                return super().dispatch(request, *args, **kwargs)
            return redirect('trainer-create')
        messages.warning(self.request, 'Sign in to view this page.')
        return redirect('/')
