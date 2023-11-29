from django.urls import path
from rest_framework.routers import DefaultRouter

from blog import views

router = DefaultRouter()
router.register(r"article-tags", views.ArticleTagViewSet)

urlpatterns = [
    path("article-categories", views.ArticleCategoryListView.as_view()),
    path("articles", views.ArticleViewSet.as_view({"get": "list"})),
    path(
        "article/<slug:slug>",
        views.ArticleViewSet.as_view({"get": "retrieve"}),
        name="article",
    ),
    path("articles/keys", views.ArticleKeysListView.as_view()),
]

urlpatterns += router.urls
