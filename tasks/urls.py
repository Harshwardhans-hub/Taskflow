from django.urls import path
from . import views 

urlpatterns = [
	path('',views.home,name='home'),
	path('about/',views.about,name='about'),
	path('tasks/', views.task_list, name='task-list'),
	path('tasks/<int:pk>/',views.task_detail,name='task-detail'),
	path('tasks/create/',views.task_create,name='task-create'),
		]
