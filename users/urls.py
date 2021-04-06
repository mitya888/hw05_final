from django.urls import path
from . import views

urlpatterns = [
    # path() для страницы регистрации нового пользователя
    path("signup/", views.SignUpView.as_view(), name="signup")
]
