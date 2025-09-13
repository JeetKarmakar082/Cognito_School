from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
import json
from datetime import datetime, time

from .models import (
    Department, Classroom, Faculty, Subject, Batch, TimeSlot,
    TimetableTemplate, TimetableEntry, FacultySubject, SchedulingConstraint
)
from .forms import (
    LoginForm, DepartmentForm, ClassroomForm, FacultyForm, SubjectForm,
    BatchForm, TimeSlotForm, TimetableTemplateForm, TimetableEntryForm, SchedulingConstraintForm, SignUpForm
)
from .utils import TimetableOptimizer


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = form.save()
            user.is_staff = True
            user.is_superuser = True
            user.save()
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect("dashboard")  # Change to your dashboard/home
    else:
        form = SignUpForm()
    return render(request, "scheduler/signup.html", {"form": form})



def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'scheduler/college-login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    # Dashboard statistics
    stats = {
        'total_departments': Department.objects.count(),
        'total_classrooms': Classroom.objects.count(),
        'total_faculties': Faculty.objects.count(),
        'total_subjects': Subject.objects.count(),
        'total_batches': Batch.objects.count(),
        'active_timetables': TimetableTemplate.objects.filter(is_active=True).count(),
    }
    
    # Recent timetables
    recent_timetables = TimetableEntry.objects.select_related(
        'batch', 'subject', 'faculty', 'classroom', 'time_slot'
    ).all().order_by('-id')
    
    context = {
        'stats': stats,
        'recent_timetables': recent_timetables,
    }
    return render(request, 'scheduler/college-dashboard.html', context)


@login_required
def manage_resources(request):
    # Get all resources with pagination
    departments = Department.objects.all()
    classrooms = Classroom.objects.select_related('department').all()
    faculties = Faculty.objects.select_related('department').all()
    subjects = Subject.objects.select_related('department').all()
    batches = Batch.objects.select_related('department').all()
    time_slots = TimeSlot.objects.all().order_by('day', 'start_time')
    
    context = {
        'departments': departments,
        'classrooms': classrooms,
        'faculties': faculties,
        'subjects': subjects,
        'batches': batches,
        'time_slots': time_slots,
    }
    return render(request, 'scheduler/manage_resources.html', context)


# @login_required
# def create_timetable(request):
#     if request.method == 'POST':
#         form = TimetableTemplateForm(request.POST)
#         if form.is_valid():
#             template = form.save(commit=False)
#             template.created_by = request.user
#             template.save()
            
#             # Generate optimized timetable entries
#             try:
#                 optimizer = TimetableOptimizer(template)
#                 success = optimizer.generate_timetable()
                
#                 if success:
#                     messages.success(request, 'Timetable created successfully!')
#                     return redirect('view_timetable', template_id=template.id)
#                 else:
#                     messages.warning(request, 'Timetable created but some conflicts remain. Please review and adjust.')
#                     return redirect('view_timetable', template_id=template.id)
#             except Exception as e:
#                 messages.error(request, f'Error generating timetable: {str(e)}')
#                 template.delete()
#                 return redirect('create_timetable')
#     else:
#         form = TimetableTemplateForm()
    
#     # Get available resources for the form
#     departments = Department.objects.all()
#     batches = Batch.objects.select_related('department').all()
    
#     context = {
#         'form': form,
#         'departments': departments,
#         'batches': batches,
#     }
#     return render(request, 'scheduler/create_timetable.html', context)

@login_required
def create_timetable(request):
    if request.method == 'POST':
        form = TimetableEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # or wherever you want after saving
    else:
        form = TimetableEntryForm()
    
    return render(request, 'scheduler/create_timetable.html', {'form': form})



# @login_required
# def view_timetable(request, template_id):
#     template = get_object_or_404(TimetableTemplate, id=template_id)
    
#     # Get all timetable entries for this template
#     entries = TimetableEntry.objects.select_related(
#         'time_slot', 'classroom', 'subject', 'faculty__user', 'batch'
#     ).filter(template=template).order_by('time_slot__day', 'time_slot__start_time')
    
#     # Get all time slots and organize data for display
#     time_slots = TimeSlot.objects.all().order_by('day', 'start_time')
#     days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    
#     # Organize timetable data by batch
#     batches = Batch.objects.filter(
#         department=template.department,
#         semester=template.semester
#     )
    
#     timetable_data = {}
#     for batch in batches:
#         timetable_data[batch] = {}
#         for day in days:
#             timetable_data[batch][day] = {}
#             day_slots = time_slots.filter(day=day)
#             for slot in day_slots:
#                 entry = entries.filter(batch=batch, time_slot=slot).first()
#                 timetable_data[batch][day][slot] = entry
    
#     context = {
#         'template': template,
#         'timetable_data': timetable_data,
#         'time_slots': time_slots,
#         'days': days,
#         'entries': entries,
#     }
#     return render(request, 'scheduler/view_timetable.html', context)


@login_required
@csrf_exempt
def get_department_batches(request):
    if request.method == 'GET':
        department_id = request.GET.get('department_id')
        if department_id:
            batches = Batch.objects.filter(department_id=department_id).values('id', 'name', 'semester')
            return JsonResponse({'batches': list(batches)})
    return JsonResponse({'batches': []})


