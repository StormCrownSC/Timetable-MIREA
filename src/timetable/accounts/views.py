from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import *
from schedule.models import *
from schedule.views import current_themes

import re

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('/accounts/login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs) | {"themes": current_themes(self.request)}
        return dict(list(context.items()))

    def form_valid(self, form):
        group_name = str(re.findall(r'value="([\w-]+)"', str(form['study_group']))[0]).upper()
        try:
            id_group = int(str(StudyGroup.objects.get(group_name=group_name)))
            user = form.save()
            login(self.request, user)
            group = UserProfileInfo(
                author=user,
                study_group=group_name,
                id_study_group=id_group
            )
            group.save()
            self.request.session['type_of_enter_data'] = 'week'
            self.request.session['themes'] = 'dark'
            return redirect('/accounts/login')
        except:
            return redirect('/accounts/register')
        

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs) | {"themes": current_themes(self.request)}
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
        'study_group': str(UserProfileInfo.objects.get(author=request.user)).split()[0],
        "themes": current_themes(request)
    }
    return render(request, 'profile.html', context)