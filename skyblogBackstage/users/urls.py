from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, LogoutView, CurrentUserView, UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('', include(router.urls)),
]