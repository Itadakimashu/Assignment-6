from typing import Any
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView,FormView
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import Book,Borrow,Review

from .forms import ReviewForm

from user.views import email_application

# Create your views here.

class BookDetailView(DetailView,FormView):
    model = Book
    form_class = ReviewForm
    template_name = 'book/book_detail.html'
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse_lazy('book_detail',kwargs={'id':  self.get_object().id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        reviews = book.reviews.all()
        context['reviews'] = reviews
        context['borrowed'] = False
        if self.request.user.is_authenticated:
            context['borrowed'] = Borrow.objects.filter(user=self.request.user,book=book).exists
        return context

    def form_valid(self, form):
        review = form.save(commit=False)
        review.book = self.get_object()
        review.user = self.request.user
        review.save()
        return super().form_valid(form)

@login_required
def borrow_book(request, book_id):
    book = Book.objects.get(id=book_id)
    user = request.user
    amount = book.price

    if amount > user.account.balance:
        messages.error(request, 'You dont have enough account blance to borrow!')
        return redirect('book_detail',book_id)
    
    user.account.balance -= amount
    user.account.save()
    
    Borrow.objects.create(
        book=book,
        user=user,
        amount=amount,
        balance_after=user.account.balance
    )
    email_application(user,'Book Borrowed Successfully',amount,'book/borrow_mail.html')
    return redirect('profile')

@login_required
def return_book(request,borrow_id):
    borrow = Borrow.objects.get(id=borrow_id)
    user_account = request.user.account

    user_account.balance += borrow.amount
    user_account.save()

    borrow.returned = True
    borrow.save()

    messages.success(request, f'refund in {borrow.amount}$ successful.')
    email_application(borrow.user,'Book Returned and Refund Successfull',borrow.amount,'book/return_book.html')

    return redirect('profile')

