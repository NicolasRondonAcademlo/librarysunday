from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Author, Book, BookItem, BookItemUser, Category


class UserSerializerView(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name")


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = "__all__"


class BookItemSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = BookItem
        fields = "__all__"


class BookItemUserSerializer(serializers.ModelSerializer):
    book_item = BookItemSerializer()
    user = UserSerializer()

    class Meta:
        model = BookItemUser
        fields = "__all__"


class BookItemUserSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = BookItemUser
        fields = "__all__"
