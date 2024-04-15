from ..forms import CustomUserCreation
from django.views.generic import CreateView


class SignUpView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreation
    success_url = "/accounts/login/"
from ..forms import CustomUserCreation
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect


class SignUpView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreation
    success_url = "/accounts/login/"

    def form_valid(self, form):
        form.save()
        email = self.request.POST.get('email')
        password = self.request.POST.get('password1')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(self.request,user)
            return redirect('/accounts/edit-profile/%i'%(user.id-1))