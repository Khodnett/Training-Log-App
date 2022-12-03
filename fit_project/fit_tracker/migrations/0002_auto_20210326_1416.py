# Generated by Django 3.0.3 on 2021-03-26 18:16

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fit_tracker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='WorkoutDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workoutdate', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WorkoutName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('date', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workoutname', to='fit_tracker.WorkoutDate')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('workout', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='fit_tracker.WorkoutName')),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField()),
                ('metric', models.CharField(choices=[('lb', 'lb'), ('kg', 'kg')], default='lb', max_length=2)),
                ('reps', models.IntegerField()),
                ('exercise', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exerciseset', to='fit_tracker.Exercise')),
            ],
        ),
        migrations.AddField(
            model_name='exercise',
            name='workout',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exercise', to='fit_tracker.WorkoutName'),
        ),
    ]
