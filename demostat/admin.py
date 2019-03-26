from django.contrib import admin
from django import forms

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

class LocationInline(admin.TabularInline):
    model = Location
    extra = 0

class RegionAdmin(admin.ModelAdmin):
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
                    'name',
                ],
            },
        ),
    ]
    inlines = [
        LocationInline,
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
            "Über", {
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
            "Über", {
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
            "Über", {
                'fields': [
                    'title',
                    'url',
                ],
            },
        ),
        (
            "Weiteres", {
                'fields': [
                    'order',
                ],
            },
        ),
    ]

class LinkInline(admin.TabularInline):
    model = Link
    extra = 0

class DemoForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        slug = cleaned_data.get('slug')
        date = cleaned_data.get('date')

        if Demo.objects.filter(date__year=date.year, date__month=date.month, date__day=date.day, slug=slug).count():
            raise forms.ValidationError(
                "Der Slug existiert schon an diesem Tag."
            )

class DemoAdmin(admin.ModelAdmin):
    form = DemoForm

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
