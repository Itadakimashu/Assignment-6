from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='bookcover/')
    price = models.DecimalField(max_digits=10,decimal_places=2)

    category = models.ManyToManyField(Category,related_name='categories')

    def __str__(self):
        return self.title
    

class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='borrowed_books')
    borrow_date = models.DateField(auto_now_add=True)
    returned = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2,default=0)


    def __str__(self):
        return f'{self.user.username} - {self.book.title}'



class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.CharField(max_length=1, choices=(
        ('1','1'),('2','2'),('3','3'),('4','4'),('5','5')
    ))
    review = models.TextField()
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Rated {self.rating} - {self.user.username} - {self.book.title}'
