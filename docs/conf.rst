Konfiguration
=============

Es ist möglich Demostat über Variablen in `mysite/settings.py` zu konfigurieren.

Alle Angaben sind Optional. Entweder haben werden sie durch Vorbelegungen ersetzt oder einfach nicht angzeigt.

String `SITE_TITLE`
-------------------

Wird als Titel im Header und der Navigation genutzt.

::

    SITE_TITLE = "Demos in Erfurt"


Url `SITE_IMPRINT_URL`
----------------------

Url zum Impressum, wird im Footer angezeigt.

Url `SITE_PRIVACY_URL`
----------------------

Url zur Datenschutzerklärung, wird im Footer angezeigt.

Dict `DEMOSTAT_LEAFLET`
-----------------------

Konfiguriere eine eigene Karten-Kachel-Quelle, z.B. für eine Proxy.

::

    DEMOSTAT_LEAFLET = [
      "url": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      "attribution": "Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>",
      "maxZoom": 18,
    ]


Mehr dazu: https://leafletjs.com/reference-1.4.0.html#tilelayer
