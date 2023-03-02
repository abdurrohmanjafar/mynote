from django.urls import path
from .views import NoteViews

urlpatterns = [
    path('', NoteViews.as_view()),
    path('<int:id>/', NoteViews.as_view()),
]