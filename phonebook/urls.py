from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("contacts", views.ListView.as_view(), name="list"),
    path("contact/<int:pk>/", views.DetailView.as_view(), name="detail"),
]