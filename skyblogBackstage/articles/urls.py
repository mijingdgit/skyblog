from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AboutProfileView, CategoryViewSet, TagViewSet, ArticleViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'', ArticleViewSet, basename='article')

urlpatterns = [
    path('about-profile/', AboutProfileView.as_view(), name='about-profile'),
    path('', include(router.urls)),
]
