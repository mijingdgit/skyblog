from django.db import models
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import logout, authenticate, login
from .models import User, UserPermission
from .serializers import (
    UserSerializer, UserCreateSerializer, LoginSerializer,
    UserPermissionSerializer
)


class LoginView(APIView):
    """登录视图"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({
            'code': 200,
            'message': '登录成功',
            'data': UserSerializer(user).data
        })


class LogoutView(APIView):
    """登出视图"""

    def post(self, request):
        logout(request)
        return Response({'code': 200, 'message': '登出成功'})


class CurrentUserView(APIView):
    """当前用户信息"""

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'code': 401, 'message': '未登录'}, status=401)
        return Response({
            'code': 200,
            'data': UserSerializer(request.user).data
        })


class UserViewSet(viewsets.ModelViewSet):
    """用户管理视图集"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ['username', 'nickname', 'email']

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_queryset(self):
        queryset = User.objects.all().order_by('-date_joined')
        # 搜索
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(username__icontains=search) |
                models.Q(nickname__icontains=search) |
                models.Q(email__icontains=search)
            )
        # 筛选
        role = self.request.query_params.get('role')
        if role:
            queryset = queryset.filter(role=role)
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active == 'true')
        return queryset

    @action(detail=True, methods=['get'])
    def permission(self, request, pk=None):
        """获取用户权限"""
        user = self.get_object()
        permission, created = UserPermission.objects.get_or_create(user=user)
        return Response(UserPermissionSerializer(permission).data)

    @action(detail=True, methods=['post'])
    def set_permission(self, request, pk=None):
        """设置用户权限"""
        user = self.get_object()
        permission, created = UserPermission.objects.get_or_create(user=user)
        serializer = UserPermissionSerializer(permission, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'code': 200, 'message': '权限更新成功'})

    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        """重置密码"""
        user = self.get_object()
        new_password = request.data.get('password')
        if not new_password:
            return Response({'code': 400, 'message': '请提供新密码'}, status=400)
        user.set_password(new_password)
        user.save()
        return Response({'code': 200, 'message': '密码重置成功'})