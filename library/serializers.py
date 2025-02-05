from rest_framework import serializers
from .models import Book, Author, Member
from django.contrib.auth.models import User



class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField() 
   

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date']

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]
        

