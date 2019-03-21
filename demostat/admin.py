from django.contrib import admin

# Register your models here.
from .models import Organisation, Region, Location, Tag, DemoGroup, Demo, Link

admin.site.register(Organisation)
admin.site.register(Region)
admin.site.register(Location)
admin.site.register(Tag)
admin.site.register(DemoGroup)
admin.site.register(Demo)
admin.site.register(Link)
