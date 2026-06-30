from django.shortcuts import render

def home(request):
    context = {'username': "Harshwardhan",
    'total_tasks' : 10}
    return render(request,'home.html',context)

    
