from django.db import models
from django.utils import timezone

import decimal
import datetime

class Organisation(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    lon = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)

    def marker_lat(self):
        if self.lat:
            return str(float(self.lat))
        else:
            return None

    def marker_lon(self):
        if self.lon:
            return str(float(self.lon))
        else:
            return None

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    def __str__(self):
        return self.name

class Demo(models.Model):
    slug = models.SlugField()
    organisation = models.ForeignKey(Organisation, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    description = models.TextField()
    note = models.TextField(blank=True)
    date = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True)

    def day(self):
        return self.date.date()

    def month(self):
        return datetime.date(self.date.date().year, self.date.date().month, 1)

    def year(self):
        return datetime.date(self.date.date().year, 1, 1)

    def is_next(self):
        return self.date >= timezone.now() and Demo.objects.filter(date__gt=timezone.now(), date__lt=self.date).count() <= 0

    def __str__(self):
        return str(self.date) + '; ' + self.title

class Link(models.Model):
    demo = models.ForeignKey(Demo, on_delete=models.PROTECT)
    title = models.CharField(max_length=30)
    url = models.URLField(max_length=200)

    order = models.IntegerField(default=0)

    def __str__(self):
        return str(self.demo) + '; ' + self.title
