from django.db import models
from django.contrib.auth.models import User


class StudyGroup(models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    study_group = models.CharField(max_length=10)

    def __str__(self):
        return self.study_group