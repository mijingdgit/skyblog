from django.db import models
from pathlib import Path
import uuid

from django.core.files.storage import default_storage
from django.utils.text import slugify
from rest_framework import views, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import AboutProfile, Article, Category, Tag
from .serializers import AboutProfileSerializer, ArticleSerializer, CategorySerializer, TagSerializer


IMAGE_SUFFIXES = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg'}
ATTACHMENT_SUFFIXES = {
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.zip', '.rar', '.7z', '.txt', '.md', '.csv', '.json', '.xmind',
}
MAX_ASSET_SIZE = 20 * 1024 * 1024


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

    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def increment_view(self, request, pk=None):
        article = self.get_object()
        Article.objects.filter(pk=article.pk).update(views=models.F('views') + 1)
        article.refresh_from_db(fields=['views'])
        return Response({'views': article.views})


class ArticleAssetUploadView(views.APIView):
    """Upload editor images and attachments for authenticated admin users."""

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        uploaded = request.FILES.get('file')
        asset_type = request.data.get('type', 'attachment')

        if uploaded is None:
            return Response({'message': '请选择要上传的文件。'}, status=400)

        if uploaded.size > MAX_ASSET_SIZE:
            return Response({'message': '文件不能超过 20MB。'}, status=400)

        suffix = Path(uploaded.name).suffix.lower()
        if asset_type == 'image':
            allowed_suffixes = IMAGE_SUFFIXES
            storage_dir = 'article-assets/images'
        else:
            allowed_suffixes = ATTACHMENT_SUFFIXES | IMAGE_SUFFIXES
            storage_dir = 'article-assets/files'

        if suffix not in allowed_suffixes:
            return Response({'message': f'暂不支持该文件类型：{suffix or "无扩展名"}。'}, status=400)

        stem = slugify(Path(uploaded.name).stem) or 'asset'
        storage_name = f'{storage_dir}/{stem}-{uuid.uuid4().hex[:10]}{suffix}'
        saved_path = default_storage.save(storage_name, uploaded)
        file_url = default_storage.url(saved_path)

        return Response({
            'name': uploaded.name,
            'url': file_url,
            'type': 'image' if asset_type == 'image' else 'attachment',
            'size': uploaded.size,
        })


class AboutProfileView(views.APIView):
    """Public singleton endpoint for the about page."""

    permission_classes = [AllowAny]

    def get(self, request):
        profile = (
            AboutProfile.objects.filter(is_active=True).order_by('-updated_at').first()
            or AboutProfile.objects.order_by('-updated_at').first()
        )
        if profile is None:
            profile = AboutProfile.objects.create()

        return Response(AboutProfileSerializer(profile).data)
