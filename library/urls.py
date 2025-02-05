from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from .views import book_list
from library.views import UserListView 


router = DefaultRouter()
router.register(r'authors', views.AuthorViewSet)
router.register(r'books', views.BookViewSet)
router.register(r'members', views.MemberViewSet)

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('auth/', views.login_signup_view, name='login_signup'),
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
    path('add/', views.add_book, name='add_book'),
    path('books/', views.book_list, name='book_list'),
    path('books/', book_list, name='book_list'),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('users/', views.check_users, name='check_users'),
    path("api/users/", UserListView.as_view(), name="user-list"),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-to-wishlist/<int:item_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:book_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('accounts/login/', LoginView.as_view(template_name='login_signup.html'), name='login'),
    path('process-payment/', views.process_payment, name='process_payment'),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


