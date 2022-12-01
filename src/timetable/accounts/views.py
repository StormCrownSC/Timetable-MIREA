from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *

import re

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('/accounts/login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        group = StudyGroup(
            author=user,
            study_group=re.findall(r'value="([\w-]+)"', str(form['study_group']))[0]
        )
        group.save()
        return redirect('/accounts/login')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('/accounts/login')


@login_required
def profile(request):
    context = {}
    context = {
        'study_group': StudyGroup.objects.get(author=request.user)
    }
    return render(request, 'profile.html', context)