from django.urls import path

from cms import views

urlpatterns = [
    path("pages", views.PageListView.as_view()),
    path("page/<slug:slug>", views.PageDetailView.as_view()),
]
