from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, UserPermission


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["username", "nickname", "email", "role", "is_active", "date_joined"]
    list_filter = ["role", "is_active", "is_staff", "date_joined"]
    search_fields = ["username", "nickname", "email"]
    ordering = ["-date_joined"]

    fieldsets = BaseUserAdmin.fieldsets + (
        ("基本信息", {"fields": ("nickname", "avatar", "phone", "bio")}),
        ("角色权限", {"fields": ("role",)}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("基本信息", {"fields": ("nickname", "role")}),
    )


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ["user", "can_manage_users", "can_manage_articles", "can_manage_projects"]
    search_fields = ["user__username"]
