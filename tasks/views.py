from django.shortcuts import render
from .models import Task
def home(request):
    context = {'username': "Harshwardhan",
    'total_tasks' : Task.objects.count()
    }

    return render(request,'home.html',context)

def about(request):
    return render(request,'about.html')

def task_list(request):
    tasks = Task.objects.all()
    context = {
    'tasks' : tasks
    }
    return render(request, 'tasks/task_list.html',context)

