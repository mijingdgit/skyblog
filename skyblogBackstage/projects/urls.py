from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectPageContentView, ProjectViewSet

router = DefaultRouter()
router.register(r'', ProjectViewSet, basename='project')

urlpatterns = [
    path('page-content/', ProjectPageContentView.as_view(), name='project-page-content'),
    path('', include(router.urls)),
]
