from django.contrib import admin
from .models import ToDoList, Item, WorkoutDate,Exercise, ExerciseSet,WorkoutName,Note
# Register your models here.
admin.site.register(ToDoList)
admin.site.register(Item)
admin.site.register(WorkoutDate)
admin.site.register(Exercise)
admin.site.register(ExerciseSet)
admin.site.register(WorkoutName)
admin.site.register(Note)
