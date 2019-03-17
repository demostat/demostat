Installieren
============

Eigenständige Entwicklungsversion
---------------------------------

Demostat Entwicklungsversion herunterladen:

::

    git clone -b dev https://github.com/demostat/demostat.git


Abhängigkeiten installieren:

::

    pip3 install -r demostat/requirements.txt


Neues Django Projekt starten:

::

    django-admin startproject mysite
    cd mysite


Demostat einbinden:

::

    ln -s ../demostat/demostat


Füge in `mysite/settings.py` Demostat zu `INSTALLED_APPS` hinzu:

::

    INSTALLED_APPS = [
      'demostat',
    ...
    ]


Beachte, dass Django-Admin ebenfalls geladen wird. (In der Standartinstallation sollte das schon geschehen sein)

Binde in `mysite/urls.py` Demostat-Urls ein:

::

    from django.urls import include

    urlpatterns = [
      path('', include('demostat.urls')),
      ...
    ]


Datenbank-Migrieren:

::

    python3 manage.py migrate


Erstelle Administrationsaccount:

::

    python3 manage.py createsuperuser


Starte Webserver:

::

    python3 manage.py runserver


Website ist erreichbar über:
http://127.0.0.1:8000/

Administration über:
http://127.0.0.1:8000/admin/
