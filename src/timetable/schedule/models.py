from django.db import models
from django.contrib.auth.models import User


class UserProfileInfo(models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    study_group = models.CharField(max_length=10)
    id_study_group = models.IntegerField()

    def __str__(self):
        return f'{self.study_group} {self.id_study_group}'

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


class CallSchedule(models.Model):
    subject_number = models.IntegerField(primary_key=True)
    time_start = models.TimeField()
    time_end = models.TimeField()

    def __str__(self):
        return f'{self.time_start} {self.time_end}'

    class Meta:
        managed = False
        db_table = 'call_schedule'


class Course(models.Model):
    id_of_course = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'course'


class Degree(models.Model):
    id_of_degree = models.AutoField(primary_key=True)
    degree_of_study = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'degree'


class Institute(models.Model):
    id_of_the_institute = models.AutoField(primary_key=True)
    name_of_the_institute = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'institute'


class Lecturer(models.Model):
    id_lecturer = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.full_name)

    class Meta:
        managed = False
        db_table = 'lecturer'


class StudyGroup(models.Model):
    id_group = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=20)
    id_institute = models.IntegerField(blank=True, null=True)
    id_of_course = models.IntegerField()
    id_degree = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.id_group)

    class Meta:
        managed = False
        db_table = 'study_group'


class Timetable(models.Model):
    id_to_group = models.IntegerField(primary_key=True)
    subject_to_number = models.IntegerField()
    id_lectur = models.IntegerField(blank=True, null=True)
    subject_title = models.CharField(max_length=500)
    auditorium = models.CharField(max_length=500, blank=True, null=True)
    day_week = models.IntegerField()
    type_of_week = models.IntegerField()

    def __str__(self):
        return f'{self.subject_title}_-_{self.id_lectur}_-_{self.auditorium}'


    class Meta:
        managed = False
        db_table = 'timetable'
        unique_together = (('id_to_group', 'subject_to_number', 'day_week', 'type_of_week'),)