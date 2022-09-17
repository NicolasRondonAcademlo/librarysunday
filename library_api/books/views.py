from rest_framework import status, viewsets
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
)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsLibrarianOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsLibrarianOrReadOnly]
    serializer_class = BookSerializer
    queryset = Book.objects.all()


class AuthorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsLibrarianOrReadOnly]
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


class BookItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsLibrarianOrReadOnly]
    serializer_class = BookItemSerializer
    queryset = BookItem.objects.all()


class BookItemUserViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsLibrarianOrReadOnly]
    serializer_class = BookItemUserSerializer
    queryset = BookItemUser.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = BookItemUserSerializerCreate(data=request.data)
        if serializer.is_valid():
            book_item = BookItem.objects.get(pk=request.data["book_item"])
            book_item.is_rent = True
            book_item.save()
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

    def get_serializer_class(self):
        if self.action == "create":
            return BookItemUserSerializerCreate
        else:
            return BookItemUserSerializer
