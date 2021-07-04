"""URL's for the chat app."""
from django.urls import path

from . import views

urlpatterns = [
    path('roles/', views.Roles.as_view()),
    path('search-roles/', views.SearchRole.as_view()),
    path('role/<int:id>/', views.SingleRole.as_view()),
    path('role/', views.SingleRole.as_view()),
    path('permissions/', views.RolePermissions.as_view()),
    path('permission/', views.SingleRolePermission.as_view()),
    path('permission/<int:id>/', views.SingleRolePermission.as_view()),
    path('user-permission/', views.UserPermissions.as_view()),
]
