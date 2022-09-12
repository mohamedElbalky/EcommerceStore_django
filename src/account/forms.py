
from dataclasses import field
import re
from sre_constants import MAX_UNTIL
from tkinter import Widget
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm

from django.db.models import Q
from .models import UserBase
# error_messages = {'required':"Please Enter your Name"}


class RegistrationUserForm(forms.ModelForm):
    username = forms.CharField(
        label=_("Username"),
        min_length=4, max_length=50,
        required=True,
        error_messages={'required': _("Sorry, you will need a username")})

    email = forms.EmailField(
        label=_("Email"),
        max_length=100, required=True,
        error_messages={'required': _("Sorry, you will need an email")})

    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput)

    password2 = forms.CharField(
        label=_("Repeat Password"),
        widget=forms.PasswordInput)

    def clean_username(self):
        username = str(self.cleaned_data["username"]).lower()
        user = UserBase.objects.filter(username=username)
        if user.exists():
            raise forms.ValidationError(
                _("username or password is already exists"))
            # self.add_error("username", _("username or password is already exists"))
        if username.__contains__("@"):
            raise forms.ValidationError(_("don't use special characters like @, #, $, %"))
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        user = UserBase.objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError(
                _("Please user another email, that email is already token"))

        return email

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError(_("Passwords don't match"))
        return cd["password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class": "mb-3 mt-1",
            "placeholder": "Username"
        })
        self.fields["email"].widget.attrs.update({
            "class": "mb-3 mt-1",
            "placeholder": "Email",
            
        })
        self.fields["password"].widget.attrs.update({
            "class": "mb-3 mt-1",
            "placeholder": "Password",
        })
        self.fields["password2"].widget.attrs.update({
            "class": "mb-3 mt-1",
            "placeholder": "Repeat Password",

        })

        # for field in self.fields.values():
        #     field.error_messages = {
        #         "required": _("Sorry, you will need an username")
        #     }

    class Meta:
        model = UserBase
        fields = ("username", "email")

        error_messages = {
            "username": {
                "required": _("Sorry, you will need an email")
            }
        }
        help_texts = {
            "username": _("enter your name here")
        }

        error_messages = {
            'name': {
                'required': "This is a custom error message from modelform meta",
            },
        }

    # def clean(self):
    #     cd = self.cleaned_data
    #     username = cd["username"].lower()
    #     password = cd["password"]
    #     password2 = cd["password2"]
    #     email = cd["email"]

    #     user_1 = UserBase.objects.filter(username=username)
    #     if user_1.exists():
    #         # raise self.add_error(_("username or password is already exists"))
    #         raise forms.ValidationError(_("username or password is already exists"))

    #     user_2 = UserBase.objects.filter(email=email)
    #     if user_2.exists():
    #         raise forms.ValidationError(_("Please user another email, that email is already token"))
    #         # raise self.add_error(_("Please user another email, that email is already token"))

    #     if password != password2:
    #         # raise self.add_error(_("Passwords don't match"))
    #         raise forms.ValidationError(_("Passwords don't match"))

    #     return cd


class LoginForm(forms.Form):
    username = forms.CharField(label='Email / Username')
    password = forms.CharField(label="Password",widget=forms.PasswordInput, required=True)

    error_messages = {
        "invalid_login": _(
            "Please enter a correct username or email and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),

    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].error_messages.update({
            "required": _("please enter usernam"),
            "invalid": _("enter valid name or email"),
        })
        self.fields["username"].widget.attrs.update({
            "class": "mb-2"
        })
        self.fields["password"].widget.attrs.update({
            "class": "mb-2"
        })


    def clean_username(self):
        username = self.cleaned_data["username"]
        lookup = Q(username=username) | Q(email=username)
        user = UserBase.objects.filter(lookup)
        print(user)
        if not user.exists():
            raise forms.ValidationError(_("this username or email is not exists"))
        user_ = user.first()
        if user_.is_active == False:
            raise forms.ValidationError(_("not active"))

        return user_






# class UserLoginForm(AuthenticationForm):
#     username = forms.CharField(label='Email / Username')
#     password = forms.CharField(label="Password",widget=forms.PasswordInput, required=True)


    # error_messages = {
    #     "invalid_login": _(
    #         "Please enter a correct username or email and password. Note that both "
    #         "fields may be case-sensitive."
    #     ),
    #     "inactive": _("This account is inactive."),

    # }
    

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["username"].error_messages.update({
    #         "invalid": _("enter valid name or email"),
    #         "required": _("please enter usernam"),
    #     })
    #     self.fields["username"].widget.attrs.update({
    #         "class": "mt-2"
    #     })
    #     self.fields["password"].widget.attrs.update({
    #         "class": "mt-2"
    #     })





class UserEditForm(forms.ModelForm):
    username = forms.CharField(label="Username", required=True)
    first_name = forms.CharField(label="First Name")
    about = forms.CharField(label="About", widget=forms.Textarea(attrs={"rows": "3"}))
    
    class Meta:
        model = UserBase
        fields = ('username','first_name', 'about', 'countery', 'phone_number', 'post_code', 'adress_line_1', 'adress_line_2')


    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class": "mb-3"
        })
        self.fields["about"].widget.attrs.update({
            "class": "mb-3"
        })
        self.fields["phone_number"].widget.attrs.update({
            "class": "mb-3"
        })
        self.fields["post_code"].widget.attrs.update({
            "class": "mb-3"
        })
        self.fields["adress_line_1"].widget.attrs.update({
            "class": "mb-3"
        })
            
        self.fields["adress_line_2"].widget.attrs.update({
            "class": "mb-3"
        })
            


class PwResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=225, widget=forms.TextInput)

    def clean_email(self):
        email = self.cleaned_data["email"]
        obj = UserBase.objects.filter(email=email)
        if not obj:
            raise forms.ValidationError("We can not find that email adress")
        return email

    
class PwResetConfirmForm(SetPasswordForm):
        new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput)
        new_password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput)

        def clean_new_password1(self):
            cd = self.cleaned_data
            password1 = cd.get("new_password1")
            if len(password1) < 8:
                raise forms.ValidationError("Your password must contain at least 8 characters.")
            return password1

        def clean_new_password2(self):
            cd = self.cleaned_data
            password1 = cd.get("new_password1")
            password2 = cd.get("new_password2")
            if password1 and password2:
                if password1 != password2:
                    raise forms.ValidationError(_("The two password fields didn’t match."))
            return password2


