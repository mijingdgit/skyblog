from pathlib import Path
import uuid

from django import forms
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.text import slugify

from .importers import (
    SUPPORTED_IMPORT_SUFFIXES,
    extract_content_from_upload,
    infer_excerpt,
    infer_title,
    normalize_markdown_assets,
)
from .models import Article


IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


class ArticleAdminForm(forms.ModelForm):
    source_file = forms.FileField(
        required=False,
        label="内容源文件",
        help_text="支持导入 .md、.markdown、.xmind、.docx、.doc 文件。选择文件后保存，系统会自动识别 Markdown 正文与图片。",
    )
    cover_upload = forms.ImageField(
        required=False,
        label="封面图片上传",
        help_text="支持上传 JPG、PNG、WEBP、GIF。上传后会自动写入下方封面图字段。",
    )

    class Meta:
        model = Article
        fields = "__all__"

    def clean_source_file(self):
        uploaded = self.cleaned_data.get("source_file")
        if not uploaded:
            return uploaded

        suffix = Path(uploaded.name).suffix.lower()
        if suffix not in SUPPORTED_IMPORT_SUFFIXES:
            raise forms.ValidationError("仅支持导入 .md、.markdown、.xmind、.docx 或 .doc 文件。")

        return uploaded

    def clean_cover_upload(self):
        uploaded = self.cleaned_data.get("cover_upload")
        if not uploaded:
            return uploaded

        suffix = Path(uploaded.name).suffix.lower()
        if suffix not in IMAGE_SUFFIXES:
            raise forms.ValidationError("封面图仅支持 .jpg、.jpeg、.png、.webp 或 .gif 文件。")

        return uploaded

    def clean(self):
        cleaned_data = super().clean()

        source_file = cleaned_data.get("source_file")
        if source_file:
            try:
                content = extract_content_from_upload(source_file)
            except forms.ValidationError as exc:
                self.add_error("source_file", exc)
            else:
                cleaned_data["content"] = content
                if not cleaned_data.get("title", "").strip():
                    cleaned_data["title"] = infer_title(content, source_file.name)
                if not cleaned_data.get("excerpt", "").strip():
                    cleaned_data["excerpt"] = infer_excerpt(content)
                self._clear_field_error("title")
                self._clear_field_error("excerpt")
                self._clear_field_error("content")
        elif cleaned_data.get("content"):
            cleaned_data["content"] = normalize_markdown_assets(cleaned_data["content"])

        cover_upload = cleaned_data.get("cover_upload")
        if cover_upload:
            cover_path = self._store_cover_file(cover_upload, cleaned_data.get("title", "cover"))
            cleaned_data["cover"] = cover_path
            self._clear_field_error("cover")

        return cleaned_data

    def save(self, commit=True):
        article = super().save(commit=False)
        article.cover = self.cleaned_data.get("cover", article.cover)
        article.content = self.cleaned_data.get("content", article.content)

        if commit:
            article.save()
            self.save_m2m()

        return article

    def _store_cover_file(self, uploaded, title: str) -> str:
        suffix = Path(uploaded.name).suffix.lower()
        base_name = slugify(title or Path(uploaded.name).stem) or "cover"
        file_name = f"{base_name}-{uuid.uuid4().hex[:10]}{suffix}"
        storage_path = f"article-covers/{file_name}"
        saved_path = default_storage.save(storage_path, ContentFile(uploaded.read()))
        return default_storage.url(saved_path)

    def _clear_field_error(self, field_name: str) -> None:
        if field_name in self.errors:
            del self.errors[field_name]
