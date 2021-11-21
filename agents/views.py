from django.shortcuts import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from leads.models import Agent

from .forms import AgentModelForm


class AgentListView(LoginRequiredMixin, generic.ListView):
    queryset = Agent.objects.all()
    template_name = "agents/agent_list.html"


class AgentCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = AgentModelForm
    template_name = "agents/agent_create.html"

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form):
        agent = form.save(commit=False)
        agent.organization = self.request.user.userprofile
        agent.save()
        return super(AgentCreateView, self).form_valid(form)
