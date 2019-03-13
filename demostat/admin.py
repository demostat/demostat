from django.contrib import admin

# Register your models here.
from .models import Organisation, Location, Demo, Link

admin.site.register(Organisation)
admin.site.register(Location)
admin.site.register(Demo)
admin.site.register(Link)
