from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Task
from .serializers import TaskSerializer

class TaskListAPI(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		tasks = Task.objects.filter(user=request.user)
		search = request.query_params.get("search", "").strip()
		status_filter = request.query_params.get("status", "")
		priority_filter = request.query_params.get("priority", "")

		if search:
			tasks = tasks.filter(Q(title__icontains=search) | Q(description__icontains=search))

		if status_filter:
			valid_statuses = {choice[0] for choice in Task.STATUS_CHOICES}
			if status_filter not in valid_statuses:
				return Response({"detail": "Invalid status filter."}, status=status.HTTP_400_BAD_REQUEST)
			tasks = tasks.filter(status=status_filter)

		if priority_filter:
			valid_priorities = {choice[0] for choice in Task.PRIORITY_CHOICES}
			if priority_filter not in valid_priorities:
				return Response({"detail": "Invalid priority filter."}, status=status.HTTP_400_BAD_REQUEST)
			tasks = tasks.filter(priority=priority_filter)

		serializer = TaskSerializer(tasks, many=True)
		return Response(serializer.data)

	def post(self,request):
		serializer = TaskSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save(user = request.user)
			return Response(serializer.data,status = status.HTTP_201_CREATED)
		return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

class TaskDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


