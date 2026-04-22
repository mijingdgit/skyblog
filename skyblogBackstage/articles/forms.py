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
from .models import AboutProfile, Article


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
            suffix = Path(source_file.name).suffix.lower()
            try:
                content = extract_content_from_upload(source_file)
            except forms.ValidationError as exc:
                self.add_error("source_file", exc)
            else:
                cleaned_data["content"] = content
                if suffix == ".xmind":
                    source_file.seek(0)
                    cleaned_data["xmind_file"] = self._store_source_file(source_file, cleaned_data.get("title") or source_file.name)
                else:
                    cleaned_data["xmind_file"] = ""
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
        article.xmind_file = self.cleaned_data.get("xmind_file", article.xmind_file)

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

    def _store_source_file(self, uploaded, title: str) -> str:
        suffix = Path(uploaded.name).suffix.lower()
        base_name = slugify(title or Path(uploaded.name).stem) or "xmind"
        file_name = f"{base_name}-{uuid.uuid4().hex[:10]}{suffix}"
        storage_path = f"article-xmind/{file_name}"
        saved_path = default_storage.save(storage_path, ContentFile(uploaded.read()))
        return default_storage.url(saved_path)

    def _clear_field_error(self, field_name: str) -> None:
        if field_name in self.errors:
            del self.errors[field_name]


def split_lines(value: str) -> list[str]:
    return [line.strip() for line in value.splitlines() if line.strip()]


def split_items(value: str) -> list[str]:
    normalized = value.replace("，", ",").replace("、", ",")
    return [item.strip() for item in normalized.split(",") if item.strip()]


def split_pipe_line(line: str, expected: int) -> list[str]:
    parts = [part.strip() for part in line.split("|")]
    return parts + [""] * max(0, expected - len(parts))


class AboutProfileAdminForm(forms.ModelForm):
    intro_paragraphs_text = forms.CharField(
        required=False,
        label="简介段落",
        widget=forms.Textarea(attrs={"rows": 5}),
        help_text="每行一段简介，保存后自动转为前台展示内容。",
    )
    skills_text = forms.CharField(
        required=False,
        label="技能栏",
        widget=forms.Textarea(attrs={"rows": 6}),
        help_text="每行格式：分类 | 技能1, 技能2, 技能3",
    )
    directions_text = forms.CharField(
        required=False,
        label="发展方向",
        widget=forms.Textarea(attrs={"rows": 6}),
        help_text="每行格式：图标 | 标题 | 描述",
    )
    experiences_text = forms.CharField(
        required=False,
        label="项目经历",
        widget=forms.Textarea(attrs={"rows": 6}),
        help_text="每行格式：时间 | 标题 | 组织/项目 | 描述",
    )
    certifications_text = forms.CharField(
        required=False,
        label="证书/学习记录",
        widget=forms.Textarea(attrs={"rows": 4}),
        help_text="每行一条证书或学习记录。",
    )
    tools_text = forms.CharField(
        required=False,
        label="工具与环境",
        widget=forms.Textarea(attrs={"rows": 5}),
        help_text="每行格式：图标 | 名称",
    )
    abilities_text = forms.CharField(
        required=False,
        label="核心能力",
        widget=forms.Textarea(attrs={"rows": 6}),
        help_text="每行格式：图标 | 标题 | 描述",
    )

    class Meta:
        model = AboutProfile
        exclude = (
            "intro_paragraphs",
            "skills",
            "directions",
            "experiences",
            "certifications",
            "tools",
            "abilities",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance:
            return

        self.fields["intro_paragraphs_text"].initial = "\n".join(self.instance.intro_paragraphs or [])
        self.fields["skills_text"].initial = "\n".join(
            f"{item.get('category', '')} | {', '.join(item.get('items') or [])}"
            for item in self.instance.skills or []
        )
        self.fields["directions_text"].initial = "\n".join(
            f"{item.get('icon', '')} | {item.get('title', '')} | {item.get('desc', '')}"
            for item in self.instance.directions or []
        )
        self.fields["experiences_text"].initial = "\n".join(
            f"{item.get('period', '')} | {item.get('title', '')} | {item.get('company', '')} | {item.get('description', '')}"
            for item in self.instance.experiences or []
        )
        self.fields["certifications_text"].initial = "\n".join(self.instance.certifications or [])
        self.fields["tools_text"].initial = "\n".join(
            f"{item.get('icon', '')} | {item.get('name', '')}" for item in self.instance.tools or []
        )
        self.fields["abilities_text"].initial = "\n".join(
            f"{item.get('icon', '')} | {item.get('title', '')} | {item.get('desc', '')}"
            for item in self.instance.abilities or []
        )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["intro_paragraphs"] = split_lines(cleaned_data.get("intro_paragraphs_text", ""))
        cleaned_data["skills"] = self._parse_skills(cleaned_data.get("skills_text", ""))
        cleaned_data["directions"] = self._parse_directions(cleaned_data.get("directions_text", ""))
        cleaned_data["experiences"] = self._parse_experiences(cleaned_data.get("experiences_text", ""))
        cleaned_data["certifications"] = split_lines(cleaned_data.get("certifications_text", ""))
        cleaned_data["tools"] = self._parse_tools(cleaned_data.get("tools_text", ""))
        cleaned_data["abilities"] = self._parse_abilities(cleaned_data.get("abilities_text", ""))
        return cleaned_data

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.intro_paragraphs = self.cleaned_data.get("intro_paragraphs", [])
        profile.skills = self.cleaned_data.get("skills", [])
        profile.directions = self.cleaned_data.get("directions", [])
        profile.experiences = self.cleaned_data.get("experiences", [])
        profile.certifications = self.cleaned_data.get("certifications", [])
        profile.tools = self.cleaned_data.get("tools", [])
        profile.abilities = self.cleaned_data.get("abilities", [])

        if commit:
            profile.save()
            self.save_m2m()

        return profile

    def _parse_skills(self, value: str) -> list[dict[str, object]]:
        result = []
        for line in split_lines(value):
            category, items = split_pipe_line(line, 2)[:2]
            if category:
                result.append({"category": category, "items": split_items(items)})
        return result

    def _parse_directions(self, value: str) -> list[dict[str, str]]:
        result = []
        for line in split_lines(value):
            icon, title, desc = split_pipe_line(line, 3)[:3]
            if title:
                result.append({"icon": icon, "title": title, "desc": desc})
        return result

    def _parse_experiences(self, value: str) -> list[dict[str, str]]:
        result = []
        for line in split_lines(value):
            period, title, company, description = split_pipe_line(line, 4)[:4]
            if title:
                result.append(
                    {
                        "period": period,
                        "title": title,
                        "company": company,
                        "description": description,
                    }
                )
        return result

    def _parse_tools(self, value: str) -> list[dict[str, str]]:
        result = []
        for line in split_lines(value):
            icon, name = split_pipe_line(line, 2)[:2]
            if name:
                result.append({"icon": icon, "name": name})
        return result

    def _parse_abilities(self, value: str) -> list[dict[str, str]]:
        result = []
        for line in split_lines(value):
            icon, title, desc = split_pipe_line(line, 3)[:3]
            if title:
                result.append({"icon": icon, "title": title, "desc": desc})
        return result
