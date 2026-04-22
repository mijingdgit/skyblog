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
    xmind_file = models.CharField("XMind 源文件", max_length=255, blank=True)
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


def default_intro_paragraphs():
    return [
        "一名专注于 Python 开发和 AI 应用落地的全栈开发者，喜欢把新技术拆解成可以被实际项目使用的能力。",
        "我的学习路线从 Python、Django、Vue 开始，逐步延伸到大模型应用、知识库问答、自动化工作流和内容生产工具。",
        "这个博客会记录技术学习、项目实践和踩坑经验，也会持续整理 AI 工具链在真实场景中的使用方式。",
    ]


def default_about_skills():
    return [
        {"category": "Python 核心", "items": ["异步编程", "Django", "FastAPI", "自动化脚本"]},
        {"category": "前端技术", "items": ["Vue3", "TypeScript", "Vite", "CSS3"]},
        {"category": "AI 应用", "items": ["RAG", "Agent", "Prompt 工程", "XMind 知识整理"]},
        {"category": "工程部署", "items": ["Docker", "Nginx", "SQLite", "GitHub"]},
    ]


def default_directions():
    return [
        {
            "icon": "AI",
            "title": "大模型应用开发",
            "desc": "关注 LLM 在知识库、自动化办公、学习系统和业务工具中的落地。",
        },
        {
            "icon": "Py",
            "title": "Python 全栈开发",
            "desc": "使用 Django、FastAPI 和 Vue 构建稳定、可维护的 Web 应用。",
        },
        {
            "icon": "Ops",
            "title": "部署与工程化",
            "desc": "整理项目上线、接口联调、资源管理和持续迭代过程中的实践。",
        },
    ]


def default_experiences():
    return [
        {
            "period": "2026 - 至今",
            "title": "SkyBlog 个人技术站",
            "company": "个人项目",
            "description": "基于 Vue3 与 Django 搭建内容发布系统，支持文章、项目、Markdown、XMind 和后台管理。",
        },
        {
            "period": "持续学习",
            "title": "AI 工具链实践",
            "company": "学习记录",
            "description": "围绕大模型、智能体、提示词、知识库和自动化工作流沉淀可复用经验。",
        },
    ]


def default_tools():
    return [
        {"icon": "Code", "name": "VS Code"},
        {"icon": "Git", "name": "Git"},
        {"icon": "API", "name": "Postman"},
        {"icon": "Docker", "name": "Docker"},
        {"icon": "Linux", "name": "Linux"},
        {"icon": "DB", "name": "SQLite"},
    ]


def default_abilities():
    return [
        {"icon": "API", "title": "后端接口开发", "desc": "使用 Django/FastAPI 构建内容管理和业务 API。"},
        {"icon": "Web", "title": "前端页面实现", "desc": "使用 Vue3 和 TypeScript 完成响应式交互页面。"},
        {"icon": "AI", "title": "AI 内容工具", "desc": "将 Markdown、XMind、Word 等学习资料接入内容展示流程。"},
        {"icon": "Ship", "title": "项目上线部署", "desc": "关注部署配置、静态资源、媒体文件和生产环境稳定性。"},
    ]


def default_certifications():
    return ["持续学习 Python / Django / Vue3", "AI 大模型应用实践", "个人技术博客建设"]


class AboutProfile(models.Model):
    """关于页面资料。"""

    name = models.CharField("名称", max_length=80, default="Sky")
    title = models.CharField("身份标题", max_length=120, default="Python 开发者 & AI 应用实践者")
    location = models.CharField("所在地", max_length=80, default="中国")
    email = models.EmailField("联系邮箱", blank=True, default="hello@example.com")
    github = models.URLField("GitHub 链接", blank=True, default="https://github.com")
    slogan = models.CharField("一句话介绍", max_length=200, default="用代码记录学习，用 AI 扩展创造。")
    avatar_text = models.CharField("头像文字", max_length=10, default="S")
    page_title = models.CharField("页面标题", max_length=80, default="关于我")
    page_description = models.CharField(
        "页面描述",
        max_length=200,
        default="探索我的技术旅程和成长轨迹",
    )
    intro_title = models.CharField("简介标题", max_length=120, default="你好，我是 Sky")
    intro_paragraphs = models.JSONField("简介段落", default=default_intro_paragraphs)
    skills = models.JSONField("技能栏", default=default_about_skills)
    directions = models.JSONField("发展方向", default=default_directions)
    experiences = models.JSONField("项目经历", default=default_experiences)
    certifications = models.JSONField("证书/学习记录", default=default_certifications)
    tools = models.JSONField("工具与环境", default=default_tools)
    abilities = models.JSONField("核心能力", default=default_abilities)
    contact_title = models.CharField("联系区标题", max_length=120, default="一起交流技术与 AI 实践")
    contact_description = models.TextField(
        "联系区描述",
        default="如果你对 Python、Django、Vue 或 AI 应用开发感兴趣，欢迎随时联系我交流。",
    )
    is_active = models.BooleanField("启用", default=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = "skyblog_about_profile"
        verbose_name = "关于资料"
        verbose_name_plural = "关于资料"
        ordering = ["-is_active", "-updated_at"]

    def __str__(self):
        return self.page_title
