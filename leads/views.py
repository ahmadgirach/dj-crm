from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, FormView
)

from agents.mixins import OrganiserAndLoginRequiredMixin

from .forms import LeadModelForm, SignupForm, AssignAgentForm, LeadCategoryUpdateForm
from .models import Lead, Category


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
            queryset = Lead.objects.filter(organization=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization, agent__isnull=False)
            """ FILTER FOR THE AGENT THAT'S LOGGED IN """
            queryset = queryset.filter(agent__user=user)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LeadListView, self).get_context_data(object_list=object_list, kwargs=kwargs)
        user = self.request.user

        if user.is_organiser:
            queryset = Lead.objects.filter(organization=user.userprofile, agent__isnull=True)
            context.update({
                "unassigned_leads": queryset
            })
        return context


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


class AssignAgentView(OrganiserAndLoginRequiredMixin, FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs()
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def form_valid(self, form):
        agent = form.cleaned_data.get("agent")
        lead = Lead.objects.get(pk=self.kwargs.get("pk"))
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "leads/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        user = self.request.user

        if user.is_organiser:
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data(object_list=object_list, kwargs=kwargs)

        user = self.request.user

        if user.is_organiser:
            queryset = Lead.objects.filter(organization=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization, agent__isnull=False)

        context.update({
            "unassigned_leads_count": queryset.filter(category__isnull=True).count()
        })

        return context


class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user

        if user.is_organiser:
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)

        return queryset

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(CategoryDetailView, self).get_context_data(object_list=object_list, kwargs=kwargs)
    #     """ `leads` is the related_name given in Lead model. This is special syntax to fetch in ForeignKey fields. """
    #     leads = self.get_object().leads.all()
    #     context.update({
    #         "leads": leads
    #     })
    #     return context


class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user

        if user.is_organiser:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            """ FILTER FOR THE AGENT THAT'S LOGGED IN """
            queryset = queryset.filter(agent__user=user)

        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={
            "pk": self.get_object().pk
        })
