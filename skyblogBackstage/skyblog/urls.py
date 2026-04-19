"""
URL configuration for SkyBlog backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

admin.site.site_header = 'SkyBlog 管理后台'
admin.site.site_title = 'SkyBlog Admin'
admin.site.index_title = '内容管理中心'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/login/', views.login_view, name='login'),
    path('admin/logout/', views.logout_view, name='logout'),
    path('admin/', views.dashboard, name='dashboard'),
    path('admin/users/', views.users_list, name='users-list'),
    path('admin/articles/', views.articles_list, name='articles-list'),
    path('admin/projects/', views.projects_list, name='projects-list'),
    # API
    path('api/csrf/', views.api_csrf, name='api-csrf'),
    path('api/login/', views.api_login, name='api-login'),
    path('api/logout/', views.api_logout, name='api-logout'),
    path('api/me/', views.api_current_user, name='api-current-user'),
    path('api/export/', views.export_data, name='api-export'),
    path('api/import/', views.import_data, name='api-import'),
    path('api/users/', include('users.urls')),
    path('api/articles/', include('articles.urls')),
    path('api/projects/', include('projects.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
