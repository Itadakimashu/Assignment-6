from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView,FormView,ListView


from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User

from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserRegistrationForm,UserDepositForm

from .models import Account

from book.models import Book,Borrow

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.

def email_application(user,subject,amount,template):
        message = render_to_string(template,{
            'amount': amount,
            'user': user,
        })
        send_email = EmailMultiAlternatives(subject,'', to=[user.email])
        send_email.attach_alternative(message,'text/html')
        send_email.send()

class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')
    template_name = 'user/register.html'


class UserLoginView(LoginView):
    template_name = 'user/login.html'
    def get_success_url(self):
        messages.success(self.request, 'successfully logged in')
        return reverse_lazy('home')

class UserLogoutView(LoginRequiredMixin,LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')
    

class UserDepositView(LoginRequiredMixin,FormView):
    form_class = UserDepositForm
    template_name = 'user/deposit.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self,form):
        user = self.request.user
        amount = form.cleaned_data['amount']
        user.account.balance += amount
        user.account.save()
        messages.success(self.request, f'Successfully Deposited {amount}$.')
        email_application(user,'Deposit Mail',amount,'user/deposit_mail.html')
        return super().form_valid(form)
    

class UserProfileView(LoginRequiredMixin,ListView):
    model = Book
    template_name = 'user/profile.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        borrows = Borrow.objects.filter(user=self.request.user)
        context['borrows'] = borrows
        return context
    



