from django.shortcuts import render,get_object_or_404, redirect
from rest_framework import viewsets
from .models import Book, Author, Member
from .serializers import BookSerializer, AuthorSerializer, MemberSerializer
from .forms import BookForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from datetime import date
from django.contrib.auth.decorators import login_required
from .models import Book, Cart, CartItem
from django.contrib import messages
from django.db import models
from .models import Wishlist
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from library.serializers import UserSerializer  





# Create your views here.
def home(request):
    return render(request, 'home.html')

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)

        if form.is_valid():
             
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            published_date = form.cleaned_data['published_date']
            cover_image = request.FILES.get('cover_image')
            price = request.POST.get('price')
            title = request.POST.get('title')
            author = request.POST.get('author')
            published_date = request.POST.get('published_date')
            cover_image = request.FILES.get('cover_image')
            price=request.POST.get('price')
            original_price = float(request.POST.get('original_price'))
            discounted_price = float(request.POST.get('discounted_price'))

            # Check for duplicates
            if Book.objects.filter(title=title, author=author, published_date=published_date).exists():
                messages.error(request, "A book with the same Title, Author, and Published Date already exists.")
              

            else:
            # Save the book
                new_book = Book(
                    title=title,
                    author=author,
                    published_date=published_date,
                    image=cover_image,
                    original_price=original_price,
                    discounted_price=discounted_price
                )
          
                new_book.save()
                messages.success(request, "Book added successfully!")

            
        else:
            # Handle invalid form
            messages.error(request, "Please correct the errors in the form.")
    

    return render(request, 'add_book.html')
        



def book_list(request):
    books = Book.objects.all()  

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
          
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            published_date = form.cleaned_data['published_date']
            if Book.objects.filter(title=title, author=author, published_date=published_date).exists():
               
                messages.error(request, "This book already exists in the library.")
            else:
              
                form.save()
                messages.success(request, "Book added successfully!")
                return render(request, 'library/book_list.html', {'books': books, 'form': form})
        else:
            messages.error(request, "There was an error with the form.")
    return render(request, 'book_list.html', {'books': books})

def check_users(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, f"User {username} added successfully.")
        
        return redirect("check_users")  
    users = User.objects.all()  
    return render(request, 'check_users.html', {'users': users})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully!")
    return redirect('check_users')

def login_signup_view(request):
    if request.method == 'POST':
        if 'email' in request.POST: 
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login_signup')
        else:  
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'login_signup.html', {'error': 'Invalid username or password.'})
    return render(request, 'login_signup.html')

def signup_view(request):
    if request.method == 'POST':
        pass
    return render(request, 'signup.html')

@login_required
def add_to_cart(request, book_id):
        book = Book.objects.get(id=book_id)
        user_cart, created = Cart.objects.get_or_create(user=request.user)

 
        cart_item, item_created = CartItem.objects.get_or_create(cart=user_cart, book=book)

        if not item_created:
            cart_item.quantity += 1
            cart_item.save()

  
        return redirect('view_cart') 

@login_required
def view_cart(request):
    user_cart = Cart.objects.filter(user=request.user).first()
    cart_items = user_cart.items.all() if user_cart else []

    
    total_price = sum(item.book.price  * item.quantity for item in cart_items)

  
    return render(request, 'cart/view_cart.html', {'cart_items': cart_items})

def remove_from_cart(request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()

   
        return redirect('view_cart') 
def checkout(request):
    cart_items = request.session.get('cart', [])
    total_price = sum(item['quantity'] * item['price'] for item in cart_items)
    return render(request, 'cart/checkout.html', {'cart_items': cart_items})

def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    book.delete()
    messages.success(request, "Book deleted successfully.")
    return redirect('book_list') 

def view_wishlist(request):
    return render(request, 'wishlist.html')


def wishlist_view(request):
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
    else:
        return render(request, 'wishlist.html', {'error': 'You must be logged in to view your wishlist.'})
    
def add_to_wishlist(request, item_id):
    if request.user.is_authenticated:
        item = Book.objects.get(id=item_id)  
        Wishlist.objects.get_or_create(user=request.user, item=item)
        return redirect('wishlist')
    else:
        return redirect('login')
    
def add_to_wishlist(request, item_id):
    item = get_object_or_404(Book, id=item_id)

   
    if not Wishlist.objects.filter(user=request.user, item=item).exists():
       
        Wishlist.objects.create(user=request.user, item=item)

   
    return redirect('item_list')  

def process_payment(request):
   
    return render(request, 'payment/success.html')



def add_to_wishlist(request, item_id):
   
    book = get_object_or_404(Book, id=item_id)

   
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user, book=book)

        
        if created:
           
            print("Book added to wishlist.")
        else:
           
            print("Book is already in the wishlist.")
    else:
        
        wishlist = request.session.get("wishlist", [])
        if item_id not in wishlist:
            wishlist.append(item_id)
            request.session["wishlist"] = wishlist
            print("Book added to guest wishlist.")
        else:
            print("Book is already in the guest wishlist.")

   
    return redirect('wishlist')


@login_required
def remove_from_wishlist(request, book_id):
   
    book = get_object_or_404(Book, id=book_id)
    Wishlist.objects.filter(user=request.user, book=book).delete()
   

    
    next_url = request.GET.get('next', 'wishlist')
    return redirect('wishlist')

def wishlist(request):
    if request.user.is_authenticated:
        
        wishlist_items = Wishlist.objects.filter(user=request.user).select_related('book')
    else:
       
        item_ids = request.session.get('wishlist', [])
        wishlist_items = Book.objects.filter(id__in=item_ids)
    
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('book')
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  




