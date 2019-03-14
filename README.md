# Demostat
Statusseite für als nächstes anstehende Demonstrationen in Erfurt.

> Die Software steckt noch in der tiefsten Anfangsphase und ist extrem unvollständig! (Das hält hier aber keinen davon ab, sie trotzdem zu nutzen :P)

![Screenshot Demo Detail](docs/screenshot-demo-detail.png)

> Wie, gestern war wieder eine Demo? Warum weiß ich davon nix?

Leider ist diese Frage hier viel zu oft vorgekommen. Das wollen wir ändern und habe diese Website geschaffen. Auf einem Blick alle Demos der nächsten vier Wochen. Dazu gleich eine Übersichtskarte, wo sich getroffen wird und Links zu offiziellen Aufrufen, Livetickern und anderweitiges Material.

Findet die Demo erst in weiter Zukunft statt oder ist schon lange vorbei? Dann lohnt sich ein Blick in das Archiv. Sortiert nach Jahr, Monat und Tag und (blad) filterbar.

Wer steckt hinter der Demo? Auch das lässt sich ganz einfach herausfinden. Zu jeder Organisation gibt es eine kleine Zusammenfassung mit Links zur Homepage.

## Inhalte
### Startseite
Alle Demos der nächsten vier Wochen aufgelistet nach Datum.

### Archiv
Alle Demos, die eingetragen wurden, sortiert nach Jahr, Monat und Tag.

### Demo
Jeder Demo wir ein Ort und eine Organisation zugeordnet. Neben Name und kurzer Beschreibung ist noch eine Linkliste vorhanden, bei der z.B. auf den offiziellen Aufruf oder Social-Media Kanäle verwiesen werden können.

### Organisation
Jede Organisation hat einen Namen, eine kurze Beschreibung und einen Link zur Homepage.

## Installation
### Eigenständige Entwicklungsversion
Demostat Entwicklungsversion herunterladen:
```
git clone -b dev https://github.com/demostat/demostat.git
```

Abhängigkeiten installieren:
```
pip3 install -r demostat/requirements.txt
```

Neues Django Projekt starten:
```
django-admin startproject mysite
cd mysite
```

Demostat einbinden:
```
ln -s ../demostat/demostat
```

Füge in `mysite/settings.py` Demostat und seine Abhängigkeiten zu `INSTALLED_APPS` hinzu:
```
INSTALLED_APPS = [
  'demostat',
  'taggit',
  ...
]
```
Beachte, dass Django-Admin ebenfalls geladen wird. (In der Standartinstallation sollte das schon geschehen sein)

Binde in `mysite/urls.py` Demostat-Urls ein:
```
from django.urls import include

urlpatterns = [
  path('', include('demostat.urls')),
  ...
]
```

Datenbank-Migrieren:
```
python3 manage.py migrate
```

Erstelle Administrationsaccount:
```
python3 manage.py createsuperuser
```

Starte Webserver:
```
python3 manage.py runserver
```

Website ist erreichbar über:
http://127.0.0.1:8000/

Administration über:
http://127.0.0.1:8000/admin/

## Konfigurationen
Es ist möglich Demostat über Variablen in `mysite/settings.py` zu konfigurieren.

Alle Angaben sind Optional. Entweder haben werden sie durch Vorbelegungen ersetzt oder einfach nicht angzeigt.

### String `SITE_TITLE`
Wird als Titel im Header und der Navigation genutzt.
```
SITE_TITLE = "Demos in Erfurt"
```

### Url `SITE_IMPRINT_URL`
Url zum Impressum, wird im Footer angezeigt.

### Url `SITE_PRIVACY_URL`
Url zur Datenschutzerklärung, wird im Footer angezeigt.

## Lizenz
Diese Software hat **noch** keine Lizenz. Das bedeutet, dass das deutsche Urherberrecht gilt.

Wir arbeiten fleißig daran, dass schnellstmöglich eine passende Lizenz gefunden und diese Projekt darunter veröffentlicht wird.
