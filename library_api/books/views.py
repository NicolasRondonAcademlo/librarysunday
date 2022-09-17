from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Author, Book, BookItem, BookItemUser, Category
from .permissions import IsLibrarianOrReadOnly
from .serializers import (
    AuthorSerializer,
    BookItemSerializer,
    BookItemUserSerializer,
    BookItemUserSerializerCreate,
    BookSerializer,
    CategorySerializer,
    UserSerializerView,
)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsLibrarianOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsLibrarianOrReadOnly]
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "author__name", "categories__name"]


class AuthorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsLibrarianOrReadOnly]
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


class BookItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsLibrarianOrReadOnly]
    serializer_class = BookItemSerializer
    queryset = BookItem.objects.all()

    @action(detail=False)
    def all_book_items_rent(self, request):
        book_items = BookItem.objects.filter(is_rent=True)
        if book_items.count() == 0:
            return Response({"data": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookItemSerializer(
            book_items, many=True, context={"request": request}
        )
        return Response({"data": serializer.data})


class BookItemUserViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsLibrarianOrReadOnly]
    serializer_class = BookItemUserSerializer
    queryset = BookItemUser.objects.all()

    def __find_numbers_of_rent_books_by_user(self, user_id):
        total_books = BookItemUser.objects.filter(user__id=user_id).count()
        return total_books

    def create(self, request, *args, **kwargs):
        serializer = BookItemUserSerializerCreate(data=request.data)
        if serializer.is_valid():
            number_books = self.__find_numbers_of_rent_books_by_user(
                request.data["user"]
            )
            if number_books >= settings.MAX_BOOKS_TO_RENT:
                return Response(
                    {
                        "data": f"Actualmente tienes {number_books} libros rentados y el maximo es {settings.MAX_BOOKS_TO_RENT}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            book_item = BookItem.objects.get(pk=request.data["book_item"])
            if book_item.is_rent:
                return Response(
                    {"data": "El libro ya esta rentado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            book_item.is_rent = True
            book_item.save()
            serializer.save()
            book_user = BookItemUser.objects.get(pk=serializer.data["id"])
            data = BookItemUserSerializer(book_user, context={"request": request})
            return Response({"data": data.data}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

    def get_serializer_class(self):
        if self.action == "create":
            return BookItemUserSerializerCreate
        else:
            return BookItemUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsLibrarianOrReadOnly]
    serializer_class = UserSerializerView
    queryset = User.objects.all()

    @action(detail=True)
    def books_rent(self, request, pk):
        data = BookItemUser.objects.filter(user_id=pk)
        serializer = BookItemUserSerializer(
            data, many=True, context={"request": request}
        )
        return Response({"data": serializer.data})
