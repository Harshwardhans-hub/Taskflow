from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages


def home(request):
    context = {'username': "Harshwardhan",
    'total_tasks' : Task.objects.count()
    }

    if request.user.is_authenticated:
        user_tasks = Task.objects.filter(user = request.user)
        context['my_tasks'] = user_tasks.count()
        context['todo_count'] = user_tasks.filter(status='todo').count()
        context['inprogress_count'] = user_tasks.filter(status = 'in_progress').count()
        context['done_count'] = user_tasks.filter(status = 'done').count()


    return render(request,'home.html',context)

def about(request):
    return render(request,'about.html')

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    search = request.GET.get('search', '')
    if search:
        tasks = tasks.filter(Q(title__icontains=search) | Q(description__icontains=search))

    status_filter = request.GET.get('status', '')
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    context = {
        'tasks': tasks,
        'search': search,
        'status_filter': status_filter,
    }

    return render(request, 'tasks/task_list.html', context)

@login_required
def task_detail(request,pk):#pk is the primary key and can also be seen as the task_id for viewing the detail about that particular task with the plk or task_id
    task = get_object_or_404(Task, pk=pk)
    context={
    'task' : task,}

    return render(request,'tasks/task_detail.html',context)

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request,"Task created successfully")
            return redirect("task-list")
    else:
        form = TaskForm()

    context = {
        'form': form,
    }

    
    return render(request, 'tasks/task_form.html', context)

@login_required
def task_update(request,pk):
    task = get_object_or_404(Task,pk=pk,user=request.user)
    if request.method=="POST":
        form = TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            messages.success(request,"Task edited successfully!")
            return redirect('task-list')

    else:

        form = TaskForm(instance=task)

    context = {'task':task,
            'form':form}

    return render(request,'tasks/task_form.html',context)        

@login_required
def task_delete(request,pk):
    task = get_object_or_404(Task,pk=pk,user=request.user)
    if request.method == "POST":
        task.delete()
        messages.success(request,"Task deleted successfully!")
        return redirect('task-list')

    context={
    'task':task
    }
    return render(request,'tasks/task_confirm_delete.html',context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)