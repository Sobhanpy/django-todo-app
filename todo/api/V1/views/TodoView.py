from ..serializer import Todoserializer
from todo.models import Task
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class TodoView(viewsets.ModelViewSet):
    serializer_class = Todoserializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]
    ordering_fields = ["-created_date"]
