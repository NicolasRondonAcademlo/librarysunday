from rest_framework.routers import DefaultRouter

from .views import AuthorViewSet, BookItemUserViewSet, BookViewSet, CategoryViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("books", BookViewSet)
router.register("authors", AuthorViewSet)
router.register("book_users", BookItemUserViewSet)
urlpatterns = [] + router.urls
