========
Oppgaver
========

Tradisjonen tro brukes en bok-database som eksempel.

I ``src/`` i Django-appen "app" er det en Django-site som endrer de samme
dataene på fire forskjellige måter, både med class based views (cbv) og
function based views (fbv).

"multifield" er veldig klassisk Django bortsett fra at hver bok ikke
har en egen side.

"singlefield", "singlefield-htmx-get" og "singlefield-htmx-boost" gjør
alle det samme; lar deg enkelt endre en type data om ei bok om gangen.

"singlefield" åpner en ny side per felt. De to andre viser fram to
forskjellige måter å gjøre det samme med htmx, uten å flytte seg vekk
fra bok-listen. "singlefield-htmx-boost" bruker Ajax og viser hvordan
man kan konfigurere HTMx.

Django
======

Se `https://www.djangoproject.com/`_.

HTMx
====

Se `https://htmx.org/`_. Det er ikke noe om hva man gjør på serveren på denne
siten, vi må lage vår egen dok.

1 Oppstart
==========

1. Få sandkassen opp å kjøre. Se README.rst
2. Lek deg litt i browseren, sammenlign de fire forskjellige måtene
   å endre en bok på.
3. Ting endrer seg straks det er mange nok bøker til at man må
   scrolle!

2 Generelt
==========

1. Sammenlign urler når du gjør det samme på de forskjellige måtene.
2. I ``templates/singlefield_app/book_list4.html`` som brukes av
   "singlefield-htmx-boost" så er det kommentert vekk noe per felt:
   ``{# hx-push-url="false" #}``. Hva skjer hvis du kommenterer det
   inn igjen? (Ved å ta vekk ``{#`` og ``#}``.) Hva synes du er best,
   med eller uten "hx-push-url"?
3. Fortsatt i ``templates/singlefield_app/book_list4.html``: Endre
   ``htmx.config.scrollIntoViewOnBoost`` til ``true`` (eller kommenter
   vekk/slett hele script-taggen) og kommenter inn minst en av de
   utkommenterte ``{# hx-swap="innerHTML show:unset" #}``. Ikke gjør
   det med alle! Sammenlign! [1]_.
4. Lek med ``hx-swap`` og ``hx-target``. Det er kjapt gjort å bytte ut feil
   ting!

3. Endre ett felt om gangen: CBV
================================

1. Se på koden til appen, i ``src/singlefield/app/cbv/``
2. For "singlefield-htmx-get" så finnes det en utkommentert ``get_fragment()`` i
   ``HTMxGetSingleFieldUpdateBookView``. Bytt om på hvilken av dem som gjelder.
3. Skriv om "singlefield-htmx-get" tingene til å bruke POST (hx-post) istf. GET
   (hx-get). Start med templatet.

   Hvis Django eller Django class-based views er lite kjent for deg er det
   kanskje enklest å legge til en femte metode (singlefield-htmx-post) ved
   å kopiere singlefield-htmx-get og så oppdatere kopien. Du vil kanskje trenge
   endre i:

   - views.py
   - urls.py
   - ../templates/singlefield_app, se templatene med "3" i navnet.

   Hvis du er godt kjent med Django class-based-views, så kreves det ikke mer
   enn 3 nye linjer i ``views.py``.

   Tips: Se https://ccbv.co.uk/projects/Django/5.2/, sammenlign "UpdateView" og
   "DetailView".

4. Endre ett felt om gangen: FBV
================================

1. Se på koden til appen, i ``src/singlefield/app/fbv/``
2. For "singlefield-htmx-get" så finnes det en utkommentert ``fragment = ..`` i
   ``update_view3``. Bytt om på hvilken av dem som gjelder.
3. Skriv om "singlefield-htmx-get" tingene til å bruke POST (hx-post) istf. GET
   (hx-get). Start med templatet.

   Den tungvinte måten er å legge til en femte metode (singlefield-htmx-post)
   ved å kopiere singlefield-htmx-get og så oppdatere kopien. Du vil kanskje
   trenge endre i:

   - views.py
   - urls.py
   - ../templates/singlefield_app, se templatene med "3" i navnet.

   Hvis du er godt kjent med Django's funksjonelle views, så kreves det ikke
   mer enn å endre 1 linje i ``views.py``.

Bonus 1
=======

Gjør flere av dataene som er lagret i JSON editerbare ved å legge til flere
singlefields, se ``forms.py``. Evt. du kan importere mer data fra
json-blobben og gjøre dem editerbare.


.. [1] ``htmx.config.scrollIntoViewOnBoost`` var ikke med fra starten
   av, se `Scroll to top by default when navigating with hx-boost <https://github.com/bigskysoftware/htmx/issues/407>`_.

Bonus 2
=======

I stedet for å gå tilbake til listesiden etter en endring, lag en detaljside.
Flytt all editerings- og slettings-knapper dit.
