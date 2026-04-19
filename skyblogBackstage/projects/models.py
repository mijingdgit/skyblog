from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Project(models.Model):
    """项目作品。"""

    title = models.CharField("项目名称", max_length=100)
    slug = models.SlugField("URL 标识", unique=True, blank=True)
    description = models.TextField("描述")
    tech_stack = models.JSONField("技术栈", default=list)
    image = models.CharField("图片标识", max_length=50, blank=True)
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
