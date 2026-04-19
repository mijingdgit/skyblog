from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, UserPermission


class UserPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermission
        fields = ['can_manage_users', 'can_manage_articles', 'can_manage_projects', 'can_export_data', 'can_import_data']


class UserSerializer(serializers.ModelSerializer):
    permission = UserPermissionSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'email', 'role', 'avatar', 'phone', 'bio', 'is_active', 'date_joined', 'permission']
        read_only_fields = ['id', 'date_joined']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'nickname', 'email', 'role', 'phone']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError('两次密码不一致')
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        # 创建权限
        UserPermission.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('用户名或密码错误')
        if not user.is_active:
            raise serializers.ValidationError('账户已被禁用')
        data['user'] = user
        return data