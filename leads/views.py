from django.core.mail import send_mail
from django.urls import reverse
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView

from .forms import LeadModelForm
from .models import Lead


class LandingPageView(TemplateView):
    template_name = "landing.html"


class LeadListView(ListView):
    template_name = "leads/lead_list.html"
    queryset = Lead.objects.all()
    context_object_name = "leads"


class LeadDetailView(DetailView):
    template_name = "leads/lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"

    def get_success_url(self):
        return reverse("leads:lead-list")


class LeadCreateView(CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def post(self, request, *args, **kwargs):
        ret = super(LeadCreateView, self).post(request, args, kwargs)
        send_mail(
            subject="New Lead has been created...",
            message="Go to site to view the lead...",
            from_email="test@test.com",
            recipient_list=["tes2t@test.com"]
        )
        return ret


class LeadUpdateView(UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse("leads:lead-list")


class LeadDeleteView(DeleteView):
    template_name = "leads/lead_delete.html"
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse("leads:lead-list")
