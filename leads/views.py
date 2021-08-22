from django.shortcuts import render, redirect

from .forms import LeadForm, LeadModelForm
from .models import Agent, Lead


def index(request):
    leads = Lead.objects.all()
    context = {"leads": leads}
    return render(request, "leads/lead_list.html", context=context)


def lead_detail(request, pk):
    lead = Lead.objects.get(pk=pk)
    context = {"lead": lead}
    return render(request, "leads/lead_detail.html", context=context)


def lead_create(request):
    form = LeadModelForm()

    if request.method == "POST":
        data = request.POST.copy()
        form = LeadModelForm(data)

        if form.is_valid():
            form.save()
            return redirect("/leads")

    context = {"form": form}

    return render(request, "leads/lead_create.html", context=context)


def lead_update(request, pk):
    lead = Lead.objects.get(pk=pk)
    form = LeadModelForm()

    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)

        if form.is_valid():
            form.save()
            return redirect("/leads")

    context = {"form": form, "lead": lead}

    return render(request, "leads/lead_update.html", context=context)


# def lead_create(request):
#     form = LeadForm()

#     if request.method == "POST":
#         data = request.POST.copy()
#         form = LeadForm(data)

#         if form.is_valid():
#             agent = Agent.objects.first()
#             cleaned_data = form.cleaned_data
#             cleaned_data.update({"agent": agent})
#             Lead.objects.create(**cleaned_data)
#             return redirect("/leads")

#     context = {"form": form}

#     return render(request, "leads/lead_create.html", context=context)
