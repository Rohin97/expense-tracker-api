
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="expensesHome"),
    # path('login/', views.loginPage, name="login"),
    path('expenses/', views.expenses, name="listExpenses"),
    path('add-expense/', views.addExpense, name="addExpense"),
    path('update-expense/<str:pk>/', views.updateExpense, name="updateExpense"),
    path('delete-expense/<str:pk>/', views.deleteExpense, name="deleteExpense"),
    path('get-summary/', views.getSummary, name="getSummary")
]