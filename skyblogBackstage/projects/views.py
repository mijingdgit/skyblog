from django.db import models
from rest_framework import views, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Project, ProjectPageContent
from .serializers import ProjectPageContentSerializer, ProjectSerializer


class ProjectPageContentView(views.APIView):
    """Public singleton endpoint for project page copy and filters."""

    permission_classes = [AllowAny]

    def get(self, request):
        page_content = (
            ProjectPageContent.objects.filter(is_active=True).order_by('-updated_at').first()
            or ProjectPageContent.objects.order_by('-updated_at').first()
        )
        if page_content is None:
            page_content = ProjectPageContent.objects.create()

        return Response(ProjectPageContentSerializer(page_content).data)


class ProjectViewSet(viewsets.ModelViewSet):
    """Project management with published-only public reads."""

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Project.objects.all().order_by('-order', '-created_at')

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) | models.Q(description__icontains=search)
            )

        is_published = self.request.query_params.get('is_published')
        if is_published is not None:
            queryset = queryset.filter(is_published=is_published == 'true')

        return queryset
