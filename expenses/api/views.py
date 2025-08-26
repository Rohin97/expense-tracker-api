from rest_framework.decorators import api_view
from django.db.models import Sum
from django.http import JsonResponse
from expenses.models import Expense
from .serializers import ExpenseSerializer
import datetime

@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def getRoutes(req):
    routes = [
        'GET /api', 
        'GET /api/expenses',
        'POST /api/expenses',
        'GET /api/expenses/:id',
        'PATCH /api/expenses/:id',
        'DELETE /api/expenses/:id',
        'GET /api/summary'
    ]
    return Response(routes)

@api_view(['GET', 'POST'])
def expenses(req):
    if req.method == 'GET':
        expenses = Expense.objects.filter(user=req.user)
        serializer = ExpenseSerializer(expenses, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif req.method == 'POST':
        serializer = ExpenseSerializer(data=req.data, context={'request': req})
        if serializer.is_valid():
            serializer.save(user=req.user)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
@api_view(['GET', 'PATCH', 'DELETE'])
def expense(req, pk):
    try:
        expense = Expense.objects.filter(user=req.user).get(id=pk)
    except Expense.DoesNotExist:
        return JsonResponse({'status': 'fail', "message": "Expense does not exist in user records."}, status=404)

    if req.method == 'GET':
        serializer = ExpenseSerializer(expense, many=False)
        return JsonResponse(serializer.data)
    elif req.method == 'PATCH':
        serializer = ExpenseSerializer(expense, data=req.data, context={'request': req}, partial=True)
        if serializer.is_valid():
            serializer.save(user=req.user)
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    elif req.method == 'DELETE':
        expense.delete()
        return JsonResponse({'status': 'success'}, status=204)

@api_view(['GET'])
def summary(req):
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
    count = Expense.objects.filter(user=req.user,date__lt=datetime.datetime.today(), date__gte=datetime.datetime.today()-datetime.timedelta(30)).count()
    for cat in CATEGORY_CHOICES:
        subtotal = Expense.objects.filter(category=cat).aggregate(subsum=Sum("amount"))["subsum"] or 0
        subcount = Expense.objects.filter(category=cat).count()
        subtotal = round(subtotal,2)
        total += subtotal
        stats.append((cat, subcount, subtotal))
    
    for i in range(len(stats)):
        percent = stats[i][2]*100/total
        percent = round(percent, 2)
        stats[i] = [stats[i][0], stats[i][1], stats[i][2], percent]

    # print(stats)
    
    context = {'stats': stats, 'total': total, 'count': count}
    
    return JsonResponse({'status': 'success', 'stats': stats, 'total': total, 'count': count}, status=200)
