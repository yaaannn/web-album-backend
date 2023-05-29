from django.urls import path

from app.user.views import (
    ChangePasswordView,
    GetUserInfoByIdView,
    GetUserInfoView,
    ModifyUserInfoView,
    ResetPasswordView,
    SendResetPasswordEmailView,
    UserLoginView,
    UserRegisterView,
)

urlpatterns = [
    path("login", UserLoginView.as_view(), name="login"),
    path("register", UserRegisterView.as_view(), name="register"),
    path("change_password", ChangePasswordView.as_view(), name="change_password"),
    path(
        "send_reset_email",
        SendResetPasswordEmailView.as_view(),
        name="send_reset_password_email",
    ),
    path("reset_password", ResetPasswordView.as_view(), name="reset_password"),
    path("get_user_info", GetUserInfoView.as_view(), name="get_user_info"),
    path("modify_user_info", ModifyUserInfoView.as_view(), name="modify_user_info"),
    path(
        "get_user_info_by_id", GetUserInfoByIdView.as_view(), name="get_user_info_by_id"
    ),
    # path("verify_code/", VerifyCodeView.as_view(), name="verify_code"),
]
