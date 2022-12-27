from django.db import models
from datetime import date
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# class ToDoList(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="todolist",null=True)
#   name = models.CharField(max_length=200)

#    def __str__(self):
#        return self.name

# class Item(models.Model):
#    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
#    text = models.CharField(max_length=300)
#   complete = models.BooleanField()

#   def __str__(self):
#        return self.text


class WorkoutDate(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="workoutdate", null=True)
    date = models.DateField()

    def __str__(self):
        return str(self.date)


class WorkoutName(models.Model):
    name = models.CharField(max_length=200)
    date = models.ForeignKey(
        WorkoutDate, on_delete=models.CASCADE, related_name="workoutname", null=True)

    def __str__(self):
        return str(self.name)


class Note(models.Model):
    notes = RichTextField(blank=True, null=True)
    workout = models.ForeignKey(
        WorkoutName, on_delete=models.CASCADE, related_name="notes", null=True)

    def __str__(self):
        return str(self.notes)


class Exercise(models.Model):
    name = models.CharField(max_length=200)
    workout = models.ForeignKey(
        WorkoutName, on_delete=models.CASCADE, related_name="exercise", null=True)

    def __str__(self):
        return str(self.name)


class ExerciseSet(models.Model):
    METRICS = (
        ("lb", "lb"),
        ("kg", "kg"),
    )

    exercise = models.ForeignKey(
        Exercise, on_delete=models.CASCADE, related_name="exerciseset", null=True)
    weight = models.IntegerField()
    metric = models.CharField(max_length=2, choices=METRICS, default='lb')
    reps = models.IntegerField()

    def __str__(self):
        return str(self.exercise)
