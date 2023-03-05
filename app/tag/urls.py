from django.urls import path
from .views import TagCreateView, TagListView, TagDeleteView

urlpatterns = [
    path("list", TagListView.as_view()),
    path("create", TagCreateView.as_view()),
    path("delete", TagDeleteView.as_view()),
]
