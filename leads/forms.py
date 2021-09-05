from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

from .models import Lead


class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        db_table = "lead_master"
        managed = True
        verbose_name = "Lead"
        verbose_name_plural = "Leads"
        fields = ("first_name", "last_name", "age", "agent")


class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", )
        field_classes = {"username": UsernameField}
