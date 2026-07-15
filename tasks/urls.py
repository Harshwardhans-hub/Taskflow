from django.urls import path
from . import views
from . import api_views

urlpatterns = [
	path('',views.home,name='home'),
	path('about/',views.about,name='about'),
	path('tasks/', views.task_list, name='task-list'),
	path('tasks/<int:pk>/',views.task_detail,name='task-detail'),
	path('tasks/create/',views.task_create,name='task-create'),
	path('tasks/<int:pk>/edit/',views.task_update,name='task-update'),
	path('tasks/<int:pk>/delete/',views.task_delete,name='task-delete'),
	path('register/',views.register,name='register'),
	path('api/tasks/',api_views.TaskListAPI.as_view(),name='task-list-api'),
	path('api/tasks/<int:pk>/',api_views.TaskDetailAPI.as_view(),name='task-detail-api'),
	]
