# Smart Classroom & Timetable Scheduler

## Project Overview

This is a comprehensive web-based timetable scheduling system developed for the Government of Jharkhand's Department of Higher and Technical Education. The system uses intelligent algorithms to generate optimized timetables while considering various constraints and parameters.

## Features

- **Intelligent Scheduling**: Advanced algorithms that consider faculty workload, room capacity, and subject requirements
- **Multi-Parameter Optimization**: Accounts for classroom availability, faculty constraints, and student batch requirements  
- **User-Friendly Interface**: Modern, responsive web interface built with Bootstrap 5
- **Resource Management**: Comprehensive management of departments, classrooms, faculty, subjects, and batches
- **Multiple Export Options**: Export timetables as CSV and print-friendly formats
- **Approval Workflow**: Built-in approval system for competent authorities
- **Conflict Detection**: Automatic detection and resolution of scheduling conflicts
- **Real-time Updates**: Dynamic form updates and real-time parameter validation

## Technology Stack

- **Backend**: Django 4.2.7 (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Bootstrap 5.3.0 with custom CSS
- **Database**: SQLite (development)
- **Icons**: Bootstrap Icons 1.10.0
- **Forms**: Django Crispy Forms with Bootstrap 5

## Key Components

### Models

1. **Department**: Academic departments
2. **Classroom**: Physical classrooms with capacity and features
3. **Faculty**: Teaching staff with workload constraints
4. **Subject**: Courses with credit hours and requirements
5. **Batch**: Student groups
6. **TimeSlot**: Time periods for scheduling
7. **TimetableTemplate**: Timetable configurations
8. **TimetableEntry**: Individual scheduled classes

### Views

- **Dashboard**: Overview with statistics and recent timetables
- **Create Timetable**: Form-based timetable generation
- **View Timetable**: Interactive timetable display
- **Manage Resources**: CRUD operations for all resources
- **Authentication**: Login/logout functionality

### Optimization Algorithm

The system includes a sophisticated optimization engine (`utils.py`) that:

- Assigns classes based on availability constraints
- Minimizes scheduling conflicts
- Optimizes resource utilization
- Balances faculty workloads
- Considers room capacity and features

## License

This project is developed for the Government of Jharkhand under the NEP 2020 initiative.

---

**Developed for**: Department of Higher and Technical Education, Government of Jharkhand  
**Version**: 1.0.0  
**Last Updated**: September 2025
