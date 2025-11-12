from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import RegistrationForm, EmailAuthenticationForm, ProfileForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        try:
            send_mail(
                subject='Добро пожаловать!',
                message='Спасибо за регистрацию в нашем магазине.',
                from_email=None,
                recipient_list=[self.object.email],
                fail_silently=True,
            )
        except Exception:
            pass
        messages.success(self.request, 'Вы успешно зарегистрированы!')
        return response


class LoginView(DjangoLoginView):
    form_class = EmailAuthenticationForm
    template_name = 'users/login.html'


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy('catalog:home')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


