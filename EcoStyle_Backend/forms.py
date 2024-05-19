from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'username': 'Username', 'email': 'Email', 'password1': '<PASSWORD>',},


class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16)
    exp_month = forms.ChoiceField(choices=[(str(i), str(i)) for i in range(1, 13)])
    exp_year = forms.ChoiceField(choices=[(str(i), str(i)) for i in range(datetime.now().year, datetime.now().year + 10)])
    CVV = forms.CharField(max_length=3)

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        if len(card_number) != 16:
            raise forms.ValidationError("Card number must be 16 digits.")
        return card_number

    def clean_CVV(self):
        cvv = self.cleaned_data['CVV']
        if len(cvv) != 3:
            raise forms.ValidationError("CVV must be 3 digits.")
        return cvv

