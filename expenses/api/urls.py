from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('expenses/', views.expenses),
    path('expenses/<str:pk>/', views.expense),
    path('summary/', views.summary)
]