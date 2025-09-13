from django.contrib import admin
from .models import (
    Department, Classroom, Faculty, Subject, Batch, TimeSlot,
    TimetableTemplate, TimetableEntry, FacultySubject, SchedulingConstraint
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'created_at']
    search_fields = ['name', 'code']
    ordering = ['name']


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity', 'room_type', 'department', 'has_projector', 'has_ac', 'is_available']
    list_filter = ['room_type', 'department', 'has_projector', 'has_ac', 'is_available']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['employee_name', 'employee_id', 'department', 'max_hours_per_day', 'max_hours_per_week', 'is_available']
    list_filter = ['department', 'is_available']
    search_fields = ['employee_name', 'employee_id']
    ordering = ['employee_name']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'credits', 'subject_type', 'department', 'semester', 'hours_per_week', 'requires_lab']
    list_filter = ['subject_type', 'department', 'semester', 'requires_lab']
    search_fields = ['name', 'code']
    ordering = ['department', 'semester', 'name']


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['name', 'program', 'department', 'semester', 'year', 'student_count']
    list_filter = ['program', 'department', 'semester', 'year']
    search_fields = ['name']
    ordering = ['department', 'semester', 'name']


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['day', 'start_time', 'end_time', 'is_break']
    list_filter = ['day', 'is_break']
    ordering = ['day', 'start_time']


@admin.register(TimetableTemplate)
class TimetableTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'academic_year', 'semester', 'created_by', 'is_active', 'is_approved', 'created_at']
    list_filter = ['department', 'semester', 'is_active', 'is_approved', 'created_at']
    search_fields = ['name', 'academic_year']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(TimetableEntry)
class TimetableEntryAdmin(admin.ModelAdmin):
    list_display = ['template', 'time_slot', 'classroom', 'subject', 'faculty', 'batch', 'is_fixed']
    list_filter = ['template', 'time_slot__day', 'is_fixed']
    search_fields = ['subject__name', 'faculty__user__first_name', 'faculty__user__last_name', 'batch__name']
    ordering = ['template', 'time_slot__day', 'time_slot__start_time']


@admin.register(FacultySubject)
class FacultySubjectAdmin(admin.ModelAdmin):
    list_display = ['faculty', 'subject', 'is_primary']
    list_filter = ['is_primary', 'subject__department']
    search_fields = ['faculty__user__first_name', 'faculty__user__last_name', 'subject__name']


@admin.register(SchedulingConstraint)
class SchedulingConstraintAdmin(admin.ModelAdmin):
    list_display = ['name', 'constraint_type', 'faculty', 'subject', 'priority', 'is_active']
    list_filter = ['constraint_type', 'priority', 'is_active']
    search_fields = ['name']
    ordering = ['priority', 'name']