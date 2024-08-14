from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Account


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit is True:
            user.save()
            Account.objects.create(
                user=user,
                account_number=10000+user.id
            )
        return user
    
class UserDepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label='Amount')
