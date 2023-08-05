# coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language

from . import models


class TranslatedMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.trans(get_language())


class OptOutForm(forms.ModelForm):
    feedback = TranslatedMultipleChoiceField(
        label=_('Please help us provide a better service'),
        widget=forms.CheckboxSelectMultiple,
        queryset=models.OptOutFeedback.objects.all(),
        required=False)

    class Meta:
        model = models.OptOut
        fields = ('email', 'feedback', 'comment')
        labels = {
            'comment': _('Please tell us what can we do better'),
        }

    def save(self, commit=True):
        item = super().save(commit)
        if commit:
            feedback = models.OptOutFeedback.objects.filter(pk__in=self.cleaned_data['feedback'])
            item.feedback.add(*feedback)
        return item
