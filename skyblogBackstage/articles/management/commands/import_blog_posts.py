from __future__ import annotations

from datetime import datetime, time
from pathlib import Path
import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.utils.text import slugify

from articles.models import Article, Category, Tag


class Command(BaseCommand):
    help = "Import curated Markdown blog posts from content/blog-posts into the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--source",
            default=str(settings.BASE_DIR / "content" / "blog-posts"),
            help="Directory containing Markdown posts with front matter.",
        )

    def handle(self, *args, **options):
        source_dir = Path(options["source"]).resolve()
        if not source_dir.exists():
            raise CommandError(f"Source directory does not exist: {source_dir}")

        posts = sorted(source_dir.rglob("*.md"))
        if not posts:
            self.stdout.write(self.style.WARNING(f"No Markdown posts found in {source_dir}"))
            return

        author = self._default_author()
        created_count = 0
        updated_count = 0

        for post_path in posts:
            metadata, content = self._read_post(post_path)
            article, created = self._upsert_article(metadata, content, author)
            created_count += int(created)
            updated_count += int(not created)
            action = "created" if created else "updated"
            self.stdout.write(f"{action}: #{article.id} {article.title}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {len(posts)} posts: {created_count} created, {updated_count} updated."
            )
        )

    def _read_post(self, post_path: Path) -> tuple[dict[str, str], str]:
        text = post_path.read_text(encoding="utf-8-sig").strip()
        if not text.startswith("---"):
            raise CommandError(f"Missing front matter in {post_path}")

        parts = text.split("---", 2)
        if len(parts) < 3:
            raise CommandError(f"Invalid front matter in {post_path}")

        metadata: dict[str, str] = {}
        for line in parts[1].splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if ":" not in stripped:
                raise CommandError(f"Invalid front matter line in {post_path}: {line}")
            key, value = stripped.split(":", 1)
            metadata[key.strip()] = value.strip().strip('"').strip("'")

        content = parts[2].strip()
        if not content:
            raise CommandError(f"Post body is empty: {post_path}")

        return metadata, content

    def _upsert_article(self, metadata: dict[str, str], content: str, author):
        title = self._required(metadata, "title")
        slug = slugify(self._required(metadata, "slug"))
        if not slug:
            raise CommandError(f"Post slug must contain ASCII letters, numbers, or hyphens: {title}")

        category = self._category_for(metadata)
        tags = self._tags_for(metadata.get("tags", ""))

        defaults = {
            "title": title,
            "excerpt": self._required(metadata, "excerpt"),
            "content": content,
            "category": category,
            "author": author,
            "cover": metadata.get("cover", ""),
            "is_published": self._bool_value(metadata.get("is_published"), True),
            "is_featured": self._bool_value(metadata.get("is_featured"), False),
            "published_at": self._published_at(metadata.get("published_at")),
        }

        article = Article.objects.filter(slug=slug).first()
        if article is None:
            article = Article.objects.create(
                slug=slug,
                views=self._int_value(metadata.get("views"), 0),
                **defaults,
            )
            created = True
        else:
            for field, value in defaults.items():
                setattr(article, field, value)
            article.save()
            created = False

        article.tags.set(tags)
        return article, created

    def _category_for(self, metadata: dict[str, str]) -> Category:
        slug = slugify(self._required(metadata, "category_slug"))
        if not slug:
            raise CommandError(f"Invalid category_slug for post: {metadata.get('title', '')}")

        category, _ = Category.objects.get_or_create(
            slug=slug,
            defaults={
                "name": metadata.get("category_name", slug),
                "icon": metadata.get("category_icon", slug[:6].upper()),
                "description": metadata.get("category_description", ""),
                "order": self._int_value(metadata.get("category_order"), 0),
            },
        )

        changed_fields = []
        for field, value in {
            "name": metadata.get("category_name", category.name),
            "icon": metadata.get("category_icon", category.icon),
            "description": metadata.get("category_description", category.description),
            "order": self._int_value(metadata.get("category_order"), category.order),
        }.items():
            if getattr(category, field) != value:
                setattr(category, field, value)
                changed_fields.append(field)

        if changed_fields:
            category.save(update_fields=changed_fields)

        return category

    def _tags_for(self, raw_tags: str) -> list[Tag]:
        names = [
            item.strip()
            for item in re.split(r"[,，、]", raw_tags)
            if item.strip()
        ]
        return [Tag.objects.get_or_create(name=name)[0] for name in names]

    def _published_at(self, raw_value: str | None):
        if not raw_value:
            return None

        raw_value = raw_value.strip()
        try:
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw_value):
                date_value = datetime.fromisoformat(raw_value).date()
                value = datetime.combine(date_value, time(hour=9))
            else:
                value = datetime.fromisoformat(raw_value)
        except ValueError as exc:
            raise CommandError(f"Invalid published_at value: {raw_value}") from exc

        if timezone.is_naive(value):
            return timezone.make_aware(value, timezone.get_current_timezone())
        return value

    def _default_author(self):
        User = get_user_model()
        return User.objects.filter(is_superuser=True).first() or User.objects.first()

    def _required(self, metadata: dict[str, str], key: str) -> str:
        value = metadata.get(key, "").strip()
        if not value:
            raise CommandError(f"Missing required front matter value: {key}")
        return value

    def _bool_value(self, raw_value: str | None, default: bool) -> bool:
        if raw_value is None or raw_value == "":
            return default
        return raw_value.strip().lower() in {"1", "true", "yes", "y", "on"}

    def _int_value(self, raw_value: str | None, default: int) -> int:
        if raw_value is None or raw_value == "":
            return default
        try:
            return int(raw_value)
        except ValueError as exc:
            raise CommandError(f"Invalid integer value: {raw_value}") from exc
