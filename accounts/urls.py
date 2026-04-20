from django.urls import path
from .views import (
    UserRegistrationView, LogoutView, UserLoginView, UserUpdateView,
    CashierDashboardView, CashierCustomerUpdateView
)

app_name = 'accounts'

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", LogoutView.as_view(), name="user_logout"),
    path("register/", UserRegistrationView.as_view(), name="user_registration"),
    path("profile/", UserUpdateView.as_view(), name="profile"),
    path("cashier/", CashierDashboardView.as_view(), name="cashier_dashboard"),
    path("cashier/update/<int:pk>/", CashierCustomerUpdateView.as_view(), name="cashier_update"),
]