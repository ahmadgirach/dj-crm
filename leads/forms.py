from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

from .models import Agent, Lead


class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        db_table = "lead_master"
        managed = True
        verbose_name = "Lead"
        verbose_name_plural = "Leads"
        fields = ("first_name", "last_name", "email", "phone_number", "age", "agent", "description")


class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", )
        field_classes = {"username": UsernameField}


class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        user = request.user
        agents = Agent.objects.filter(organization=user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents


class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            "category",
        )
