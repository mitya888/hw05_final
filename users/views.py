#  импортируем CreateView, чтобы создать ему наследника
from django.views.generic import CreateView

from django.urls import reverse_lazy

#  импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import CreationForm


class SignUpView(CreateView):
    form_class = CreationForm
    # где signup — это параметр "name" в path()
    success_url = reverse_lazy("signup")
    template_name = "signup.html"
