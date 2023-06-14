import json
import os
from datetime import date
from typing import Any
from django.db import transaction, connection
from django.core.management.base import BaseCommand, CommandParser
from recommend.models import *

class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("table_name", type=str)

    def handle(self, *args: Any, **options: Any) -> str | None:
        if options['table_name']=='movie':
            self.populate_movies()
        elif options['table_name']=='user':
            self.populate_users()
        elif options['table_name']=='related_user':
            self.populate_related_users()
        elif options['table_name']=='user_preference':
            self.populate_user_preference()
        else:
            self.populate_movies()
            self.populate_users()
            self.populate_related_users()
            self.populate_user_preference()

    @staticmethod
    def populate_movies():
        print("starting populating movies")
        with open(f"{os.getcwd()}/recommend/initial_db_data/movie_data.json") as mf:
            data = json.loads(mf.read())
            with transaction.atomic():
                for movie in data:
                    movie_model = Movie()
                    movie_model.name = movie['movie_name']
                    movie_model.genres = json.dumps(movie['genres'])
                    movie_date = movie['release_date'].split('/')
                    movie_model.release_date = date(int(movie_date[2]), int(movie_date[0]), int(movie_date[1]))
                    movie_model.save()
        print("populating movies completed")

    @staticmethod
    def populate_users():
        print("starting populating users")
        with open(f"{os.getcwd()}/recommend/initial_db_data/user_data.json") as uf:
            data = json.loads(uf.read())
            with transaction.atomic():
                for user in data:
                    user_model = User()
                    user_model.pk = user['user_id']
                    user_model.name = user['name']
                    user_model.save()
        print("populating users completed")

    @staticmethod
    def populate_related_users():
        print("starting populating related users")
        with open(f"{os.getcwd()}/recommend/initial_db_data/related_users.json") as ruf:
            data = json.loads(ruf.read())
            with transaction.atomic():
                for user_id, related_users in data.items():
                    for related_user in related_users:
                        ru_model = RelatedUser()
                        ru_model.user = User(pk=user_id)
                        ru_model.related_user = User(pk=related_user['user_id'])
                        ru_model.save()
        print("populating related users completed")

    @staticmethod
    def populate_user_preference():
        print("starting populating user preferences")
        with open(f"{os.getcwd()}/recommend/initial_db_data/user_preference.json") as upf:
            data = json.loads(upf.read())
            for user in data:
                for preference in user['preference']:
                    try:
                        up_model = UserPreference()
                        up_model.user = User(pk=user['user_id'])
                        up_model.genre = preference['genre']
                        up_model.preference_score = preference['preference_score']
                        up_model.save()
                    except Exception as e:
                        # print(e)
                        pass
        print("populaing user preferences completed")
