from django.core.management.base import BaseCommand
from django.conf import settings
from reviews.models import Category, Genre, Title
import csv

imports = {
    Category: "category.csv",
    Genre: "genre.csv",
    # пока не вкурил как со связанными полями это завести
    #Title: "titles.csv",

}


class Command(BaseCommand):
    help = 'import test data to database from csv files'

    def handle(self, *args, **options):
        for table, file in imports.items():
            with open(f'{settings.BASE_DIR}/static/data/{file}') as f:
                print(f'пилим {table.__name__}')
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    print(f'saving {row} to {table.__name__}')
                    table.objects.create(**row)
