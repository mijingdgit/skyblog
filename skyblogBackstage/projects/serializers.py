from typing import Optional

from django.utils.text import slugify
from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'tech_stack',
            'image',
            'github',
            'demo',
            'highlights',
            'order',
            'is_published',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def _build_unique_slug(
        self,
        title: str,
        slug_value: Optional[str],
        instance: Optional[Project] = None,
    ):
        base_slug = slugify((slug_value or '').strip()) or slugify(title) or 'project'
        candidate = base_slug
        suffix = 2

        queryset = Project.objects.all()
        if instance is not None:
            queryset = queryset.exclude(pk=instance.pk)

        while queryset.filter(slug=candidate).exists():
            candidate = f'{base_slug}-{suffix}'
            suffix += 1

        return candidate

    def create(self, validated_data):
        validated_data['slug'] = self._build_unique_slug(
            validated_data.get('title', ''),
            validated_data.get('slug'),
        )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        next_title = validated_data.get('title', instance.title)
        next_slug = validated_data.get('slug', instance.slug)
        validated_data['slug'] = self._build_unique_slug(next_title, next_slug, instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if isinstance(data.get('highlights'), str):
            import json

            data['highlights'] = json.loads(data['highlights']) if data['highlights'] else []
        return data
