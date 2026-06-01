==============
HTMx sandkasse
==============

1. Putt koden et sted og stå i samme katalog som denne fila
2. Lag et virtualenv, f.eks::

   $ python3 -m venv .venv && source .venv/bin/activate
3. Installer i virtualenvet::

   $ pip install -e .
4. Lag sqlite databasen::

   $ python manage.py makemigrations
5. Kjør opp sandkasse-siten::

   $ python3 manage.py runserver
6. Besøk `http://127.0.0.1:8000 <http://127.0.0.1:8000/>`_ med browser og hold
   øye med konsoll

Du kan legge til masse bøker vha.::

   $ python3 manage.py import_from_librarything librarything_languagebooks_202605210857.json

Du kan slette databasen og starte på nytt ved å slette fila ``src/db.sqlite3``.
