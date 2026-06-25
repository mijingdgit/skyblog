from django.contrib import admin

from .forms import AboutProfileAdminForm, ArticleAdminForm
from .models import AboutProfile, Article, Category, Tag


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
    readonly_fields = ["xmind_file"]
    class Media:
        css = {
            "all": ("admin/css/article-editor.css",)
        }
        js = ("admin/js/article-editor.js",)

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
                "fields": ("source_file", "xmind_file"),
                "description": "上传 Markdown、XMind 或 Word 文件后，页面会自动切换到对应编辑模式；保存时会提取正文，Markdown 中可访问的本地图片也会一并复制到站点媒体目录。",
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


@admin.register(AboutProfile)
class AboutProfileAdmin(admin.ModelAdmin):
    form = AboutProfileAdminForm
    list_display = ["page_title", "name", "title", "is_active", "updated_at"]
    list_filter = ["is_active", "updated_at"]
    search_fields = ["name", "title", "slogan", "page_description"]
    fieldsets = (
        (
            "基础信息",
            {
                "fields": (
                    "is_active",
                    "name",
                    "title",
                    "location",
                    "email",
                    "github",
                    "slogan",
                    "avatar_text",
                ),
            },
        ),
        (
            "页面文案",
            {
                "fields": (
                    "page_title",
                    "page_description",
                    "intro_title",
                    "intro_paragraphs_text",
                ),
                "description": "简介段落改为每行一段，不需要手写 JSON。",
            },
        ),
        (
            "模块数据",
            {
                "fields": (
                    "skills_text",
                    "directions_text",
                    "experiences_text",
                    "certifications_text",
                    "tools_text",
                    "abilities_text",
                ),
                "description": "每个模块使用说明中的分隔格式填写，保存后自动转成前台需要的数据结构。",
            },
        ),
        (
            "联系区域",
            {
                "fields": ("contact_title", "contact_description"),
            },
        ),
    )
