from django.shortcuts import render

def home(request):
    context = {'username': "Harshwardhan",
    'total_tasks' : 10}
    return render(request,'home.html',context)

def about(request):
    return render(request,'about.html')

def task_list(request):
    return render(request, 'tasks/task_list.html')

