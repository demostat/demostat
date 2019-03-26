from django.contrib import admin

# Register your models here.
from .models import Organisation, Region, Location, Tag, Demo, Link

class OrganisationAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None, {
                'fields': [
                    'slug',
                ],

            },
        ),
        (
            "Über", {
                'fields': [
                    'name',
                    'description',
                    'url',
                ],
            },
        ),
    ]

    list_display = (
        'name',
    )

class RegionAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None, {
                'fields': [
                    'slug',
                ],

            },
        ),
        (
            None, {
                'fields': [
                    'group',
                ],
            },
        ),
        (
            None, {
                'fields': [
                    'name',
                ],
            },
        ),
    ]

    list_display = (
        'name',
    )

class LocationAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None, {
                'fields': [
                    'region',
                ],

            },
        ),
        (
            None, {
                'fields': [
                    'name',
                ],
            },
        ),
        (
            "Koordinaten", {
                'fields': [
                    'lat',
                    'lon',
                ],
            },
        ),
    ]

    list_display = (
        'name',
    )

class TagAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None, {
                'fields': [
                    'slug',
                ],

            },
        ),
        (
            None, {
                'fields': [
                    'name',
                ],
            },
        ),
    ]

    list_display = (
        'name',
    )

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
            "Über", {
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
            "Weiteres", {
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

admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Demo, DemoAdmin)
admin.site.register(Link, LinkAdmin)
