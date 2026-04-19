from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from users.models import User
from articles.models import Article, Category
from projects.models import Project
import json


def api_csrf(request):
    """Return a CSRF token and ensure the cookie is set for SPA requests."""
    return JsonResponse({'code': 200, 'csrfToken': get_token(request)})


def login_view(request):
    """登录页面"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('/admin/')
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误'})

    return render(request, 'login.html')


def logout_view(request):
    """退出登录"""
    logout(request)
    return redirect('/admin/login/')


@login_required
def dashboard(request):
    """控制台首页"""
    context = {
        'user_count': User.objects.count(),
        'article_count': Article.objects.count(),
        'project_count': Project.objects.count(),
        'published_article_count': Article.objects.filter(is_published=True).count(),
    }
    return render(request, 'dashboard.html', context)


@login_required
def users_list(request):
    """用户列表"""
    users = User.objects.all().order_by('-date_joined')

    # 搜索
    search = request.GET.get('search')
    if search:
        users = users.filter(
            username__icontains=search
        ) | users.filter(
            nickname__icontains=search
        ) | users.filter(
            email__icontains=search
        )

    # 筛选
    role = request.GET.get('role')
    if role:
        users = users.filter(role=role)

    # 分页
    paginator = Paginator(users, 20)
    page = request.GET.get('page', 1)
    users = paginator.get_page(page)

    return render(request, 'users.html', {
        'users': users,
        'search': search,
        'role': role,
        'paginator': paginator,
    })


@login_required
def articles_list(request):
    """文章列表"""
    articles = Article.objects.all().select_related('category', 'author').order_by('-published_at', '-created_at')

    # 搜索
    search = request.GET.get('search')
    if search:
        articles = articles.filter(title__icontains=search) | articles.filter(content__icontains=search)

    # 筛选
    category = request.GET.get('category')
    if category:
        articles = articles.filter(category_id=category)

    is_published = request.GET.get('is_published')
    if is_published is not None:
        articles = articles.filter(is_published=is_published == 'true')

    # 分页
    paginator = Paginator(articles, 20)
    page = request.GET.get('page', 1)
    articles = paginator.get_page(page)

    # 获取分类
    categories = Category.objects.all()

    return render(request, 'articles.html', {
        'articles': articles,
        'categories': categories,
        'search': search,
        'category': category,
        'is_published': is_published,
        'paginator': paginator,
    })


@login_required
def projects_list(request):
    """项目列表"""
    projects = Project.objects.all().order_by('-order', '-created_at')

    # 搜索
    search = request.GET.get('search')
    if search:
        projects = projects.filter(title__icontains=search) | projects.filter(description__icontains=search)

    # 筛选
    is_published = request.GET.get('is_published')
    if is_published is not None:
        projects = projects.filter(is_published=is_published == 'true')

    # 分页
    paginator = Paginator(projects, 20)
    page = request.GET.get('page', 1)
    projects = paginator.get_page(page)

    return render(request, 'projects.html', {
        'projects': projects,
        'search': search,
        'is_published': is_published,
        'paginator': paginator,
    })


# API 视图
@csrf_exempt
def api_login(request):
    """API 登录"""
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(request, username=data.get('username'), password=data.get('password'))
        if user and user.is_active:
            login(request, user)
            return JsonResponse({'code': 200, 'message': '登录成功', 'data': {'username': user.username, 'nickname': user.nickname}})
        return JsonResponse({'code': 401, 'message': '用户名或密码错误'})
    return JsonResponse({'code': 405, 'message': '不支持的请求方法'})


def api_logout(request):
    """API 登出"""
    logout(request)
    return JsonResponse({'code': 200, 'message': '登出成功'})


def api_current_user(request):
    """获取当前用户"""
    if not request.user.is_authenticated:
        return JsonResponse({'code': 401, 'message': '未登录'})
    return JsonResponse({
        'code': 200,
        'data': {
            'username': request.user.username,
            'nickname': request.user.nickname,
            'role': request.user.role,
            'email': request.user.email
        }
    })


# 数据导入导出
@login_required
def export_data(request):
    """导出数据"""
    articles = Article.objects.all().values()
    projects = Project.objects.all().values()

    from django.http import JsonResponse
    return JsonResponse({
        'articles': list(articles),
        'projects': list(projects)
    })


@login_required
def import_data(request):
    """导入数据"""
    if request.method == 'POST':
        data = json.loads(request.body)

        if data.get('articles'):
            for article_data in data['articles']:
                Article.objects.update_or_create(
                    id=article_data.get('id'),
                    defaults=article_data
                )

        if data.get('projects'):
            for project_data in data['projects']:
                Project.objects.update_or_create(
                    id=project_data.get('id'),
                    defaults=project_data
                )

        return JsonResponse({'code': 200, 'message': '导入成功'})

    return JsonResponse({'code': 405, 'message': '不支持的请求方法'})
