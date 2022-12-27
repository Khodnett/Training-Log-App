from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import WorkoutDate, Exercise, ExerciseSet, WorkoutName, Note
from .forms import CreateNewList, LogWorkout, LogExercises, OneRepMaxCalculator, AdditionalNotes, ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Count
import calendar as calend
from calendar import HTMLCalendar
from .utils import Calendar
from datetime import datetime, timedelta
# Create your views here.


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calend.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = str(next_month.year) + '-' + str(next_month.month)
    return month


def index(response, id):

    x = WorkoutName.objects.get(id=id)
    ls = WorkoutDate.objects.get(id=id)

    if response.user != ls.user:
        return HttpResponse(status=403)

    if response.method == "POST":

        if 'notes' in response.POST:
            if x.notes.count() == 0:
                noteform = AdditionalNotes(response.POST)
                if noteform.is_valid():
                    note = noteform.cleaned_data["notes"]
                    n = Note(notes=note)
                    n.save()
                    x.notes.add(n)
            else:
                noteform = AdditionalNotes(response.POST)

                if noteform.is_valid():
                    note = noteform.cleaned_data["notes"]
                    noteId = x.notes.values('id')[0]['id']
                    Note.objects.filter(id=noteId).update(notes=note)

                    noteform = AdditionalNotes()

        else:
            noteform = AdditionalNotes()

        if 'exercise' in response.POST:

            form = LogExercises(response.POST)

            if form.is_valid():
                e = form.cleaned_data["exercise"]
                w = form.cleaned_data["weight"]
                m = form.cleaned_data["metric"]
                r = form.cleaned_data["reps"]

                if not x.exercise.filter(name=e).exists():
                    ex = Exercise(name=e)
                    exSets = ExerciseSet(weight=w, metric=m, reps=r)
                    ex.save()
                    exSets.save()
                    x.exercise.add(ex)
                    ex.exerciseset.add(exSets)
                else:
                    exId = x.exercise.filter(name=e).values('id')
                    exId = exId[0]['id']
                    ex = Exercise(id=exId)
                    exSets = ExerciseSet(weight=w, metric=m, reps=r)
                    exSets.save()
                    ex.exerciseset.add(exSets)

        else:
            form = LogExercises()

    else:
        if x.notes.count() > 0:
            ntId = x.notes.values('id')[0]['id']
            nt = Note.objects.get(id=ntId)
            noteform = AdditionalNotes(initial={'notes': nt})
        else:
            noteform = AdditionalNotes()

        form = LogExercises()

    return render(response, "fit_tracker/log.html", {"ls": ls, "form": form, "noteform": noteform})


def home(response):

    context = ''

    if response.method == "POST":

        form = LogWorkout(response.POST)

        if form.is_valid():

            nm = form.cleaned_data["name"]
            d = form.cleaned_data["date"]

            if response.user.workoutdate.filter(date=d).exists():
                context = 'date already exists'

            else:

                t = WorkoutDate(date=d)
                n = WorkoutName(name=nm, date=t)
                t.save()
                n.save()
                response.user.workoutdate.add(t)

                return HttpResponseRedirect("/%i" % t.id)

    else:
        form = LogWorkout()

    return render(response, "fit_tracker/home.html", {"form": form, "context": context})


def view(response):
    return render(response, "fit_tracker/view.html", {})


def about(response):
    return render(response, "fit_tracker/about.html", {})


def contact(response):
    if response.method == 'POST':
        form = ContactForm(response.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'], }
            message = "\n".join(body.values())
            try:
                send_mail(subject, message, 'Kalb1776@gmail.com',
                          ['Kalb1776@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            return HttpResponseRedirect("/")

    form = ContactForm()
    return render(response, "fit_tracker/contact.html", {'form': form})


def calculator(response):
    if response.method == "POST":
        form = OneRepMaxCalculator(response.POST)
        context = ''
        if form.is_valid():
            w = form.cleaned_data["weight"]
            r = form.cleaned_data["reps"]

            if r < 1:
                form = OneRepMaxCalculator()
                context = 'The minimum number of reps is 1'
                return render(response, "fit_tracker/calculator.html", {"form": form, "context": context})

            max = round(w * (1 + ((r-1)/30)), 1)
            context = 'Your one rep max is ' + str(max)
        return render(response, "fit_tracker/calculator.html", {"form": form, "context": context, "max": max})

    else:
        form = OneRepMaxCalculator()
    return render(response, "fit_tracker/calculator.html", {"form": form})


@login_required
def calendar(response, year=datetime.now().year, month=datetime.now().strftime('%B')):

    if response.method == "POST":
        if response.POST.get("workout_title"):
            wt = response.POST["workout_title"]
            dt = response.POST["date"]
            date = WorkoutDate(date=dt)
            name = WorkoutName(name=wt, date=date)
            date.save()
            name.save()
            response.user.workoutdate.add(date)

            return HttpResponseRedirect("/%i" % date.id)

    y = year
    m = month[:3]
    mm = {name: num for num, name in enumerate(calend.month_abbr) if num}
    m = int(mm[m])
    if len(str(m)) <= 1:
        monthAndYear = str(y)+'-0'+str(m)+'-01'
    else:
        monthAndYear = str(y)+'-'+str(m)+'-01'
    prev = prev_month(datetime.fromisoformat(monthAndYear))
    dt = prev.split('-')
    prevYear = dt[0]
    prevMonth = calend.month_name[int(dt[1])]

    next = next_month(datetime.fromisoformat(monthAndYear))
    nextdt = next.split('-')
    nextYear = nextdt[0]
    nextMonth = calend.month_name[int(nextdt[1])]

    cal = Calendar(y, m, response)
    html_cal = cal.formatmonth(withyear=True)
    # return context
    return render(response, "fit_tracker/calendar.html", {'cal': html_cal,
                                                          'year': y, 'month': month,
                                                          'prevYear': prevYear, 'prevMonth': prevMonth,
                                                          'nextYear': nextYear, 'nextMonth': nextMonth, })


@login_required
def delete_set(response, id):

    set = ExerciseSet.objects.get(id=id)
    wo = WorkoutDate.objects.filter(
        user=response.user, workoutname__exercise__exerciseset=set.id)
    if not wo:
        return HttpResponse(status=403)
    woId = wo.values('id')
    woId = woId[0]['id']

    exCount = Exercise.objects.filter(exerciseset=set.id)
    x = exCount.values('id')
    x = x[0]['id']
    lift = Exercise.objects.get(id=x)
    setsRem = lift.exerciseset.count()

    set.delete()

    if setsRem == 1:
        # delete lift
        lift.delete()

    return HttpResponseRedirect("/%i" % woId)


@login_required
def delete_workout(response, id):
    try:
        workout = WorkoutDate.objects.get(user=response.user, id=id)
    except:
        return HttpResponse(status=403)

    date = datetime.strptime(str(workout), '%Y-%m-%d').date()
    year = date.strftime('%Y')
    month = date.strftime('%B')
    workout.delete()
    return HttpResponseRedirect("/calendar/"+year+"/"+month)


@login_required
def delete_note(response, id):

    note = Note.objects.get(id=id)
    wo = WorkoutDate.objects.filter(
        user=response.user, workoutname__notes=note.id)
    if not wo:
        return HttpResponse(status=403)

    woId = wo.values('id')
    woId = woId[0]['id']

    note.delete()

    return HttpResponseRedirect("/%i" % woId)
