from django.apps import AppConfig


class SchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'
    verbose_name = 'Smart Timetable Scheduler'
    
    def ready(self):
        # Import signal handlers if any
        pass