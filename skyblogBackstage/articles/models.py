from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    """文章分类。"""

    name = models.CharField("分类名称", max_length=50)
    slug = models.SlugField("标识", unique=True)
    icon = models.CharField("图标", max_length=10, default="标签")
    description = models.TextField("描述", blank=True)
    order = models.IntegerField("排序", default=0)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        db_table = "skyblog_category"
        verbose_name = "分类"
        verbose_name_plural = "分类"
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.name


class Tag(models.Model):
    """文章标签。"""

    name = models.CharField("标签名称", max_length=30)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        db_table = "skyblog_tag"
        verbose_name = "标签"
        verbose_name_plural = "标签"

    def __str__(self):
        return self.name


class Article(models.Model):
    """文章。"""

    title = models.CharField("标题", max_length=200)
    slug = models.SlugField("URL 标识", unique=True, blank=True)
    excerpt = models.TextField("摘要")
    content = models.TextField("正文")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="articles",
        verbose_name="分类",
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="articles",
        verbose_name="标签",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="articles",
        verbose_name="作者",
    )
    cover = models.CharField("封面图", max_length=200, blank=True)
    views = models.IntegerField("阅读量", default=0)
    is_published = models.BooleanField("是否发布", default=True)
    is_featured = models.BooleanField("是否推荐", default=False)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)
    published_at = models.DateTimeField("发布时间", null=True, blank=True)

    class Meta:
        db_table = "skyblog_article"
        verbose_name = "文章"
        verbose_name_plural = "文章"
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title
