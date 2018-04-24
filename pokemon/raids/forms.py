from django import forms

from .models import Raid, RaidRecord


class RaidRecordForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if 'screenshot' not in field:
                self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['raid'].queryset = Raid.objects.filter(active=True)

    class Meta:
        model = RaidRecord
        fields = ['raid', 'time_remaining', 'date', 'lineup_screenshot', 'finish_screenshot']
