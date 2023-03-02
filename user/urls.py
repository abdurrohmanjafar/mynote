from django.urls import path
from .views import register_user, MyTokenObtainPairView

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view()),
    path('register/', register_user),
]