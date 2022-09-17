from rest_framework.routers import DefaultRouter

from .views import (
    AuthorViewSet,
    BookItemUserViewSet,
    BookItemViewSet,
    BookViewSet,
    CategoryViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("books", BookViewSet)
router.register("authors", AuthorViewSet)
router.register("book_users", BookItemUserViewSet)
router.register("book_items", BookItemViewSet)
router.register("users", UserViewSet)
urlpatterns = [] + router.urls
