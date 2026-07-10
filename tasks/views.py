from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm


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

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task-list')
    else:
        form = TaskForm()

    context = {
        'form': form,
    }
    return render(request, 'tasks/task_form.html', context)

def task_update(request,pk):
    task = get_object_or_404(Task,pk=pk)
    if request.method=="POST":
        form = TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('task-list')

    else:

        form = TaskForm(instance=task)

    context = {'task':task,
            'form':form}
    return render(request,'tasks/task_form.html',context)        

def task_delete(request,pk):
    task = get_object_or_404(Task,pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect('task-list')

    context={
    'task':task
    }
    return render(request,'tasks/task_confirm_delete.html',context)
