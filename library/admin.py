from django.contrib import admin
from .models import Book, Author, Member, Wishlist

# Register your models here.


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'original_price', 'discounted_price', 'discount_percentage')
    list_editable = ('original_price', 'discounted_price')
    readonly_fields = ('discount_percentage',)

    def discount_percentage(self, obj):
        if obj.original_price > 0:
            return f"{round(100 - (obj.discounted_price / obj.original_price) * 100, 2)}%"
        return "0%"
    discount_percentage.short_description = "Discount Percentage"

admin.site.register(Wishlist)
admin.site.register(Author)
admin.site.register(Member)
