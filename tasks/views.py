
from django.shortcuts import render,get_object_or_404
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

def task_detail(request,pk):#pk is the primary key and can also be seen as the task_id for viewing the detail about that particular task with the plk or task_id
    task = get_object_or_404(Task, pk=pk)
    context={
    'task' : task,}

    return render(request,'tasks/task_detail.html',context)