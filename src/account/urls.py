from django.urls import path
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import views
from .views import (
    account_register,
    activate,
    dashboard,
    Update_profile,
    login_view,
    delete_user,
)
from .forms import PwResetForm, PwResetConfirmForm

app_name = "account"


urlpatterns = [
    path("register/", account_register, name="register"),
    path('activate/<slug:uidb64>/<slug:token>)/',  activate, name='activate'),
    # path("login/", views.LoginView.as_view(
    #     template_name="account/registration/login.html", form_class=UserLoginForm),
    #     name="login"
    # ),
    path("login/", login_view, name="login"),
    path("logout/", views.LogoutView.as_view(next_page="/account/login/"),
         name="logout"
         ),

    # change password
    path("password_change/", views.PasswordChangeView.as_view(
        template_name="account/registration/password_change.html",
        success_url="done/"), name="password_change"),
    path("password_change/done/", views.PasswordChangeDoneView.as_view(
        template_name="account/registration/password_change_done.html"), name="password_change_done"),


    # reset password
    path("password_reset/", views.PasswordResetView.as_view(
        template_name="account/registration/password_reset.html",
        email_template_name="account/registration/password_reset_email.html",
        success_url="done",
        form_class=PwResetForm), 
        name="password_reset"),

    path("password_reset/done/", views.PasswordResetDoneView.as_view(
        template_name="account/registration/password_reset_done.html"),
        name="password_reset_done"),

    path("reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(
        template_name="account/registration/password_reset_confirm.html",
        success_url= reverse_lazy("account:password_reset_complete"),
        form_class= PwResetConfirmForm
        ),
        name="password_reset_confirm"),

    path("reset/done/", views.PasswordResetCompleteView.as_view(
        template_name="account/registration/password_reset_complete.html"),
        name="password_reset_complete"),


    # dashboard
    path("dashboard/", dashboard, name="dashboard"),
    path("profile/update/", Update_profile, name="update_profile"),
    path("profile/delete/", delete_user, name="delete_user"),
    path("profile/delete_confirm/", TemplateView.as_view(
        template_name="account/user/delete_confirm.html"), name="delete_confirm")
]

views.PasswordResetConfirmView
