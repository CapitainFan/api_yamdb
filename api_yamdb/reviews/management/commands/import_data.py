import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Genre, Title

IMPORTS = {
    Category: "category.csv",
    Genre: "genre.csv",
    Title: "titles.csv",

}

REPLACE_FIELDS = {
    Title: ['category', 'category_id'],
}


class Command(BaseCommand):
    help = 'import test data to database from csv files'

    def handle(self, *args, **options):
        for table, file in IMPORTS.items():
            with open(f'{settings.BASE_DIR}/static/data/{file}') as f:
                print(f'пилим {table.__name__}')
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    if table in REPLACE_FIELDS:
                        row[REPLACE_FIELDS[table][1]] = row.pop(
                            REPLACE_FIELDS[table][0])
                        print(f'saving {row} to {table.__name__}')
                    table.objects.create(**row)
