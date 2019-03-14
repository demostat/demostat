from django.contrib import admin

# Register your models here.
from .models import Organisation, Location, Demo, Link, Tag

admin.site.register(Organisation)
admin.site.register(Location)
admin.site.register(Demo)
admin.site.register(Link)
admin.site.register(Tag)
