from django.db import models
from django.core.validators import MinLengthValidator, FileExtensionValidator
from django.utils.text import slugify
from django.urls import reverse
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.lexers import guess_lexer
import os
from datetime import datetime


def section_image_upload_path(instance, filename):
    """Generate upload path for section images using slugified title"""
    base_filename, file_extension = os.path.splitext(filename)
    return f'sections/{slugify(instance.title)}/{slugify(base_filename)}{file_extension}'

def banners_image_upload_path(instance, filename):
    base_filename, file_extenstion = os.path.splitext(filename)
    return f'blogs/{slugify(instance.title)}/{slugify(base_filename)}{file_extenstion}'

class Section(models.Model):
    class ProgrammingLanguage(models.TextChoices):
        PYTHON = 'python', 'Python'
        JAVASCRIPT = 'javascript', 'JavaScript'
        HTML = 'html', 'HTML'
        CSS = 'css', 'CSS'
        SQL = 'sql', 'SQL'
        BASH = 'bash', 'Bash'
        GENERIC = 'text', 'Generic Text'

    title = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(5)],
        help_text="Title of the section (5-100 characters)"
    )

    description = models.TextField(
        max_length=500,
        blank=True,
        help_text="Optional description of the section (max 500 characters)"
    )

    image = models.ImageField(
        upload_to=section_image_upload_path,
        blank=True,
        null=True,
        help_text="Optional image for the section",
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png',])]
    )

    code_snippet = models.TextField(
        blank=True,
        help_text="Code snippet to display with syntax highlighting"
    )

    language = models.CharField(
        max_length=20,
        choices=ProgrammingLanguage.choices,
        default=ProgrammingLanguage.PYTHON,
        help_text="Programming language for syntax highlighting"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Blog Section'
        verbose_name_plural = 'Blog Sections'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-detect language if not specified"""
        if self.code_snippet and not self.language:
            try:
                self.language = guess_lexer(self.code_snippet).name.lower()
            except:
                self.language = self.ProgrammingLanguage.GENERIC
        super().save(*args, **kwargs)

    @property
    def highlighted_code(self):
        """Returns highlighted HTML version of the code snippet"""
        if not self.code_snippet:
            return ""

        try:
            lexer = get_lexer_by_name(self.language)
            formatter = HtmlFormatter(linenos=False, cssclass="codehilite")
            return highlight(self.code_snippet, lexer, formatter)
        except:
            return f"<pre><code>{self.code_snippet}</code></pre>"

    @property
    def css_styles(self):
        """Returns Pygments CSS styles for the highlighted code"""
        return HtmlFormatter().get_style_defs('.codehilite')


class Blog(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        ARCHIVED = 'AR', 'Archived'

    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(10)],
        help_text="Title of the blog post (10-200 characters)"
    )
    banner = models.ImageField(
        upload_to=banners_image_upload_path,
        blank=False,
        null=False,
        help_text="The main banner for the post",
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png',])],
        default='temp/blog_image_default.png',
                    )
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish_date',
        help_text="URL-friendly version of the title"
    )

    summary = models.TextField(
        max_length=500,
        help_text="Brief summary of the blog post"
    )

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
        help_text="Current publication status"
    )

    publish_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date when the blog was published"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    sections = models.ManyToManyField(
        'Section',
        through='BlogSection',
        related_name='blogs',
        help_text="Sections contained in this blog post"
    )

    tags = models.ManyToManyField(
        'Tag',
        related_name='blogs',
        blank=True,
        help_text="Tags for categorizing the blog post"
    )

    class Meta:
        ordering = ['-publish_date']
        indexes = [
            models.Index(fields=['-publish_date']),
            models.Index(fields=['status']),
        ]
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == self.Status.PUBLISHED and not self.publish_date:
            self.publish_date = datetime.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:blog_details', args=[
            self.slug
        ])

    @property
    def is_published(self):
        return self.status == self.Status.PUBLISHED

    @property
    def ordered_sections(self):
        """Returns sections in their defined order"""
        return self.sections.through.objects.filter(
            blog=self
        ).order_by('order').select_related('section')


class BlogSection(models.Model):
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='blog_sections'
    )
    section = models.ForeignKey(
        'Section',
        on_delete=models.CASCADE,
        related_name='blog_sections'
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Order of the section within the blog"
    )

    class Meta:
        ordering = ['order']
        unique_together = ['blog', 'section']


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, validators=[MinLengthValidator(5)])
    slug = models.SlugField(max_length=60, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
