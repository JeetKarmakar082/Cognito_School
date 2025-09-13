from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from scheduler.models import Department, Classroom, Faculty, Subject, TimeSlot
from datetime import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Create departments
        cs_dept = Department.objects.get_or_create(
            name="Computer Science & Engineering", code="CSE")[0]
        ee_dept = Department.objects.get_or_create(
            name="Electrical Engineering", code="EE")[0]
        
        # Create classrooms
        Classroom.objects.get_or_create(
            name="Room 101", capacity=60, room_type="lecture",
            department=cs_dept, has_projector=True, has_ac=True)
        
        # Create time slots
        TimeSlot.objects.get_or_create(
            day="monday", start_time=time(9, 0), end_time=time(10, 0))
        TimeSlot.objects.get_or_create(
            day="monday", start_time=time(10, 0), end_time=time(11, 0))
        
        self.stdout.write("Sample data loaded successfully!")
