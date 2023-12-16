from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import RegistrationForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
