from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from agents.mixins import OrganiserAndLoginRequiredMixin

from .forms import LeadModelForm, SignupForm
from .models import Lead


class SignupView(CreateView):
    template_name = "registration/signup.html"
    """
    SINCE WE DON'T USE DEFAULT USER MODEL, WE CAN'T USE DEFAULT USER SIGNUP FORM... IT WILL RAISE AN ERROR WHILE
    REGISTRATION.

    HENCE WE OVERRIDE THE DEFAULT FORM AND ASSIGN OUR USER MODEL. THAT WAY IT WILL WORK.
    """
    # form_class = UserCreationForm
    form_class = SignupForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(TemplateView):
    template_name = "landing.html"


class LeadListView(LoginRequiredMixin, ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user

        if user.is_organiser:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            """ FILTER FOR THE AGENT THAT'S LOGGED IN """
            queryset = queryset.filter(agent__user=user)

        return queryset


class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user

        if user.is_organiser:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            """ FILTER FOR THE AGENT THAT'S LOGGED IN """
            queryset = queryset.filter(agent__user=user)

        return queryset

    @staticmethod
    def get_success_url():
        return reverse("leads:lead-list")


class LeadCreateView(OrganiserAndLoginRequiredMixin, CreateView):
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


class LeadUpdateView(OrganiserAndLoginRequiredMixin, UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.filter(organization=user.userprofile)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-list")


class LeadDeleteView(OrganiserAndLoginRequiredMixin, DeleteView):
    template_name = "leads/lead_delete.html"

    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.filter(organization=user.userprofile)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-list")
