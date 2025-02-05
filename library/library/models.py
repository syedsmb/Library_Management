from django.db import models
from django.contrib.auth.models import User
#from .models import cart
#from .models import Book

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    # birth_date = models.DateField()

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    published_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=13)
    image = models.ImageField(upload_to='books/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    available_copies = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Add this field
    original_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def offer_percentage(self):
        if self.original_price and self.discounted_price:
            discount = (self.original_price - self.discounted_price) / self.original_price * 100
            return int(discount)
        return 0
    
    def discount_percentage(self):
        if self.original_price > 0:
            return round(100 - (self.discounted_price / self.original_price) * 100, 2)
        return 0

    def __str__(self):
        return f"{self.title} by {self.author}"

class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #items = models.ManyToManyField('Book', through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart ({self.user.username})"

class CartItem(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=1)
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Assuming a price field exists

    def __str__(self):
        return f"{self.book.title} (x{self.quantity})"
    
 

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    #item = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="wishlist_items")  # Replace 'Book' with your item model
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"  # Customize based on your model