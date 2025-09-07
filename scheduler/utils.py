import random
from collections import defaultdict
from datetime import datetime, time
from django.db.models import Q

from .models import (
    Department, Classroom, Faculty, Subject, Batch, TimeSlot,
    TimetableTemplate, TimetableEntry, FacultySubject, SchedulingConstraint
)


class TimetableOptimizer:
    def __init__(self, template):
        self.template = template
        self.time_slots = list(TimeSlot.objects.filter(is_break=False).order_by('day', 'start_time'))
        self.classrooms = list(Classroom.objects.filter(is_available=True))
        self.batches = list(Batch.objects.filter(
            department=template.department,
            semester=template.semester
        ))
        self.faculty_workload = defaultdict(int)
        self.classroom_utilization = defaultdict(list)
        self.batch_schedule = defaultdict(list)
        self.conflicts = []
        
    def generate_timetable(self):
        """Generate optimized timetable using constraint satisfaction"""
        try:
            # Clear existing entries
            TimetableEntry.objects.filter(template=self.template).delete()
            
            # Get all subject-faculty mappings
            subject_faculty_map = self._get_subject_faculty_mappings()
            
            # Generate class requirements
            class_requirements = self._generate_class_requirements()
            
            # Sort requirements by priority
            class_requirements = self._prioritize_requirements(class_requirements)
            
            # Schedule classes
            scheduled = 0
            total = len(class_requirements)
            
            for requirement in class_requirements:
                if self._schedule_class(requirement, subject_faculty_map):
                    scheduled += 1
            
            # Try to resolve conflicts with alternative arrangements
            self._resolve_conflicts()
            
            return scheduled == total
            
        except Exception as e:
            print(f"Error in timetable generation: {str(e)}")
            return False
    
    def _get_subject_faculty_mappings(self):
        """Get available faculty for each subject"""
        mappings = defaultdict(list)
        
        for batch in self.batches:
            for subject in batch.subjects.all():
                # Get faculty who can teach this subject
                faculty_subjects = FacultySubject.objects.filter(
                    subject=subject,
                    faculty__is_available=True,
                    faculty__department=subject.department
                ).select_related('faculty')
                
                for fs in faculty_subjects:
                    mappings[subject].append(fs.faculty)
        
        return mappings
    
    def _generate_class_requirements(self):
        """Generate list of all required classes"""
        requirements = []
        
        for batch in self.batches:
            for subject in batch.subjects.all():
                classes_per_week = subject.hours_per_week
                
                for i in range(classes_per_week):
                    requirements.append({
                        'batch': batch,
                        'subject': subject,
                        'class_number': i + 1,
                        'requires_lab': subject.requires_lab,
                        'priority': self._calculate_priority(subject, batch)
                    })
        
        return requirements
    
    def _calculate_priority(self, subject, batch):
        """Calculate scheduling priority for a subject"""
        priority = 1
        
        # Core subjects get higher priority
        if subject.subject_type == 'core':
            priority += 2
        
        # Practical subjects need labs
        if subject.requires_lab:
            priority += 1
        
        # Higher semester subjects get priority
        priority += subject.semester * 0.1
        
        return priority
    
    def _prioritize_requirements(self, requirements):
        """Sort requirements by priority and constraints"""
        return sorted(requirements, key=lambda x: x['priority'], reverse=True)
    
    def _schedule_class(self, requirement, subject_faculty_map):
        """Schedule a single class"""
        batch = requirement['batch']
        subject = requirement['subject']
        requires_lab = requirement['requires_lab']
        
        # Get available faculty for this subject
        available_faculty = subject_faculty_map.get(subject, [])
        if not available_faculty:
            self.conflicts.append(f"No faculty available for {subject.name}")
            return False
        
        # Try each time slot
        random.shuffle(self.time_slots)  # Add randomness for better distribution
        
        for time_slot in self.time_slots:
            # Check if batch is available
            if not self._is_batch_available(batch, time_slot):
                continue
            
            # Find suitable classroom
            suitable_classrooms = self._find_suitable_classrooms(batch, requires_lab)
            
            for classroom in suitable_classrooms:
                if not self._is_classroom_available(classroom, time_slot):
                    continue
                
                # Find available faculty
                for faculty in available_faculty:
                    if self._is_faculty_available(faculty, time_slot):
                        # Check faculty workload constraints
                        if self._check_faculty_workload(faculty, time_slot):
                            # Create timetable entry
                            entry = TimetableEntry.objects.create(
                                template=self.template,
                                time_slot=time_slot,
                                classroom=classroom,
                                subject=subject,
                                faculty=faculty,
                                batch=batch
                            )
                            
                            # Update tracking
                            self._update_tracking(faculty, classroom, batch, time_slot)
                            return True
        
        self.conflicts.append(f"Could not schedule {subject.name} for {batch.name}")
        return False
    
    def _find_suitable_classrooms(self, batch, requires_lab):
        """Find classrooms suitable for the batch and requirements"""
        suitable = []
        
        for classroom in self.classrooms:
            # Check capacity
            if classroom.capacity < batch.student_count:
                continue
            
            # Check if lab is required
            if requires_lab and classroom.room_type != 'lab':
                continue
            
            # Check department preference
            if classroom.department and classroom.department != batch.department:
                continue
            
            suitable.append(classroom)
        
        # Sort by preference (department match, capacity efficiency)
        suitable.sort(key=lambda x: (
            x.department == batch.department,
            -(x.capacity - batch.student_count)  # Prefer closer capacity match
        ), reverse=True)
        
        return suitable
    
    def _is_batch_available(self, batch, time_slot):
        """Check if batch is available at the given time slot"""
        existing = TimetableEntry.objects.filter(
            template=self.template,
            batch=batch,
            time_slot=time_slot
        ).exists()
        
        return not existing
    
    def _is_classroom_available(self, classroom, time_slot):
        """Check if classroom is available at the given time slot"""
        existing = TimetableEntry.objects.filter(
            template=self.template,
            classroom=classroom,
            time_slot=time_slot
        ).exists()
        
        return not existing
    
    def _is_faculty_available(self, faculty, time_slot):
        """Check if faculty is available at the given time slot"""
        existing = TimetableEntry.objects.filter(
            template=self.template,
            faculty=faculty,
            time_slot=time_slot
        ).exists()
        
        return not existing
    
    def _check_faculty_workload(self, faculty, time_slot):
        """Check if faculty workload constraints are satisfied"""
        # Check daily workload
        daily_classes = TimetableEntry.objects.filter(
            template=self.template,
            faculty=faculty,
            time_slot__day=time_slot.day
        ).count()
        
        if daily_classes >= faculty.max_hours_per_day:
            return False
        
        # Check weekly workload
        weekly_classes = TimetableEntry.objects.filter(
            template=self.template,
            faculty=faculty
        ).count()
        
        if weekly_classes >= faculty.max_hours_per_week:
            return False
        
        return True
    
    def _update_tracking(self, faculty, classroom, batch, time_slot):
        """Update internal tracking structures"""
        day_slot = f"{time_slot.day}_{time_slot.start_time}"
        
        self.faculty_workload[faculty.id] += 1
        self.classroom_utilization[classroom.id].append(day_slot)
        self.batch_schedule[batch.id].append(day_slot)
    
    def _resolve_conflicts(self):
        """Try to resolve scheduling conflicts with alternative arrangements"""
        # Implementation for conflict resolution
        # This could include swapping classes, finding alternative time slots, etc.
        pass
    
    def get_optimization_report(self):
        """Generate optimization report with statistics"""
        entries = TimetableEntry.objects.filter(template=self.template)
        
        report = {
            'total_classes_scheduled': entries.count(),
            'classroom_utilization': self._calculate_classroom_utilization(),
            'faculty_workload_distribution': self._calculate_faculty_workload(),
            'conflicts': self.conflicts,
            'suggestions': self._generate_suggestions()
        }
        
        return report
    
    def _calculate_classroom_utilization(self):
        """Calculate classroom utilization statistics"""
        utilization = {}
        
        for classroom in self.classrooms:
            scheduled_slots = TimetableEntry.objects.filter(
                template=self.template,
                classroom=classroom
            ).count()
            
            total_slots = len(self.time_slots)
            utilization_rate = (scheduled_slots / total_slots) * 100 if total_slots > 0 else 0
            
            utilization[classroom.name] = {
                'scheduled': scheduled_slots,
                'total': total_slots,
                'rate': round(utilization_rate, 2)
            }
        
        return utilization
    
    def _calculate_faculty_workload(self):
        """Calculate faculty workload distribution"""
        workload = {}
        
        faculties = Faculty.objects.filter(department=self.template.department)
        
        for faculty in faculties:
            scheduled_hours = TimetableEntry.objects.filter(
                template=self.template,
                faculty=faculty
            ).count()
            
            workload[faculty.user.get_full_name()] = {
                'scheduled': scheduled_hours,
                'max_weekly': faculty.max_hours_per_week,
                'utilization': round((scheduled_hours / faculty.max_hours_per_week) * 100, 2) if faculty.max_hours_per_week > 0 else 0
            }
        
        return workload
    
    def _generate_suggestions(self):
        """Generate suggestions for timetable improvement"""
        suggestions = []
        
        # Check for underutilized resources
        classroom_util = self._calculate_classroom_utilization()
        for classroom, stats in classroom_util.items():
            if stats['rate'] < 50:
                suggestions.append(f"Classroom {classroom} is underutilized ({stats['rate']}%)")
        
        # Check for faculty workload imbalance
        faculty_workload = self._calculate_faculty_workload()
        for faculty, stats in faculty_workload.items():
            if stats['utilization'] > 90:
                suggestions.append(f"Faculty {faculty} has high workload ({stats['utilization']}%)")
            elif stats['utilization'] < 30:
                suggestions.append(f"Faculty {faculty} has low workload ({stats['utilization']}%)")
        
        return suggestions