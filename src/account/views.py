from multiprocessing import reduction
import re
from sys import orig_argv
from tracemalloc import is_tracing
from urllib import request
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import is_valid_path
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.core.mail import EmailMessage, send_mail
from django.conf import settings


from .backends import EmailBackend
from .forms import RegistrationUserForm, UserEditForm, LoginForm
from .models import UserBase
from .tokens import account_activation_token


def login_view(request):
    if request.user.is_authenticated:
        return redirect("account:dashboard")
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data
            print(user)
            username = user["username"]
            password = user["password"]
            # print(username)
            email = EmailBackend()
            user = email.authenticate(request, username=username, password=password)

            if user and user.is_active:
                login(request, user)
                # if request.POST.get("")
                return redirect("account:dashboard")

    context = {
        "form": form
    }
    return render(request, "account/registration/login.html", context)


def account_register(request):

    if request.user.is_authenticated:
        return redirect("account:dashboard")

    registerForm = RegistrationUserForm()
    if request.method == "POST":
        registerForm = RegistrationUserForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = "Activate your account"
            message = render_to_string("account/registration/account_activation_email.html", {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            to_email = registerForm.cleaned_data["email"]
            email = EmailMessage(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [to_email]
            )
            email.send()

            return render(request, "account/user/check_gmail.html")

    context = {
        "form": registerForm
    }
    return render(request, "account/registration/register.html", context)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, UserBase.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        login(request, user, backend='account.backends.EmailBackend')

        return redirect("account:dashboard")

    else:
        return render(request, "account/registration/activation_invalid.html")


@login_required
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("account:login")
    return render(request, "account/user/dashboard.html")


@login_required
def Update_profile(request):
    try:
        obj = get_object_or_404(
            UserBase, email=request.user.email, is_active=True)
    except UserBase.DoesNotExist:
        return redirect("account:login")

    form = UserEditForm(instance=obj)
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()

    context = {
        "form": form
    }
    return render(request, "account/user/update_profile.html", context)


@login_required
def delete_user(request):
    try:
        user = get_object_or_404(
            UserBase, email=request.user.email, is_active=True)
    except UserBase.DoesNotExist:
        return redirect("account:login")

    if request.method == "POST":
        user.is_active = False
        user.save()
        logout(request)
        return redirect("account:delete_confirm")
