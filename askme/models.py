from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

# Create your models here.
class Queries(models.Model):
    place = models.CharField(max_length=30)
    duration  = models.IntegerField(validators=[MinValueValidator(1, "Duration must be greater than 1 character")])
    # personalize = models.CharField(max_length=100)

class Data(models.Model):
    gpt_place = models.CharField(max_length=30)
    gpt_duration  = models.IntegerField(validators=[MinValueValidator(1, "Duration must be greater than 1 character")])
    gpt_result = models.TextField(max_length=10000)

    def __str__(self):
        return self.gpt_place+"( "+str(self.gpt_duration)+" )"

class Food(models.Model):
    gpt_place = models.CharField(max_length=30)
    gpt_result = models.TextField(max_length=10000)

    def __str__(self):
        return self.gpt_place

class Statistics(models.Model):
    stat_place = models.CharField(max_length=30)
    stat_duration  = models.IntegerField(validators=[MinValueValidator(1, "Duration must be greater than 1 character")])
    stat_count = models.IntegerField(validators=[MinValueValidator(1, "Duration must be greater than 1 character")])

    def __str__(self):
        return self.stat_place+"( "+str(self.stat_duration)+"-"+str(self.stat_count)+" )"

class Search_history(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_place =models.CharField(max_length=30)
    search_duration  = models.IntegerField()
    search_query = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} searched for '{self.search_duration}-days'"