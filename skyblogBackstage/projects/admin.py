from django.contrib import admin

from .forms import ProjectAdminForm, ProjectPageContentAdminForm
from .models import Project, ProjectPageContent


@admin.register(ProjectPageContent)
class ProjectPageContentAdmin(admin.ModelAdmin):
    form = ProjectPageContentAdminForm
    list_display = ['__str__', 'is_active', 'updated_at']
    list_filter = ['is_active', 'updated_at']
    fieldsets = (
        (
            '页面文案',
            {
                'fields': (
                    'title_prefix',
                    'title_accent',
                    'description',
                    'filters_text',
                    'is_active',
                ),
            },
        ),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    list_display = ['title', 'order', 'is_published', 'created_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order', '-created_at']
    fieldsets = (
        (
            '基础信息',
            {
                'fields': (
                    'title',
                    'slug',
                    'description',
                    'image_upload',
                    'image',
                    'github',
                    'demo',
                    'order',
                    'is_published',
                ),
            },
        ),
        (
            '展示内容',
            {
                'fields': ('tech_stack_text', 'highlights_text'),
                'description': '技术栈和项目亮点均为每行一条，保存后自动转为前台可读取的数据。',
            },
        ),
    )
