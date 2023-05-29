from django.urls import path

from app.admin.views import (
    AdminLoginView,
    AuditPhotoView,
    DeletePhotoView,
    DeleteUserView,
    FreezeUserView,
    GetAdminInfoView,
    GetCommentListView,
    GetPhotoListView,
    GetUserListView,
)

urlpatterns = [
    path("login", AdminLoginView.as_view(), name="admin_login"),
    path("info", GetAdminInfoView.as_view(), name="admin_info"),
    path("user/list", GetUserListView.as_view(), name="user_list"),
    path("user/delete", DeleteUserView.as_view()),
    path("photo/list", GetPhotoListView.as_view()),
    path("photo/delete", DeletePhotoView.as_view()),
    path("photo/audit", AuditPhotoView.as_view()),
    path("user/freeze", FreezeUserView.as_view()),
    path("comment/list", GetCommentListView.as_view()),
]
