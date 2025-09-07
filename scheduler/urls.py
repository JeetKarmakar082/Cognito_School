from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Resource Management
    path('manage-resources/', views.manage_resources, name='manage_resources'),
    
    # Timetable Management
    path('create-timetable/', views.create_timetable, name='create_timetable'),
    path('timetable/<int:template_id>/', views.view_timetable, name='view_timetable'),
    path('timetable/<int:template_id>/approve/', views.approve_timetable, name='approve_timetable'),
    path('timetable/<int:template_id>/export/', views.export_timetable, name='export_timetable'),
    path('timetable/<int:template_id>/delete/', views.delete_timetable, name='delete_timetable'),
    
    # AJAX endpoints
    path('api/department-batches/', views.get_department_batches, name='get_department_batches'),
    path('api/update-entry/', views.update_timetable_entry, name='update_timetable_entry'),
]