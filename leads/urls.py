from django.urls import path
from .views import index, lead_detail, lead_create, lead_update, lead_delete

urlpatterns = [
    path('', index),
    path('<int:pk>', lead_detail),
    path('<int:pk>/update/', lead_update),
    path('<int:pk>/delete/', lead_delete),
    path('create/', lead_create),
]
