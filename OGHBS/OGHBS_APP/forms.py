from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime

FOOD_CHOICE = (
  (1, 'Yes'),
  (0, 'No')
)


RATING_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)


class SearchForm(forms.Form):
    check_in_date = forms.DateField(label="Enter check-in Date ", required=True, widget=forms.DateInput(attrs={'class': 'datepicker', 'placeholder': '', 'required': 'true'}))
    check_out_date = forms.DateField(label="Enter check-out Date ", required=True, widget=forms.DateInput(attrs={'class': 'datepicker', 'placeholder': '', 'required': 'true'}))

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

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        date1 = cleaned_data.get('check_in_date')
        date2 = cleaned_data.get('check_out_date')

        if date1 and date2 and date1 > date2:
            raise ValidationError(_('Invalid date - Check-out date cannot be before Check-in Date'))


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
    # user_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Username'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Full Name'}))
    roll_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Roll No'}))
    department = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Department'}))
    # address = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Address'}))
    # password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-line full-width', 'placeholder': 'Password'}))
    # password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-line full-width', 'placeholder': 'Confirm Password'}))

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

    # def clean_user_name(self):
    #     data = self.cleaned_data['user_name']
    #     user = User.objects.filter(username=data)
    #     if len(user) != 0:
    #         raise ValidationError(_("Username is already taken"))
    #     return data

class EditProfessorForm(forms.Form):
    # user_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Username'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Full Name'}))
    # email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'input-line full-width', 'placeholder': 'Email'}))
    department = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Department'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Address'}))
    # password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-line full-width', 'placeholder': 'Password'}))
    # password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-line full-width', 'placeholder': 'Confirm Password'}))

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

    # def clean_user_name(self):
    #     data = self.cleaned_data['user_name']
    #     user = User.objects.filter(username=data)
    #     if len(user) != 0:
    #         raise ValidationError(_("Username is already taken"))
    #     return data

class BookingForm(forms.Form):
    user_name = forms.CharField(label="User Name ",widget=forms.TextInput(attrs={'class': 'input-line full-width','readonly':'true'}))
    guesthouse=forms.CharField(label="Guesthouse ",widget=forms.TextInput(attrs={'class': 'input-line full-width','readonly':'true'}))
    room_type=forms.CharField(label="Type of room ",widget=forms.TextInput(attrs={'class': 'input-line full-width','readonly':'true'}))
    check_in_date = forms.DateField(label="Check-in Date ", required=True, widget=forms.SelectDateWidget(attrs={'class': 'form-control', 'placeholder': 'Check-in Date', 'readonly': 'true','disabled':'true'}))
    check_out_date = forms.DateField(label="Check-out Date ", required=True, widget=forms.SelectDateWidget(attrs={'class': 'form-control', 'placeholder': 'Check-out Date', 'readonly': 'true','disabled':'true'}))
    visitor_num=forms.IntegerField(label="Enter no. of visitors ",widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of Visitors', 'required': 'true'}))
    food=forms.ChoiceField(initial=(1,"Yes"),choices=FOOD_CHOICE, widget=forms.Select(attrs={'class': 'custom-select category', 'required': 'false'}))
    visitor_names=forms.CharField(label="Enter name of vistors",widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Separated by \' , \'','required':'true'}))
    
    def __init__(self,room_type, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        if room_type=="AC 1 Bed" or room_type=='NAC 1 Bed':
            self.n=1
        elif room_type=="AC 2 Bed" or room_type=='NAC 2 Bed':
            self.n=2
        elif room_type=="AC 3 Bed" or room_type=='NAC 3 Bed':
            self.n=3
        else:
            self.n=1


    def clean(self):
        cleaned_data = super().clean()
        visitor_num = self.cleaned_data.get('visitor_num')
        if visitor_num>self.n:
            raise ValidationError(_("Number of vistors cannot be more than "+str(self.n)+" for one booking"))
    
    def clean_visitor_names(self):
        names = self.cleaned_data.get('visitor_names')
        num = int(self.cleaned_data.get('visitor_num'))
        cnt=names.count(",") + 1
        if cnt>num:
            raise ValidationError(_("Number of vistors cannot be more than "+str(num)+" for this booking"))
        return names

class FeedbackForm(forms.Form):
    comfort_of_stay=forms.ChoiceField(initial=(5,5),choices=RATING_CHOICES, widget=forms.Select(attrs={'class': 'custom-select category', 'required': 'false'}))
    room_cleanliness=forms.ChoiceField(initial=(5,5),choices=RATING_CHOICES, widget=forms.Select(attrs={'class': 'custom-select category', 'required': 'false'}))
    service_quality=forms.ChoiceField(initial=(5,5),choices=RATING_CHOICES, widget=forms.Select(attrs={'class': 'custom-select category', 'required': 'false'}))
    additional_feedback=forms.CharField(label="Additional Feedbacks",widget=forms.TextInput(attrs={'class': 'input-line full-width', 'placeholder': 'Additional Feedbacks...','required':'False'}))










