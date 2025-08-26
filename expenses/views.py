from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Sum
from .models import Expense
from .forms import ExpenseForm
import datetime

# Create your views here.

def home(req):
    return render(req, 'home.html')

def getSummary(req):
    stats = []
    total = 0
    CATEGORY_CHOICES = [
        ('Housing'),
        ('Insurance'),
        ('Medical'),
        ('Food & supplies'),
        ('Utilities'),
        ('Entertainment'),
        ('Personal')
    ]
    count = Expense.objects.filter(date__lt=datetime.datetime.today(), date__gte=datetime.datetime.today()-datetime.timedelta(30)).count()
    # total = Expense.objects.filter(category=cat).annotate(total=sum("amount"))
    # print(count)
    for cat in CATEGORY_CHOICES:
        # print(cat)
        subtotal = Expense.objects.filter(category=cat).aggregate(subsum=Sum("amount"))["subsum"] or 0
        subcount = Expense.objects.filter(category=cat).count()
        subtotal = round(subtotal,2)
        total += subtotal
        stats.append((cat, subcount, subtotal))
        # print(subtotal, total)

    # print(stats)
    
    for i in range(len(stats)):
        percent = stats[i][2]*100/total
        percent = round(percent, 2)
        stats[i] = [stats[i][0], stats[i][1], stats[i][2], percent]

    print(stats)
    
    context = {'stats': stats, 'total': total, 'count': count}
    
    return render(req, 'summary.html', context)

def loginPage(req):
    # if req.method == 'POST':
    #     username = req.POST.get('username')
    #     password = req.POST.get('password')

    # try:
    #     user = User.objects.get(username=username)
    # except:


    context = {}
    return render(req, 'login_register.html', context)


def expenses(req):
    expenses = Expense.objects.filter(user=req.user)
    context = {'expenses': expenses}
    return render(req, 'listExpenses.html', context)

def addExpense(req):
    if req.method == 'POST':
        form = ExpenseForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('listExpenses')

    form = ExpenseForm()
    context = {'form': form}
    return render(req, 'expenseForm.html', context)

def updateExpense(req, pk):
    expense = Expense.objects.get(id=pk)

    if req.method == 'POST':
        form = ExpenseForm(req.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('listExpenses')

    form = ExpenseForm(instance=expense)
    context = {'form': form, 'edit': True}
    return render(req, 'expenseForm.html', context)

def deleteExpense(req, pk):
    expense = Expense.objects.get(id=pk)
    if req.method == 'POST':
        expense.delete()
        return redirect('listExpenses')
    return render(req, 'deleteExpenses.html', {'obj': expense})
