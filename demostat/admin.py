from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import Organisation, Region, Location, Tag, Demo, Link

@admin.register(Demo)
class DemoAdmin(admin.ModelAdmin):
    search_fields = (
            'slug',
            'title',
            'location__name',
            'organisation__name',
            'description',
            'note',
            'tags',
        )

    prepopulated_fields = {"slug": ("title",)}

    date_hierarchy = 'date'

    list_display = (
            'title',
            'date',
            'location'
        )

    list_filter = (
            ('location', admin.RelatedOnlyFieldListFilter),
            ('tags', admin.RelatedOnlyFieldListFilter),
            ('organisation', admin.RelatedOnlyFieldListFilter),
        )

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = (
            'title',
            'fqdn',
            'demo_name',
            'demo_date',
        )

    search_fields = (
            'title',
            'url',
            'demo__title'
        )

    date_hierarchy = 'demo__date'

    def demo_name(self, obj):
        return obj.demo.title

    def demo_date(self, obj):
        return obj.demo.date

    def fqdn(self, obj):
        return format_html("<a href='{}'>{}</a>", obj.url, obj.fqdn)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
            'name',
            'region'
        )

    list_filter = (
            ('region', admin.RelatedOnlyFieldListFilter),
        )

    search_fields = (
            'name',
            'region__name',
        )

@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = (
            'name',
            'url_fqdn',
        )

    prepopulated_fields = {"slug": ("name",)}

    def url_fqdn(self, obj):
        if not obj.url_fqdn:
            return None

        return format_html("<a href='{}'>{}</a>", obj.url, obj.url_fqdn)

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = (
            'name',
            'group',
        )

    list_filter = (
            ('group', admin.RelatedOnlyFieldListFilter),
        )

    prepopulated_fields = {'slug': ('name',)}

    search_fields = (
            'name',
            'group',
        )

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

    search_fields = (
            'name',
        )
