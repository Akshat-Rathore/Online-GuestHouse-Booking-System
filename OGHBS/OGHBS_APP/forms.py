from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime


class SearchForm(forms.Form):
    check_in_date = forms.DateField(label="Enter check-in Date", required=True, widget=forms.SelectDateWidget())
    check_out_date = forms.DateField(label="Enter check-in Date", required=True, widget=forms.SelectDateWidget())

    def clean_check_in_date(self):
        data = self.cleaned_data['check_in_date']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - Check-in date cannot be in the past'))
        return data

    def clean_check_out_date(self):
        data = self.cleaned_data['check_out_date']
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - Check-out date cannot be in the past'))
        if data < self.cleaned_data['check_in_date']:
            raise ValidationError(_('Invalid Date- Check out date cannot be before check-in date'))
        return data
