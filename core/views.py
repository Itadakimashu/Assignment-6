from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView

from book.models import Book,Category

# Create your views here.

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_id = self.kwargs.get('id')

        if category_id:
            books = Book.objects.filter(category__id=category_id)
        else:
            books = Book.objects.all()
        
        categories = Category.objects.all()
        context['books'] = books
        context['categories'] = categories
        return context

