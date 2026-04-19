from django.contrib import admin

from .forms import ArticleAdminForm
from .models import Article, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "icon", "order", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["order"]
    search_fields = ["name", "description"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    search_fields = ["name"]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = [
        "title",
        "category",
        "author",
        "is_published",
        "is_featured",
        "views",
        "published_at",
    ]
    list_filter = ["is_published", "is_featured", "category", "created_at"]
    search_fields = ["title", "excerpt", "content"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    ordering = ["-published_at", "-created_at"]
    autocomplete_fields = ["author", "category", "tags"]
    fieldsets = (
        (
            "内容导入",
            {
                "fields": ("source_file",),
                "description": "上传 Markdown、XMind 或 Word 文件后，保存时会自动提取正文；Markdown 中可访问的本地图片也会一并复制到站点媒体目录。",
            },
        ),
        (
            "文章信息",
            {
                "fields": (
                    "title",
                    "slug",
                    "excerpt",
                    "content",
                    "category",
                    "tags",
                    "author",
                    "cover_upload",
                    "cover",
                    "is_published",
                    "is_featured",
                    "published_at",
                ),
            },
        ),
    )
