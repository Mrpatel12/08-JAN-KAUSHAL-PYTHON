from rest_framework import viewsets, permissions
from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all().select_related('farm', 'crop')
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.filter(farm__owner=self.request.user)

    def perform_create(self, serializer):
        farm_id = self.request.data.get('farm_id')
        farm = None
        if farm_id:
            from apps.farms.models import Farm
            farm = Farm.objects.get(id=farm_id, owner=self.request.user)
        serializer.save(farm=farm)
