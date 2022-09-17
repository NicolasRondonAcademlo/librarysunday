from django.contrib import admin

from .models import Author, Book, BookItem, BookItemUser, BookShelf, Category

# Register your models here.

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(BookItem)
admin.site.register(BookShelf)
admin.site.register(BookItemUser)
