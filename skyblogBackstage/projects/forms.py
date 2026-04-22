from pathlib import Path
import uuid

from django import forms
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.text import slugify

from .models import Project, ProjectPageContent


IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}


def split_lines(value: str) -> list[str]:
    return [line.strip() for line in value.splitlines() if line.strip()]


class ProjectAdminForm(forms.ModelForm):
    image_upload = forms.FileField(
        required=False,
        label="项目封面上传",
        help_text="支持上传 JPG、PNG、WEBP、GIF、SVG。上传后会自动写入下方项目封面/图片标识字段。",
    )
    tech_stack_text = forms.CharField(
        required=False,
        label="技术栈",
        widget=forms.Textarea(attrs={"rows": 4}),
        help_text="每行一个技术栈，例如：Vue3",
    )
    highlights_text = forms.CharField(
        required=False,
        label="项目亮点",
        widget=forms.Textarea(attrs={"rows": 4}),
        help_text="每行一个项目亮点，会显示在前台项目卡片中。",
    )

    class Meta:
        model = Project
        exclude = ("tech_stack", "highlights")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["tech_stack_text"].initial = "\n".join(self.instance.tech_stack or [])
            self.fields["highlights_text"].initial = "\n".join(self.instance.highlights or [])

    def clean_image_upload(self):
        uploaded = self.cleaned_data.get("image_upload")
        if not uploaded:
            return uploaded

        suffix = Path(uploaded.name).suffix.lower()
        if suffix not in IMAGE_SUFFIXES:
            raise forms.ValidationError("项目封面仅支持 .jpg、.jpeg、.png、.webp、.gif 或 .svg 文件。")

        return uploaded

    def clean(self):
        cleaned_data = super().clean()

        image_upload = cleaned_data.get("image_upload")
        if image_upload:
            cleaned_data["image"] = self._store_project_image(
                image_upload,
                cleaned_data.get("title") or image_upload.name,
            )
            self._clear_field_error("image")

        cleaned_data["tech_stack"] = split_lines(cleaned_data.get("tech_stack_text", ""))
        cleaned_data["highlights"] = split_lines(cleaned_data.get("highlights_text", ""))
        return cleaned_data

    def save(self, commit=True):
        project = super().save(commit=False)
        project.image = self.cleaned_data.get("image", project.image)
        project.tech_stack = self.cleaned_data.get("tech_stack", project.tech_stack)
        project.highlights = self.cleaned_data.get("highlights", project.highlights)

        if commit:
            project.save()
            self.save_m2m()

        return project

    def _store_project_image(self, uploaded, title: str) -> str:
        suffix = Path(uploaded.name).suffix.lower()
        base_name = slugify(title or Path(uploaded.name).stem) or "project"
        file_name = f"{base_name}-{uuid.uuid4().hex[:10]}{suffix}"
        storage_path = f"project-covers/{file_name}"
        saved_path = default_storage.save(storage_path, ContentFile(uploaded.read()))
        return default_storage.url(saved_path)

    def _clear_field_error(self, field_name: str) -> None:
        if field_name in self.errors:
            del self.errors[field_name]


class ProjectPageContentAdminForm(forms.ModelForm):
    filters_text = forms.CharField(
        required=False,
        label="筛选按钮",
        widget=forms.Textarea(attrs={"rows": 5}),
        help_text="每行一个筛选按钮，格式：key|显示名称。例如：llm|AI / 大模型。key 支持 all、llm、frontend、backend。",
    )

    class Meta:
        model = ProjectPageContent
        exclude = ("filters",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["filters_text"].initial = "\n".join(
                f"{item.get('key', '')}|{item.get('label', '')}"
                for item in self.instance.filters or []
            )

    def clean_filters_text(self):
        value = self.cleaned_data.get("filters_text", "")
        filters = []

        for line in split_lines(value):
            if "|" not in line:
                raise forms.ValidationError("筛选按钮格式必须为：key|显示名称。")

            key, label = [part.strip() for part in line.split("|", 1)]
            if not key or not label:
                raise forms.ValidationError("筛选按钮的 key 和显示名称均不能为空。")

            filters.append({"key": key, "label": label})

        return filters

    def save(self, commit=True):
        page_content = super().save(commit=False)
        page_content.filters = self.cleaned_data.get("filters_text", page_content.filters)

        if commit:
            page_content.save()

        return page_content
