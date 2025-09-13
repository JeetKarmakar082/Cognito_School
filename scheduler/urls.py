from django.urls import path
from . import views

urlpatterns = [

    # Account Creation
    path("signup/", views.signup_view, name="signup"),

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
    path("timetable/<int:entry_id>/view/", views.view_timetable, name="view_timetable"),
    path("timetable/<int:entry_id>/export/", views.export_timetable, name="export_timetable"),
    # path('timetable/<int:template_id>/approve/', views.approve_timetable, name='approve_timetable'),
    # path('timetable/<int:template_id>/delete/', views.delete_timetable, name='delete_timetable'),
    
    # AJAX endpoints
    path('api/department-batches/', views.get_department_batches, name='get_department_batches'),
    path('api/update-entry/', views.update_timetable_entry, name='update_timetable_entry'),

    # Create Pages
    path('subject/create/', views.create_subject, name='create_subject'),
    path('department/create/', views.create_department, name='create_department'),
    path('classroom/create/', views.create_classroom, name='create_classroom'),
    path('faculty/create/', views.create_faculty, name='create_faculty'),
    path('batch/create/', views.create_batch, name='create_batch'),
    path('timeslot/create/', views.create_timeslot, name='create_timeslot'),
    path('template/create/', views.create_timetable_template, name='create_timetable_template'),
    path('constraint/create/', views.create_scheduling_constraint, name='create_scheduling_constraint'),
]