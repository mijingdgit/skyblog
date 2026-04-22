from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


def default_project_page_filters():
    return [
        {"key": "all", "label": "全部"},
        {"key": "llm", "label": "AI / 大模型"},
        {"key": "frontend", "label": "前端项目"},
        {"key": "backend", "label": "后端项目"},
    ]


class ProjectPageContent(models.Model):
    """项目页展示配置。"""

    title_prefix = models.CharField("标题前半部分", max_length=80, default="项目")
    title_accent = models.CharField("标题强调部分", max_length=80, default="作品")
    description = models.TextField(
        "页面说明",
        default="这里展示的项目内容，已经改为直接读取后台已发布数据。",
    )
    filters = models.JSONField("筛选按钮", default=default_project_page_filters)
    is_active = models.BooleanField("启用", default=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = "skyblog_project_page_content"
        verbose_name = "项目页配置"
        verbose_name_plural = "项目页配置"
        ordering = ["-is_active", "-updated_at"]

    def __str__(self):
        return f"{self.title_prefix}{self.title_accent}"


class Project(models.Model):
    """项目作品。"""

    title = models.CharField("项目名称", max_length=100)
    slug = models.SlugField("URL 标识", unique=True, blank=True)
    description = models.TextField("描述")
    tech_stack = models.JSONField("技术栈", default=list)
    image = models.CharField("项目封面/图片标识", max_length=255, blank=True)
    github = models.URLField("GitHub 链接", blank=True)
    demo = models.URLField("演示链接", blank=True)
    highlights = models.JSONField("项目亮点", default=list)
    order = models.IntegerField("排序", default=0)
    is_published = models.BooleanField("是否发布", default=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = "skyblog_project"
        verbose_name = "项目"
        verbose_name_plural = "项目"
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title
