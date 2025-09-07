# Create a setup script for easy project initialization

import os
import sys
import subprocess


def run_command(command, description=""):
    """Run a command and handle errors"""
    print(f"\n{'='*50}")
    print(f"RUNNING: {description or command}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command.split(), check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False


def create_env_file():
    """Create .env file with default settings"""
    env_content = """
# Django Settings
SECRET_KEY=django-insecure-your-secret-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
DATABASE_URL=sqlite:///db.sqlite3

# Optional: For production
# DATABASE_URL=postgresql://user:password@localhost/smart_scheduler

# Security (set to False in production)
CSRF_COOKIE_SECURE=False
SESSION_COOKIE_SECURE=False
"""
    
    with open('.env', 'w') as f:
        f.write(env_content.strip())
    print("✓ Created .env file with default settings")


def create_sample_data():
    """Create a Django management command to load sample data"""
    
    # Create management command directory
    management_dir = 'scheduler/management'
    commands_dir = 'scheduler/management/commands'
    
    os.makedirs(management_dir, exist_ok=True)
    os.makedirs(commands_dir, exist_ok=True)
    
    # Create __init__.py files
    open(f'{management_dir}/__init__.py', 'w').close()
    open(f'{commands_dir}/__init__.py', 'w').close()
    
    # Create sample data command
    sample_data_command = '''
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from scheduler.models import Department, Classroom, Faculty, Subject, TimeSlot
from datetime import time


class Command(BaseCommand):
    help = 'Load sample data for testing'
    
    def handle(self, *args, **options):
        self.stdout.write("Loading sample data...")
        
        # Create departments
        cs_dept = Department.objects.get_or_create(
            name="Computer Science & Engineering",
            code="CSE"
        )[0]
        
        ee_dept = Department.objects.get_or_create(
            name="Electrical Engineering", 
            code="EE"
        )[0]
        
        # Create classrooms
        Classroom.objects.get_or_create(
            name="Room 101",
            capacity=60,
            room_type="lecture",
            department=cs_dept,
            has_projector=True,
            has_ac=True
        )
        
        Classroom.objects.get_or_create(
            name="Lab 201",
            capacity=30,
            room_type="lab", 
            department=cs_dept,
            has_projector=True
        )
        
        # Create time slots
        time_slots = [
            ("monday", time(9, 0), time(10, 0)),
            ("monday", time(10, 0), time(11, 0)),
            ("monday", time(11, 15), time(12, 15)),
            ("monday", time(12, 15), time(13, 15)),
            ("tuesday", time(9, 0), time(10, 0)),
            ("tuesday", time(10, 0), time(11, 0)),
        ]
        
        for day, start_time, end_time in time_slots:
            TimeSlot.objects.get_or_create(
                day=day,
                start_time=start_time,
                end_time=end_time
            )
        
        # Add break time
        TimeSlot.objects.get_or_create(
            day="monday",
            start_time=time(11, 0),
            end_time=time(11, 15),
            is_break=True
        )
        
        self.stdout.write(
            self.style.SUCCESS("Successfully loaded sample data!")
        )
'''
    
    with open(f'{commands_dir}/load_sample_data.py', 'w') as f:
        f.write(sample_data_command)
    
    print("✓ Created sample data management command")


def main():
    """Main setup function"""
    print("="*60)
    print("SMART CLASSROOM & TIMETABLE SCHEDULER SETUP")
    print("Government of Jharkhand - Higher Education Department")
    print("="*60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher required")
        sys.exit(1)
    
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Step 1: Create .env file
    if not os.path.exists('.env'):
        create_env_file()
    else:
        print("✓ .env file already exists")
    
    # Step 2: Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("ERROR: Failed to install dependencies")
        sys.exit(1)
    
    # Step 3: Database setup
    if not run_command("python manage.py makemigrations", "Creating database migrations"):
        print("ERROR: Failed to create migrations")
        sys.exit(1)
    
    if not run_command("python manage.py migrate", "Applying database migrations"):
        print("ERROR: Failed to apply migrations")
        sys.exit(1)
    
    # Step 4: Create sample data command
    create_sample_data()
    
    # Step 5: Load sample data
    if run_command("python manage.py load_sample_data", "Loading sample data"):
        print("✓ Sample data loaded successfully")
    
    # Step 6: Create superuser
    print("\n" + "="*50)
    print("CREATE ADMIN USER")
    print("="*50)
    print("Please create an admin user to access the system:")
    
    if run_command("python manage.py createsuperuser", "Creating admin user"):
        print("✓ Admin user created successfully")
    
    # Final instructions
    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    print("To start the development server:")
    print("  python manage.py runserver")
    print("\nThen visit: http://127.0.0.1:8000")
    print("\nAdmin panel: http://127.0.0.1:8000/admin")
    print("="*60)


if __name__ == "__main__":
    main()