"""URL's for the chat app."""
from django.urls import path

from . import views

urlpatterns = [
    path('sale-order-print/', views.SalePrint.as_view()),

]
