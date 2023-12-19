import random
from django.conf import settings
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.models import User
from users.forms import RegistrationForm, UserProfileForm, UserPasswordChangeForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:code')

    def form_valid(self, form):
        new_pass = ''.join([str(random.randint(0, 9)) for _ in range(9)])
        new_user = form.save(commit=False)
        new_user.ver_code = new_pass
        new_user.save()
        send_mail(
            subject='Подтверждение почты',
            message=f'Код {new_user.ver_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )

        return super().form_valid(form)


class CodeView(View):
    model = User
    template_name = 'users/code.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        code = request.POST.get('code')
        user = User.objects.filter(ver_code=code).first()

        if user is not None:
            user.is_active = True
            user.save()
            return redirect('users:login')

        else:
            return redirect('users:code')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
