from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Housing','Housing'),
        ('Insurance','Insurance'),
        ('Medical','Medical'),
        ('Food & supplies','Food & Supplies'),
        ('Utilities','Utilities'),
        ('Entertainment', 'Entertainemnt'),
        ('Personal','Personal')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.category}: ${self.amount}"

