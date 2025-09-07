from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, HTML
from crispy_forms.bootstrap import PrependedText

from .models import (
    Department, Classroom, Faculty, Subject, Batch, TimeSlot,
    TimetableTemplate, SchedulingConstraint
)


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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Login', css_class='btn btn-primary w-100'))


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'})
        }


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
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class FacultyForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Faculty
        fields = ['employee_id', 'department', 'phone', 'max_hours_per_day', 'max_hours_per_week', 'avg_leaves_per_month', 'is_available']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'max_hours_per_day': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_hours_per_week': forms.NumberInput(attrs={'class': 'form-control'}),
            'avg_leaves_per_month': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'credits', 'subject_type', 'department', 'semester', 'hours_per_week', 'requires_lab']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control'}),
            'subject_type': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 8}),
            'hours_per_week': forms.NumberInput(attrs={'class': 'form-control'}),
            'requires_lab': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['name', 'program', 'department', 'semester', 'year', 'student_count', 'subjects']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 8}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'student_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'subjects': forms.SelectMultiple(attrs={'class': 'form-select', 'multiple': True})
        }


class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['day', 'start_time', 'end_time', 'is_break']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'is_break': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class TimetableTemplateForm(forms.ModelForm):
    batches = forms.ModelMultipleChoiceField(
        queryset=Batch.objects.none(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'multiple': True}),
        required=True
    )
    
    class Meta:
        model = TimetableTemplate
        fields = ['name', 'department', 'academic_year', 'semester', 'max_classes_per_day']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'academic_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '2023-24'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 8}),
            'max_classes_per_day': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'row g-3'
        
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('academic_year', css_class='col-md-6'),
            ),
            Row(
                Column('department', css_class='col-md-4'),
                Column('semester', css_class='col-md-4'),
                Column('max_classes_per_day', css_class='col-md-4'),
            ),
            'batches',
            HTML('<hr>'),
            Submit('submit', 'Generate Timetable', css_class='btn btn-primary')
        )
        
        # Update batches queryset based on department and semester if data is available
        if 'department' in self.data and 'semester' in self.data:
            try:
                department_id = int(self.data.get('department'))
                semester = int(self.data.get('semester'))
                self.fields['batches'].queryset = Batch.objects.filter(
                    department_id=department_id,
                    semester=semester
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['batches'].queryset = Batch.objects.filter(
                department=self.instance.department,
                semester=self.instance.semester
            )


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
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }