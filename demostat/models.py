from django.db import models
from django.utils import timezone

import decimal
import datetime

class Organisation(models.Model):
    """
    Der Veranstalter einer Demo
    """
    slug = models.SlugField()
    name = models.CharField(max_length=200)

    description = models.TextField(blank=True)
    url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class Region(models.Model):
    """
    Mehrere Orte bilden eine Region. Alle Demos einer Region werden dann zusammen angezeigt
    """
    slug = models.SlugField("Slug")
    group = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, verbose_name="Gruppe")
    name = models.CharField("Name", max_length=200)

    def locations_helper(self, start):
        locs = []
        locs += self.location_set.all()

        for region in self.region_set.all():
            if region != start:
                locs += region.locations_helper(start)

        return locs

    def locations(self):
        """
        Alle Orte, die auf die eigene und alle Kind-Regionen zeigen als Array

        Übergibt sich selbst als startparameter und wird immer weiter durchgereicht, um bei möglichen rekursionen rechtzeitig abbrechen zu können
        """
        return self.locations_helper(self)

    def scheduled_helper(self, start):
        out = Demo.objects.filter(date__gt=timezone.now().date(), location__region=self).count()

        for region in self.region_set.all():
            if region != start:
                out += region.scheduled_helper(start)

        return out

    def scheduled(self):
        """
        Anzahl künfitiger Veranstaltungen

        Übergibt sich selbst als startparameter und wird immer weiter durchgereicht, um bei möglichen rekursionen rechtzeitig abbrechen zu können
        """
        return self.scheduled_helper(self)

    def scheduled_month_helper(self, start):
        out = Demo.objects.filter(date__gt=timezone.now().date(), date__lt=timezone.now().date()+datetime.timedelta(weeks=4), location__region=self).count()

        for region in self.region_set.all():
            if region != start:
                out += region.scheduled_month_helper(start)

        return out

    def scheduled_month(self):
        """
        Anzahl Veranstaltungen im nächten Monat

        Übergibt sich selbst als startparameter und wird immer weiter durchgereicht, um bei möglichen rekursionen rechtzeitig abbrechen zu können
        """
        return self.scheduled_month_helper(self)

    def upcoming(self):
        """
        Anzahl  nur in diesem Monat an diesem Ort stattfindende Demos
        """

        return Demo.objects.filter(date__gt=timezone.now().date(), date__lt=timezone.now().date()+datetime.timedelta(weeks=4), location__region=self).count()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ort"
        verbose_name_plural = "Orte"

        ordering = ['name']


class Location(models.Model):
    """
    Ein Ort einer Demonstration
    """
    name = models.CharField("Name", max_length=200)

    region = models.ForeignKey(Region, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Ort")

    lat = models.DecimalField("Latitude", max_digits=22, decimal_places=16, blank=True, null=True, help_text="Breitengrad")
    lon = models.DecimalField("Longitude", max_digits=22, decimal_places=16, blank=True, null=True, help_text="Längengrad")

    def marker_lat(self):
        return str(float(self.lat))

    def marker_lon(self):
        return str(float(self.lon))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Standort"
        verbose_name_plural = "Standorte"

        ordering = ['name']


class Tag(models.Model):
    """
    Demos können durch Tags kategorisiert werden
    """
    slug = models.SlugField("Slug")

    name = models.CharField("Name", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

        ordering = ['name']

class Demo(models.Model):
    """
    Eine Demo, eine Veranstaltung, ein Ort
    """
    slug = models.SlugField("Slug")
    group = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, verbose_name="Gruppe")

    title = models.CharField("Titel", max_length=200)
    organisation = models.ManyToManyField(Organisation, verbose_name="Organisation")
    date = models.DateTimeField("Datum")
    location = models.ForeignKey(Location, on_delete=models.PROTECT, verbose_name="Ort")

    description = models.TextField("Beschreibung")
    note = models.TextField("Anmerkungen", blank=True)

    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Tags")

    def __date(self):
        """
        Gebe die Zeit in der aktuellen Zeitzone zurück.
        Django macht im Backend alles mittels UTC.
        """
        return timezone.localtime(self.date)

    def day(self):
        return datetime.date(self.__date().year, self.__date().month, self.__date().day)

    def month(self):
        return datetime.date(self.__date().year, self.__date().month, 1)

    def year(self):
        return datetime.date(self.__date().year, 1, 1)

    def is_next(self):
        return self.date >= timezone.now() and Demo.objects.filter(date__gt=timezone.now(), date__lt=self.date).count() <= 0

    def __str__(self):
        return str(self.__date()) + "; " + self.title

    class Meta:
        verbose_name = "Demo"
        verbose_name_plural = "Demos"

        ordering = ['date', 'title']

class Link(models.Model):
    """
    Zu Demonstartionen können Links hinzugefügt werden
    """
    demo = models.ForeignKey(Demo, on_delete=models.PROTECT, verbose_name="Demo")

    title = models.CharField("Titel", max_length=30)
    url = models.URLField("Url", max_length=200)

    order = models.IntegerField("Reihenfolge", default=0)

    def __str__(self):
        return str(self.demo) + "; " + self.title

    class Meta:
        verbose_name = "Link"
        verbose_name_plural = "Links"
