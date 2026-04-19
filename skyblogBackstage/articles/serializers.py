from typing import Optional

from django.utils.text import slugify
from rest_framework import serializers

from .models import Article, Category, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_at']


class CategorySerializer(serializers.ModelSerializer):
    article_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'description', 'order', 'article_count', 'created_at']

    def get_article_count(self, obj):
        return obj.articles.filter(is_published=True).count()


class ArticleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    author_name = serializers.CharField(source='author.nickname', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'category', 'category_name',
            'tags', 'tag_ids', 'author', 'author_name', 'cover', 'views',
            'is_published', 'is_featured', 'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = ['id', 'views', 'created_at', 'updated_at']

    def _build_unique_slug(
        self,
        title: str,
        slug_value: Optional[str],
        instance: Optional[Article] = None,
    ):
        base_slug = slugify((slug_value or '').strip()) or slugify(title) or 'article'
        candidate = base_slug
        suffix = 2

        queryset = Article.objects.all()
        if instance is not None:
            queryset = queryset.exclude(pk=instance.pk)

        while queryset.filter(slug=candidate).exists():
            candidate = f'{base_slug}-{suffix}'
            suffix += 1

        return candidate

    def create(self, validated_data):
        tag_ids = validated_data.pop('tag_ids', [])
        validated_data['slug'] = self._build_unique_slug(
            validated_data.get('title', ''),
            validated_data.get('slug'),
        )
        article = Article.objects.create(**validated_data)
        if tag_ids:
            article.tags.set(tag_ids)
        return article

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop('tag_ids', None)
        next_title = validated_data.get('title', instance.title)
        next_slug = validated_data.get('slug', instance.slug)
        validated_data['slug'] = self._build_unique_slug(next_title, next_slug, instance)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tag_ids is not None:
            instance.tags.set(tag_ids)
        return instance
