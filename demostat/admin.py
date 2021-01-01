from django.contrib import admin

# Register your models here.
from .models import Organisation, Region, Location, Tag, Demo, Link

@admin.register(Demo)
class DemoAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Location)
admin.site.register(Link)
