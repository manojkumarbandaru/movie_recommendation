from django.db import models

class User(models.Model):
    name=models.CharField(max_length=255)

class RelatedUser(models.Model):
    user=models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="related_user")
    related_user=models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="related_to_user")

class Movie(models.Model):
    name=models.CharField(max_length=255)
    genres=models.CharField(max_length=255)
    release_date=models.DateField()

class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.CharField(max_length=255)
    preference_score = models.DecimalField(max_digits=5, decimal_places=2)