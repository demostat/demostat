# Demostat
Statusseite für als nächstes anstehende Demonstrationen in Erfurt.

![Screenshot Demo Detail](docs/screenshot-demo-detail.png)

> Die Software steckt noch in der tiefsten Anfangsphase und ist extrem unvollständig!

## Demo
Jeder Demo wir ein Ort und eine Organisation zugeordnet. Neben Name und kurzer Beschreibung ist noch eine Linkliste vorhanden, bei der z.B. auf den offiziellen Aufruf oder Social-Media Kanäle verwiesen werden können.

## Installation
### Eigenständige Entwicklungsversion
Demostat herunterladen:
```
git clone https://github.com/demostat/demostat.git
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

Füge `demostat` und Abhängigkeiten zu `INSTALLED_APPS` hinzu:
```
INSTALLED_APPS = [
  'demostat',
  'taggit',
  ...
]
```
Beachte, dass Django-Admin ebenfalls geladen wird.

Binde Demostat-Urls ein:
```
path('', include('demostat.urls')),
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
