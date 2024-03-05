from django.contrib import admin
from django.urls import path
from tdlapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', signupPage, name='signupPage'),
    path('login/', loginpage, name='loginpage'),
    path('logout/', logoutpage, name='logoutpage'),
    path('home/', home, name='home'),

    
    path('tasks/', task_list, name='task_list'),
    path('tasks/<int:pk>/', task_detail, name='task_detail'),
    path('tasks/create/', task_create, name='task_create'),
    path('tasks/<int:pk>/update/', task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', task_delete, name='task_delete'),
    path('tasks/filter_by_priority/<str:priority>/', task_filter_by_priority, name='task_filter_by_priority'),
    path('taskcomplete/<str:id>/', taskcomplete, name='taskcomplete'),
    path('tasks/filter_by_date/', task_filter_by_date, name='task_filter_by_date'),
    
    path('activate/<uid64>/<token>', activate,name='activate'),
    
    path('forgetpassword/', forgetpassword, name="forgetpassword"),
    path('changepassword/', changepassword, name="changepassword"),
]
