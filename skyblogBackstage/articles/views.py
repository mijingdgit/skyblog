from django.db import models
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Article, Category, Tag
from .serializers import ArticleSerializer, CategorySerializer, TagSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Category management with public read access."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['name', 'description']


class TagViewSet(viewsets.ModelViewSet):
    """Tag management with public read access."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['name']


class ArticleViewSet(viewsets.ModelViewSet):
    """Article management with published-only public reads."""

    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Article.objects.all().order_by('-published_at', '-created_at')

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search)
                | models.Q(excerpt__icontains=search)
                | models.Q(content__icontains=search)
            )

        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category_id=category)

        tag = self.request.query_params.get('tag')
        if tag:
            queryset = queryset.filter(tags__id=tag)

        is_published = self.request.query_params.get('is_published')
        if is_published is not None:
            queryset = queryset.filter(is_published=is_published == 'true')

        if self.request.query_params.get('is_featured') == 'true':
            queryset = queryset.filter(is_featured=True)

        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        article = self.get_object()
        article.is_published = True
        article.save(update_fields=['is_published'])
        return Response({'code': 200, 'message': 'Article published'})

    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        article = self.get_object()
        article.is_published = False
        article.save(update_fields=['is_published'])
        return Response({'code': 200, 'message': 'Article unpublished'})

    @action(detail=True, methods=['post'])
    def toggle_featured(self, request, pk=None):
        article = self.get_object()
        article.is_featured = not article.is_featured
        article.save(update_fields=['is_featured'])
        state = 'featured' if article.is_featured else 'not featured'
        return Response({'code': 200, 'message': f'Article marked as {state}'})
