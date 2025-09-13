from django import forms
from .models import (
    Department, Classroom, Faculty, Subject, Batch, TimeSlot,
    TimetableTemplate, TimetableEntry, SchedulingConstraint
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# ---------------- Sign Up ----------------

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


# ---------------- Login ----------------

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )



# ---------------- Department ----------------
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }

# ---------------- Classroom ----------------
class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name', 'capacity', 'room_type', 'department', 'has_projector', 'has_ac', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'has_projector': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_ac': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# ---------------- Faculty ----------------
class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = [
            'employee_name',
            'employee_id',
            'department',
            'phone',
            'max_hours_per_day',
            'max_hours_per_week',
            'avg_leaves_per_month',
            'is_available'
        ]
        widgets = {
            'employee_name': forms.TextInput(attrs={'class': 'form-control'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'max_hours_per_day': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_hours_per_week': forms.NumberInput(attrs={'class': 'form-control'}),
            'avg_leaves_per_month': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# ---------------- Subject ----------------
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = [
            'name', 'code', 'credits', 'subject_type',
            'department', 'semester', 'hours_per_week', 'requires_lab'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control'}),
            'subject_type': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 8}),
            'hours_per_week': forms.NumberInput(attrs={'class': 'form-control'}),
            'requires_lab': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# ---------------- Batch ----------------
class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['name', 'program', 'department', 'semester', 'year', 'student_count']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 8}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'student_count': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# ---------------- TimeSlot ----------------
class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['day', 'start_time', 'end_time', 'is_break']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'is_break': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# ---------------- TimetableTemplate ----------------
class TimetableTemplateForm(forms.ModelForm):
    class Meta:
        model = TimetableTemplate
        fields = ['name', 'department', 'academic_year', 'semester', 'max_classes_per_day', 'is_active', 'is_approved']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'academic_year': forms.TextInput(attrs={'class': 'form-control'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_classes_per_day': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# ---------------- TimetableEntry ----------------
class TimetableEntryForm(forms.ModelForm):
    class Meta:
        model = TimetableEntry
        fields = ['template', 'time_slot', 'classroom', 'subject', 'faculty', 'batch', 'is_fixed']
        widgets = {
            'template': forms.Select(attrs={'class': 'form-select'}),
            'time_slot': forms.Select(attrs={'class': 'form-select'}),
            'classroom': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'faculty': forms.Select(attrs={'class': 'form-select'}),
            'batch': forms.Select(attrs={'class': 'form-select'}),
            'is_fixed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# ---------------- SchedulingConstraint ----------------
class SchedulingConstraintForm(forms.ModelForm):
    class Meta:
        model = SchedulingConstraint
        fields = ['name', 'constraint_type', 'faculty', 'subject', 'classroom', 'time_slot', 'priority', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'constraint_type': forms.Select(attrs={'class': 'form-select'}),
            'faculty': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'classroom': forms.Select(attrs={'class': 'form-select'}),
            'time_slot': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
