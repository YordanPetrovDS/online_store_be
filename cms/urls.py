from django.urls import path

from cms import views

app_name = "cms"

urlpatterns = [
    path("pages", views.PageListView.as_view()),
    path("page/<slug:slug>", views.PageDetailView.as_view()),
]
