import json
from html import unescape

from django.core.management.base import BaseCommand

from singlefield.app.models import Book


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        with open(options['filename'], 'r', encoding='utf-8') as JF:
            jsonblob = json.load(JF)
        books = []
        for value in jsonblob.values():
            title = value.get('title', 'LACKS TITLE')
            title_field = unescape(title)

            year = value.get('date', 0)
            try:
                year_field = int(year)
            except ValueError:
                year_field = 0

            authors = []
            for author in value.get('authors', []):
                if 'lf' in author:
                    authors.append(author['lf'])
                    continue
                if 'fl' in author:
                    authors.append(author['fl'])
                    continue
            author_field = '; '.join(authors) or '-'

            misc = {}
            for key in ('language', 'summary', 'publication', 'pages'):
                if key in value:
                    misc_value = value[key]
                    if isinstance(misc_value, str):
                        misc[key] = misc_value.strip()
                    elif isinstance(misc_value, list):
                        misc[key] = ', '.join(misc_value)
                    else:
                        misc[key] = misc_value
            if 'isbn' in value:
                if '0' in value['isbn']:
                    misc['ISBN-10'] = value['isbn']['0']
                if '2' in value['isbn']:
                    misc['ISBN-13'] = value['isbn']['2']

            books.append(
                Book(
                    author=author_field,
                    title=title_field,
                    year=year_field,
                    misc=misc,
                )
            )
        Book.objects.bulk_create(books)
