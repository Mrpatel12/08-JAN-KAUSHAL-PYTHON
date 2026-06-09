from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from apps.expenses.models import Expense
from apps.harvests.models import Harvest


class AnalyticsOverview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        farms = user.farms.all()
        data = {}
        # Simple aggregation: total expenses and harvest revenue per farm
        for f in farms:
            expenses_total = Expense.objects.filter(farm=f).aggregate(total=Sum('amount'))['total'] or 0
            revenue_total = Harvest.objects.filter(farm=f).aggregate(total=Sum('revenue'))['total'] or 0
            data[str(f.id)] = {
                'farm_name': f.name,
                'expenses_total': expenses_total,
                'revenue_total': revenue_total,
            }
        return Response(data)
