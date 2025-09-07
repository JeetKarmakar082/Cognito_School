# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class Classroom(models.Model):
    ROOM_TYPES = [
        ('lecture', 'Lecture Hall'),
        ('lab', 'Laboratory'),
        ('seminar', 'Seminar Room'),
        ('auditorium', 'Auditorium'),
    ]
    
    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='lecture')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    has_projector = models.BooleanField(default=False)
    has_ac = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} (Capacity: {self.capacity})"


class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    max_hours_per_day = models.PositiveIntegerField(default=6)
    max_hours_per_week = models.PositiveIntegerField(default=30)
    avg_leaves_per_month = models.PositiveIntegerField(default=2)
    is_available = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Faculties"
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"


class Subject(models.Model):
    SUBJECT_TYPES = [
        ('core', 'Core Subject'),
        ('elective', 'Elective'),
        ('practical', 'Practical'),
        ('project', 'Project Work'),
    ]
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    credits = models.PositiveIntegerField()
    subject_type = models.CharField(max_length=20, choices=SUBJECT_TYPES, default='core')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    hours_per_week = models.PositiveIntegerField(default=4)
    requires_lab = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class Batch(models.Model):
    PROGRAMS = [
        ('ug', 'Undergraduate'),
        ('pg', 'Postgraduate'),
        ('diploma', 'Diploma'),
    ]
    
    name = models.CharField(max_length=50)
    program = models.CharField(max_length=20, choices=PROGRAMS)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    year = models.PositiveIntegerField()
    student_count = models.PositiveIntegerField()
    subjects = models.ManyToManyField(Subject)
    
    def __str__(self):
        return f"{self.name} - Semester {self.semester}"


class TimeSlot(models.Model):
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    ]
    
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_break = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['day', 'start_time', 'end_time']
        ordering = ['day', 'start_time']
    
    def __str__(self):
        return f"{self.get_day_display()} {self.start_time} - {self.end_time}"


class TimetableTemplate(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=20)
    semester = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    max_classes_per_day = models.PositiveIntegerField(default=6)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_timetables')
    
    def __str__(self):
        return f"{self.name} - {self.academic_year}"


class TimetableEntry(models.Model):
    template = models.ForeignKey(TimetableTemplate, on_delete=models.CASCADE, related_name='entries')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    is_fixed = models.BooleanField(default=False)  # For special classes with fixed slots
    
    class Meta:
        unique_together = [
            ['template', 'time_slot', 'classroom'],
            ['template', 'time_slot', 'faculty'],
            ['template', 'time_slot', 'batch'],
        ]
    
    def __str__(self):
        return f"{self.subject.name} - {self.batch.name} - {self.time_slot}"


class FacultySubject(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['faculty', 'subject']
    
    def __str__(self):
        return f"{self.faculty.user.get_full_name()} - {self.subject.name}"


class SchedulingConstraint(models.Model):
    CONSTRAINT_TYPES = [
        ('no_back_to_back', 'No Back-to-Back Classes'),
        ('max_continuous', 'Maximum Continuous Hours'),
        ('preferred_time', 'Preferred Time Slot'),
        ('blocked_time', 'Blocked Time Slot'),
        ('room_preference', 'Room Preference'),
    ]
    
    name = models.CharField(max_length=100)
    constraint_type = models.CharField(max_length=20, choices=CONSTRAINT_TYPES)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, blank=True)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, null=True, blank=True)
    priority = models.PositiveIntegerField(default=1)  # 1 = High, 5 = Low
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_constraint_type_display()})"