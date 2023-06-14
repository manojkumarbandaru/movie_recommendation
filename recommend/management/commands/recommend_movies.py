import json
import math
from datetime import date
from decimal import Decimal
from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from recommend.models import *

class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("user_id", type=int)
        parser.add_argument("top_n", type=int)

    def handle(self, *args: Any, **options: Any):
        all_movies = Movie.objects.values()
        preprocessed_movies = self.preprocess_movie_data(all_movies)

        user_id = options['user_id']
        related_users = RelatedUser.objects.filter(user_id=user_id).values_list('related_user_id', flat=True)
        related_users_preferences = UserPreference.objects.filter(user_id__in=related_users).values('user_id', 'genre', 'preference_score')

        related_users_movies = {}
        # calculating the relevant scores of a movie  for all related_users which will be used to find the average in the next step
        for movie_id, movie in preprocessed_movies.items():
            for related_user in related_users_preferences:
                relevant_score = self.movie_relevant_score(movie, related_user)
                if movie_id not in related_users_movies:
                    related_users_movies[movie_id] = []
                else:
                    related_users_movies[movie_id].append(relevant_score)
                
        user_perferences = UserPreference.objects.filter(id=user_id).values('user_id', 'genre', 'preference_score')
        user_movies = []
        # calculating the relevant score of a movie by adding user relevant score and average of relevant scores of all related users.
        for movie_id, movie in preprocessed_movies.items():
            relevant_score = 0
            for user_perference in user_perferences:
                relevant_score+=self.movie_relevant_score(movie, user_perference)
            
            if movie_id in related_users_movies:
                relevant_score+=sum(related_users_movies[movie_id])/len(related_users_movies[movie_id])
            user_movies.append((relevant_score, movie_id, movie['name']))

        top_n_movies = sorted(user_movies, key=lambda item:item[0], reverse=True)[:10]
        print(top_n_movies)            

    def preprocess_movie_data(self, movies):
        """
            pre processeses movies by calculating decay value using guassian decay function
        """
        preprocessed_movies = {}
        today = date.today()
        # decay value can be modified according to our use case, In the current datesets movies are very old
        # so used higher value here
        decay = 1300
        for movie in movies:
            release_date = movie['release_date']
            time_delta = (today - release_date).days
            decay_value = Decimal(math.exp(-0.5*(time_delta/decay)**2))
            preprocessed_movies[movie['id']] = {'name': movie['name'], 'genres': movie['genres'], 'decay_value': decay_value}
        return preprocessed_movies
    
    def movie_relevant_score(self, movie, user_preference):
        """
            calculates relevant score by combining genre preferences and movie decay value
        """
        relevant_score=0
        if user_preference['genre'] in movie['genres']:
            relevant_score+=user_preference['preference_score']*movie['decay_value']

        return relevant_score
        