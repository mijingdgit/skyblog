---
title: Django REST Framework 给博客做公开 API：序列化、权限与发布状态
slug: drf-public-api-for-blog
excerpt: 记录用 Django REST Framework 为博客前台提供文章、分类和标签接口时，序列化字段、公开读取权限和发布状态过滤的关键设计。
category_slug: python-ai
category_name: Python
category_icon: PY
category_description: Python、AI 应用、自动化脚本与后端实践。
category_order: 1
tags: Django, DRF, API, Python, 后端
published_at: 2026-04-21
is_published: true
is_featured: false
views: 0
---

## 为什么博客也需要 API 设计

个人博客的后端看起来只是增删改查，但只要前台和后台分离，就会遇到 API 设计问题。比如：前台只能看到已发布文章，后台可以看到草稿；文章详情要返回分类名称和标签；阅读量可以公开增加，但不能让未登录用户随便改正文。

Django REST Framework 的优势是可以把这些规则集中到 ViewSet、Serializer 和 Permission 里，让接口行为清楚可控。

## 模型关系

博客文章通常至少有三类数据：

1. `Category`：分类，一篇文章属于一个分类。
2. `Tag`：标签，一篇文章可以有多个标签。
3. `Article`：正文、摘要、发布状态、阅读量、发布时间。

文章模型可以保留 `is_published` 和 `published_at` 两个字段。前者决定是否可见，后者决定排序和展示日期。

## Serializer 字段设计

前台展示文章列表时，只拿分类 id 不够，还需要分类名称。DRF 可以用 `source` 提供只读字段：

```python
class ArticleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "excerpt",
            "content",
            "category",
            "category_name",
            "tags",
            "tag_ids",
            "views",
            "is_published",
            "published_at",
        ]
```

这里有一个常见取舍：读接口返回嵌套标签对象，写接口用 `tag_ids`。这样前台展示方便，后台保存也简单。

## 公开读取，登录写入

博客前台应该允许匿名读取，但文章创建、编辑、删除需要登录。可以直接使用：

```python
permission_classes = [IsAuthenticatedOrReadOnly]
```

这个权限类适合内容站点。`GET`、`HEAD`、`OPTIONS` 可以匿名访问，写操作需要认证。

## 发布状态过滤

同一个接口在前台和后台的可见范围不同。一个实用写法是在 `get_queryset` 里判断用户是否登录：

```python
def get_queryset(self):
    queryset = Article.objects.all().order_by("-published_at", "-created_at")

    if not self.request.user.is_authenticated:
        queryset = queryset.filter(is_published=True)

    is_published = self.request.query_params.get("is_published")
    if is_published is not None:
        queryset = queryset.filter(is_published=is_published == "true")

    return queryset.distinct()
```

这样匿名用户只能看到已发布内容，后台管理页可以根据筛选条件查看草稿或已发布文章。

## 阅读量接口

阅读量适合单独做一个 action，而不是让前台提交整篇文章更新：

```python
@action(detail=True, methods=["post"], permission_classes=[AllowAny])
def increment_view(self, request, pk=None):
    article = self.get_object()
    Article.objects.filter(pk=article.pk).update(views=models.F("views") + 1)
    article.refresh_from_db(fields=["views"])
    return Response({"views": article.views})
```

这里使用 `F` 表达式避免并发请求互相覆盖。虽然个人博客访问量可能不大，但这是一个低成本的好习惯。

## Slug 的处理

文章 URL 标识建议使用唯一 slug。中文标题可以保留为展示标题，slug 使用英文短语，例如：

```text
drf-public-api-for-blog
vue3-admin-article-flow
```

保存时可以生成唯一 slug，遇到重复就追加数字后缀。这样链接更稳定，也更适合分享和 SEO。

## 小结

DRF 做博客 API 时，重点不是把所有字段暴露出去，而是把“谁能看到什么、谁能修改什么、列表如何筛选”写清楚。只要权限、序列化和查询集边界稳定，前台页面就能放心消费接口。
