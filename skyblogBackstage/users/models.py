from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """自定义用户模型。"""

    ROLE_CHOICES = [
        ("admin", "管理员"),
        ("editor", "编辑"),
        ("user", "普通用户"),
    ]

    nickname = models.CharField("昵称", max_length=50, default="")
    avatar = models.ImageField("头像", upload_to="avatars/", blank=True, null=True)
    role = models.CharField("角色", max_length=20, choices=ROLE_CHOICES, default="user")
    phone = models.CharField("手机号", max_length=20, blank=True)
    bio = models.TextField("个人简介", blank=True)
    is_active = models.BooleanField("是否启用", default=True)

    class Meta:
        db_table = "skyblog_user"
        verbose_name = "用户"
        verbose_name_plural = "用户"

    def __str__(self):
        return self.nickname or self.username


class UserPermission(models.Model):
    """用户权限扩展。"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="permission")
    can_manage_users = models.BooleanField("管理用户", default=False)
    can_manage_articles = models.BooleanField("管理文章", default=True)
    can_manage_projects = models.BooleanField("管理项目", default=True)
    can_export_data = models.BooleanField("导出数据", default=False)
    can_import_data = models.BooleanField("导入数据", default=False)

    class Meta:
        db_table = "skyblog_user_permission"
        verbose_name = "用户权限"
        verbose_name_plural = "用户权限"

    def __str__(self):
        return f"{self.user.username} - 权限"
