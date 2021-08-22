from django.urls import path
from leads.views import index, lead_detail, lead_create, lead_update

urlpatterns = [
    path('', index),
    path('<int:pk>', lead_detail),
    path('<int:pk>/update/', lead_update),
    path('create/', lead_create),
]
