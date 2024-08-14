from django.contrib import admin

from .models import Book,Category,Borrow,Review

# Register your models here.
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Borrow)
admin.site.register(Review)
