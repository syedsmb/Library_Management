# forms.py
from django import forms
from .models import Book
from datetime import date

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'cover_image', 'available_copies']  
def clean_published_date(self):
    published_date = self.cleaned_data.get('published_date')
    if not published_date:
        published_date = date.today() 
    return published_date