from django.contrib import admin

# Register your models here.
from .models import Organisation, Region, Location, Tag, Demo, Link

class LinkAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None, {
                'fields': [
                    'demo',
                ],

            },
        ),
        (
            None, {
                'fields': [
                    'title',
                    'url',
                ],
            },
        ),
        (
            None, {
                'fields': [
                    'order',
                ],
            },
        ),
    ]

class LinkInline(admin.TabularInline):
    model = Link
    extra = 0

class DemoAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None, {
                'fields': [
                    'slug',
                    'group',
                ],

            },
        ),
        (
            'Über', {
                'fields': [
                    'title',
                    'organisation',
                    'date',
                    'location',
                    'description',
                ],
            },
        ),
        (
            'Weiteres', {
                'fields': [
                    'note',
                    'tags',
                ],
            },
        ),
    ]
    inlines = [
        LinkInline,
    ]

    list_display = (
        'date',
        'title',
    )

    list_filter = [
        'date',
    ]

admin.site.register(Organisation)
admin.site.register(Region)
admin.site.register(Location)
admin.site.register(Tag)
admin.site.register(Demo, DemoAdmin)
admin.site.register(Link, LinkAdmin)
