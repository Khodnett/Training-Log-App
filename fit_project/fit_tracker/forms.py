from django import forms
from django.forms import ModelForm
from .models import Note
from ckeditor.fields import RichTextField

class CreateNewList(forms.Form):
    name = forms.CharField(label="Name",max_length=200)
    check= forms.BooleanField(required = False)

class LogWorkout(forms.Form):
    name = forms.CharField(label="Title",max_length=200)
    date= forms.DateField()

class LogExercises(forms.Form):
    METRICS = (
    ("lb", "lb"),
    ("kg", "kg"),
    )
    exercise = forms.CharField(label="Exercise",max_length=200)
    weight = forms.IntegerField()
    metric = forms.ChoiceField(choices = METRICS)
    reps = forms.IntegerField()

class OneRepMaxCalculator(forms.Form):
    weight=forms.IntegerField()
    reps = forms.IntegerField()

class ContactForm(forms.Form):
	first_name = forms.CharField(max_length = 50)
	last_name = forms.CharField(max_length = 50)
	email_address = forms.EmailField(max_length = 150)
	message = forms.CharField(widget = forms.Textarea(attrs={'rows': 5}), max_length = 2000)

class AdditionalNotes(ModelForm):
    class Meta:
        model = Note
        fields= ["notes"]
