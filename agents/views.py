from django.shortcuts import reverse
from django.views import generic

from leads.models import Agent

from .mixins import OrganiserAndLoginRequiredMixin
from .forms import AgentModelForm


class AgentListView(OrganiserAndLoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"

    def get_queryset(self):
        organization = self.request.user.userprofile
        """ SHOW ONLY AGENTS WHICH BELONGS TO CURRENT LOGGED IN USER """
        return Agent.objects.filter(organization=organization)


class AgentCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    form_class = AgentModelForm
    template_name = "agents/agent_create.html"

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form):
        agent = form.save(commit=False)
        agent.organization = self.request.user.userprofile
        agent.save()
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganiserAndLoginRequiredMixin, generic.DetailView):
    context_object_name = "agent"
    queryset = Agent.objects.all()
    template_name = "agents/agent_detail.html"


class AgentUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView):
    form_class = AgentModelForm
    queryset = Agent.objects.all()
    template_name = "agents/agent_update.html"

    def get_success_url(self):
        return reverse("agents:agent-list")


class AgentDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    form_class = AgentModelForm
    queryset = Agent.objects.all()
    template_name = "agents/agent_delete.html"

    def get_success_url(self):
        return reverse("agents:agent-list")
