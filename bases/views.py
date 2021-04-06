from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView
# Create your views here.

class SinPrivilegios(LoginRequiredMixin, PermissionRequiredMixin):
    login_url = "bases:login"
    raise_exception = False
    redirect_field_name = "redirect_to"

    #Rewrite method
    def handle_no_permission(self):
        from django.contrib.auth.models import AnonymousUser
        if not self.request.user == AnonymousUser():
                self.login_url = "bases:sin_privilegios"
        return HttpResponseRedirect(reverse_lazy(self.login_url))

class Home(LoginRequiredMixin, TemplateView):
    template_name = 'bases/home.html'
    login_url = '/login'

class HomeSinPrivilegios(LoginRequiredMixin, TemplateView):
    login_url = "bases:login"
    template_name="bases/sin_privilegios.html"