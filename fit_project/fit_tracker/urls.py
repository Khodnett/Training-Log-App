from django.urls import path
from . import views

urlpatterns = [
    path("<int:id>", views.index, name="index"),
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("view/", views.view, name="view"),
    path("calendar/", views.calendar, name="calendar"),
    path("calendar/<int:year>/<str:month>/", views.calendar, name="calendar"),
    path("calculator/", views.calculator, name="calculator"),
    path("<int:id>/delete_set", views.delete_set, name="delete_set"),
    path("<int:id>/delete_workout/", views.delete_workout, name="delete_workout"),
    path("<int:id>/delete_note", views.delete_note, name="delete_note"),
]
