from django.contrib import admin
from django.utils.html import format_html
from pygments.formatters.html import HtmlFormatter
from .models import Blog, Section, BlogSection, Tag
from datetime import timezone


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'created_at', 'updated_at')
    list_filter = ('language', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at', 'highlighted_code_preview')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'language')
        }),
        ('Media', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
        ('Code', {
            'fields': ('code_snippet', 'highlighted_code_preview')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def highlighted_code_preview(self, obj):
        if obj.code_snippet:
            return format_html(obj.highlighted_code)
        return "No code snippet"
    highlighted_code_preview.short_description = "Code Preview"


class BlogSectionInline(admin.TabularInline):
    model = BlogSection
    extra = 1
    ordering = ('order',)
    raw_id_fields = ('section',)
    autocomplete_fields = ['section']


class BlogSectionInline(admin.TabularInline):
    model = BlogSection
    extra = 1
    ordering = ('order',)
    raw_id_fields = ('section',)
    autocomplete_fields = ['section']


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'publish_date', 'is_published')
    list_filter = ('status', 'publish_date', 'tags')
    search_fields = ('title', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'get_absolute_url_link')
    date_hierarchy = 'publish_date'
    filter_horizontal = ('tags',)
    inlines = [BlogSectionInline]
    actions = ['publish_selected', 'archive_selected']

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'summary', 'status')
        }),
        ('Publication', {
            'fields': ('publish_date',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'get_absolute_url_link'),
            'classes': ('collapse',)
        })
    )

    def get_absolute_url_link(self, obj):
        if obj.pk:
            return format_html('<a href="{}" target="_blank">View on site</a>', obj.get_absolute_url())
        return "Save first to get URL"

    get_absolute_url_link.short_description = "Public URL"

    @admin.action(description='Publish selected blogs')
    def publish_selected(self, request, queryset):
        updated = queryset.update(status=Blog.Status.PUBLISHED, publish_date=timezone.now())
        self.message_user(request, f'{updated} blogs published successfully')

    @admin.action(description='Archive selected blogs')
    def archive_selected(self, request, queryset):
        updated = queryset.update(status=Blog.Status.ARCHIVED)
        self.message_user(request, f'{updated} blogs archived successfully')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogSection)
class BlogSectionAdmin(admin.ModelAdmin):
    list_display = ('blog', 'section', 'order')
    list_editable = ('order',)
    list_filter = ('blog',)
    raw_id_fields = ('blog', 'section')
    ordering = ('blog', 'order')