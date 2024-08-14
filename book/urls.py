from django.urls import path
from . import views
urlpatterns = [
    path('<int:id>/',views.BookDetailView.as_view(), name='book_detail'),
    path('borrow/<int:book_id>/',views.borrow_book, name = 'borrow_book'),
    path('return/<int:borrow_id>/',views.return_book, name = 'return_book'),
]   
