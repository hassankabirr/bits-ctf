from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Contest(models.Model):
    CONTEST_STATUS_CHOICES = [
        (0, 'not started'),
        (1, 'started'),
        (2, 'finish')
    ]
    name = models.CharField(max_length=255, blank=False)
    contest_status = models.IntegerField(choices=CONTEST_STATUS_CHOICES, default=0)
    start_time = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    end_time = models.DateTimeField(auto_now_add=False, blank=True, null=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=255, null=True)
    question_body = models.TextField(null=True)
    contest = models.ForeignKey(Contest, on_delete=models.SET_NULL, blank=False, null=True)
    flag = models.CharField(max_length=255, null=True)
    score = models.IntegerField(null=True)
    main_score = models.IntegerField(null=True)
    first_team = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    cat = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title


class Team(models.Model):
    name = models.CharField(max_length=255, null=True, unique=True)
    join_team_uuid = models.UUIDField(default=uuid.uuid4, unique=True, blank=True)
    solved_questions = models.ManyToManyField(Question, related_name="teams", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    @property
    def total_score(self):
        if self.solved_questions.count() > 0:
            return self.solved_questions.all().aggregate(models.Sum('score'))['score__sum']
        else:
            return 0

    def __str__(self):
        return self.name + f'({self.pk})'


class CustomUser(AbstractUser):
    USER_STATUS_CHOICES =[
        (0, 'not verified'),
        (1, 'verified'),
        (2, 'joined team')
    ]
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    user_status = models.IntegerField(default=0, choices=USER_STATUS_CHOICES, blank=True)
    university = models.CharField(max_length=255, blank=False, null=True)