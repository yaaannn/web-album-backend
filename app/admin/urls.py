from django.urls import path

from .views import (
    AdminLoginView,
    GetAdminInfoView,
    GetUserListView,
    DeleteUserView,
    GetPhotoListView,
)

urlpatterns = [
    path("login", AdminLoginView.as_view()),
    path("info", GetAdminInfoView.as_view()),
    path("user/list", GetUserListView.as_view()),
    path("user/delete", DeleteUserView.as_view()),
    path("photo/list", GetPhotoListView.as_view()),
]
