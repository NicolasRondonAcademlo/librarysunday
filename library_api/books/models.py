from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class BookShelf(models.Model):
    hallway = models.CharField(max_length=3)

    def __str__(self) -> str:
        return self.hallway


class Book(models.Model):
    title = models.CharField(max_length=200, null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

    def __str__(self) -> str:
        return self.title


class BookItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_rent = models.BooleanField(default=False)
    is_reserved = models.BooleanField(default=False)
    shelf = models.ForeignKey(BookShelf, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.book.title + "---" + self.id


class BookItemUser(models.Model):
    book_item = models.ForeignKey(BookItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.book_item.book.title + " " + self.user.first_name
