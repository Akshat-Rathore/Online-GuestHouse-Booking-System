from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime


class SearchForm(forms.Form):
    check_in_date = forms.DateField(label="Enter check-in Date ", required=True, widget=forms.SelectDateWidget())
    check_out_date = forms.DateField(label="Enter check-out Date ", required=True, widget=forms.SelectDateWidget())

    def clean(self):
        cleaned_data = super().clean()
        date1 = cleaned_data['check_in_date']
        date2 = cleaned_data['check_out_date']

        if date1 > date2:
            raise ValidationError(_('Invalid date - Check-out date cannot be before Check-in Date'))

    def clean_check_in_date(self):
        data = self.cleaned_data['check_in_date']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - Check-in date cannot be in the past'))
        return data

    def clean_check_out_date(self):
        data = self.cleaned_data['check_out_date']
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - Check-out date cannot be in the past'))
        return data



class StudentForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Username'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Full Name'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'input-line full-width', 'placeholder': 'Email'}))
    roll_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Roll No'}))
    department = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Department'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Address'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-line full-width', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-line full-width', 'placeholder': 'Confirm Password'}))

    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get('password1')
        pass2 = cleaned_data.get('password2')
        if pass1 != pass2:
            raise ValidationError(_("Password and Confirm Password don't match with each other"))

    def clean_email(self):
        data = self.cleaned_data['email']
        user = User.objects.filter(email=data)
        if len(user) != 0:
            raise ValidationError(_("User is already registered"))
        elif len(data) < 12 or data[-12:] != "iitkgp.ac.in":
            raise ValidationError(_("Please enter your institute Email ID"))
        return data

    def clean_user_name(self):
        data = self.cleaned_data['user_name']
        user = User.objects.filter(username=data)
        if len(user) != 0:
            raise ValidationError(_("Username is already taken"))
        return data

class ProfessorForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Username'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Full Name'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'input-line full-width', 'placeholder': 'Email'}))
    department = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Department'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Address'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-line full-width', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-line full-width', 'placeholder': 'Confirm Password'}))

    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get('password1')
        pass2 = cleaned_data.get('password2')
        if pass1 != pass2:
            raise ValidationError(_("Password and Confirm Password don't match with each other"))

    def clean_email(self):
        data = self.cleaned_data['email']
        user = User.objects.filter(email=data)
        if len(user) != 0:
            raise ValidationError(_("User is already registered"))
        elif len(data) < 12 or data[-12:] != "iitkgp.ac.in":
            raise ValidationError(_("Please enter your institute Email ID"))
        return data

    def clean_user_name(self):
        data = self.cleaned_data['user_name']
        user = User.objects.filter(username=data)
        if len(user) != 0:
            raise ValidationError(_("Username is already taken"))
        return data

class LoginForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-line full-width', 'placeholder': 'Password'}))


class EditStudentForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Username'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Full Name'}))
    roll_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Roll No'}))
    department = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Department'}))
    # address = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Address'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-line full-width', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-line full-width', 'placeholder': 'Confirm Password'}))

    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get('password1')
        pass2 = cleaned_data.get('password2')
        if pass1 != pass2:
            raise ValidationError(_("Password and Confirm Password don't match with each other"))

    # def clean_email(self):
    #     data = self.cleaned_data['email']
    #     user = User.objects.filter(email=data)
    #     if len(user) != 0:
    #         raise ValidationError(_("User is already registered"))
    #     elif len(data) < 12 or data[-12:] != "iitkgp.ac.in":
    #         raise ValidationError(_("Please enter your institute Email ID"))
    #     return data

    def clean_user_name(self):
        data = self.cleaned_data['user_name']
        user = User.objects.filter(username=data)
        if len(user) != 0:
            raise ValidationError(_("Username is already taken"))
        return data

class EditProfessorForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Username'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Full Name'}))
    # email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'input-line full-width', 'placeholder': 'Email'}))
    department = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Department'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Address'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-line full-width', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-line full-width', 'placeholder': 'Confirm Password'}))

    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get('password1')
        pass2 = cleaned_data.get('password2')
        if pass1 != pass2:
            raise ValidationError(_("Password and Confirm Password don't match with each other"))

    # def clean_email(self):
    #     data = self.cleaned_data['email']
    #     user = User.objects.filter(email=data)
    #     if len(user) != 0:
    #         raise ValidationError(_("User is already registered"))
    #     elif len(data) < 12 or data[-12:] != "iitkgp.ac.in":
    #         raise ValidationError(_("Please enter your institute Email ID"))
    #     return data

    def clean_user_name(self):
        data = self.cleaned_data['user_name']
        user = User.objects.filter(username=data)
        if len(user) != 0:
            raise ValidationError(_("Username is already taken"))
        return data