from datetime import timedelta

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template import loader
from django.utils import timezone

from pokemon.trainers.models import Trainer


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--send',
            action='store_true',
            dest='send',
            default=False,
            help='Send the emails?',
        )

    def handle(self, *args, **options):
        today = timezone.now()
        week_ago = today - timedelta(days=7)

        trainers = Trainer.objects.filter(updated_at__lte=week_ago)

        for trainer in trainers:
            days = (today - trainer.updated_at).days
            email = trainer.user.emailaddress_set.first().email
            context = {
                'email': email,
                'trainer': trainer,
                'days': days,
            }
            print(context)
            if options['send']:
                from_email = 'LNK PoGO <noreply@lnkpogo.com>'
                subject = 'Update your Trainer Profile!'
                body = loader.render_to_string('email/update_profile.txt', context)
                email_message = EmailMultiAlternatives(
                    subject, body, from_email, [email])
                html_email = loader.render_to_string('email/update_profile.html', context)
                email_message.attach_alternative(html_email, 'text/html')
                email_message.send()
