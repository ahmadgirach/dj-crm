from django import forms
from .models import Lead


class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        db_table = "lead_master"
        managed = True
        verbose_name = "Lead"
        verbose_name_plural = "Leads"
        fields = ("first_name", "last_name", "age", "agent")


class LeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=0)
