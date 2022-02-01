import csv
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from clubdata.main.models import Club, Match


class Command(BaseCommand):
    help = 'Import historic match data 1888-2020'

    def add_arguments(self, parser):
        parser.add_argument('csvfile')

    def handle(self, *args, **options):
        col_map = {
            'date': 0,
            'home': 2,
            'away': 3,
            'home_goals': 5,
            'away_goals': 6,
        }

        club_map = {}

        def get_result(home_goals, away_goals):
            if home_goals > away_goals:
                result = 'w'
            elif home_goals == away_goals:
                result = 'd'
            else:
                result = 'l'
            return result

        def get_club_from_cache_or_db(club_name):
            club_obj = club_map.get(club_name)
            if not club_obj:
                club_obj, created = Club.objects.get_or_create(name=club_name)
                club_map[club_name] = club_obj
            
            return club_obj


        with open(options['csvfile'], 'r') as football_data:
            reader = csv.reader(football_data, delimiter=',')
            #skip col titles
            next(reader)
            for row in reader:
                home_club_obj = get_club_from_cache_or_db(row[col_map['home']])
                away_club_obj = get_club_from_cache_or_db(row[col_map['away']])
                home_goals = row[col_map['home_goals']]
                away_goals = row[col_map['away_goals']]
                result = get_result(home_goals, away_goals)

                date = datetime.datetime.strptime(row[col_map['date']], '%Y-%m-%d')

                Match.objects.get_or_create(
                    date=date,
                    home=home_club_obj,
                    away=away_club_obj,
                    home_goals=home_goals,
                    away_goals=away_goals,
                    result=result
                )