@login_required
@csrf_exempt
def update_timetable_entry(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        entry_id = data.get('entry_id')
        field = data.get('field')
        value = data.get('value')
        
        try:
            entry = TimetableEntry.objects.get(id=entry_id)
            
            if field == 'classroom':
                classroom = Classroom.objects.get(id=value)
                entry.classroom = classroom
            elif field == 'faculty':
                faculty = Faculty.objects.get(id=value)
                entry.faculty = faculty
            elif field == 'subject':
                subject = Subject.objects.get(id=value)
                entry.subject = subject
            
            entry.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False})


@login_required
def approve_timetable(request, template_id):
    if request.method == 'POST':
        template = get_object_or_404(TimetableTemplate, id=template_id)
        
        # Check if user has permission to approve
        if request.user.is_staff or request.user.is_superuser:
            template.is_approved = True
            template.approved_by = request.user
            template.is_active = True
            template.save()
            
            # Deactivate other timetables for the same department and semester
            TimetableTemplate.objects.filter(
                department=template.department,
                semester=template.semester,
                academic_year=template.academic_year,
                is_active=True
            ).exclude(id=template.id).update(is_active=False)
            
            messages.success(request, 'Timetable approved and activated successfully!')
        else:
            messages.error(request, 'You do not have permission to approve timetables.')
    
    return redirect('view_timetable', template_id=template_id)


# @login_required
# def export_timetable(request, template_id):
#     template = get_object_or_404(TimetableTemplate, id=template_id)
#     entries = TimetableEntry.objects.select_related(
#         'time_slot', 'classroom', 'subject', 'faculty__user', 'batch'
#     ).filter(template=template).order_by('batch__name', 'time_slot__day', 'time_slot__start_time')
    
#     # Create CSV response
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = f'attachment; filename="timetable_{template.name}.csv"'
    
#     import csv
#     writer = csv.writer(response)
#     writer.writerow(['Batch', 'Day', 'Time', 'Subject', 'Faculty', 'Classroom'])
    
#     for entry in entries:
#         writer.writerow([
#             entry.batch.name,
#             entry.time_slot.get_day_display(),
#             f"{entry.time_slot.start_time} - {entry.time_slot.end_time}",
#             entry.subject.name,
#             entry.faculty.user.get_full_name(),
#             entry.classroom.name
#         ])
    
#     return response


@login_required
def delete_timetable(request, template_id):
    if request.method == 'POST':
        template = get_object_or_404(TimetableTemplate, id=template_id)
        
        # Check if user has permission to delete
        if template.created_by == request.user or request.user.is_staff:
            template.delete()
            messages.success(request, 'Timetable deleted successfully!')
        else:
            messages.error(request, 'You do not have permission to delete this timetable.')
    
    return redirect('dashboard')



def view_timetable(request, entry_id):
    entry = get_object_or_404(TimetableEntry, id=entry_id)

    return render(request, "scheduler/view_timetable.html", {
        "entry": entry
    })


import csv
def export_timetable(request, entry_id):
    entry = get_object_or_404(TimetableEntry, id=entry_id)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="timetable_entry_{entry.id}.csv"'

    writer = csv.writer(response)
    writer.writerow(["Day", "Time Slot", "Subject", "Faculty", "Classroom", "Batch"])

    writer.writerow([
        entry.time_slot.day,
        f"{entry.time_slot.start_time} - {entry.time_slot.end_time}",
        entry.subject.name,
        entry.faculty.employee_name,
        entry.classroom.name,
        entry.batch.name,
    ])

    return response




# Create Pages

@login_required
def create_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = SubjectForm()
    return render(request, 'scheduler/create_subject.html', {'form': form})

@login_required
def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = DepartmentForm()
    return render(request, 'scheduler/create_department.html', {'form': form})

@login_required
def create_classroom(request):
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ClassroomForm()
    return render(request, 'scheduler/create_classroom.html', {'form': form})

@login_required
def create_faculty(request):
    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = FacultyForm()
    return render(request, 'scheduler/create_faculty.html', {'form': form})

@login_required
def create_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = SubjectForm()
    return render(request, 'scheduler/create_subject.html', {'form': form})

@login_required
def create_batch(request):
    if request.method == 'POST':
        form = BatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = BatchForm()
    return render(request, 'scheduler/create_batch.html', {'form': form})

@login_required
def create_timeslot(request):
    if request.method == 'POST':
        form = TimeSlotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TimeSlotForm()
    return render(request, 'scheduler/create_timeslot.html', {'form': form})

@login_required
def create_timetable_template(request):
    if request.method == 'POST':
        form = TimetableTemplateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TimetableTemplateForm()
    return render(request, 'scheduler/create_timetable_template.html', {'form': form})

@login_required
def create_scheduling_constraint(request):
    if request.method == 'POST':
        form = SchedulingConstraintForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = SchedulingConstraintForm()
    return render(request, 'scheduler/create_scheduling_constraint.html', {'form': form})