from django.urls import path
from . import views

urlpatterns = [
    path('users/me/', views.Auth.as_view()),
    path('users/', views.Users.as_view()),
    path('staff/', views.SingleStaff.as_view()),
    path('staffs/', views.Staffs.as_view()),
    path('toggle-activate-staff/<int:id>', views.ToggleActivateUsers.as_view()),
    path('login/', views.Login.as_view()),


]
