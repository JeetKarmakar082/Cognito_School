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
- **Database**: SQLite (development) / PostgreSQL (production)
- **Icons**: Bootstrap Icons 1.10.0
- **Forms**: Django Crispy Forms with Bootstrap 5

## Installation Guide

### Prerequisites

- Python 3.8 or higher
- Node.js (optional, for advanced development)
- Git

### Step 1: Clone the Project

```bash
git clone <your-repository-url>
cd smart_scheduler
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

### Step 5: Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Step 6: Load Sample Data (Optional)

```bash
python manage.py loaddata fixtures/sample_data.json
```

### Step 7: Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## Project Structure

```
smart_scheduler/
├── smart_scheduler/
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py             # Main URL configuration
│   ├── wsgi.py             # WSGI configuration
│   └── asgi.py             # ASGI configuration
├── scheduler/              # Main application
│   ├── migrations/         # Database migrations
│   ├── __init__.py
│   ├── admin.py           # Django admin configuration
│   ├── apps.py            # Application configuration
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # Application URLs
│   ├── forms.py           # Django forms
│   └── utils.py           # Utility functions (optimization algorithms)
├── templates/             # HTML templates
│   └── scheduler/
│       ├── base.html      # Base template
│       ├── login.html     # Login page
│       ├── dashboard.html # Dashboard
│       ├── create_timetable.html
│       ├── view_timetable.html
│       └── manage_resources.html
├── static/               # Static files
│   ├── css/
│   │   ├── style.css     # Main styles
│   │   └── dashboard.css # Dashboard-specific styles
│   ├── js/
│   │   ├── main.js       # Main JavaScript
│   │   └── scheduler.js  # Scheduler-specific JS
│   └── images/           # Image assets
├── media/                # User-uploaded files
├── requirements.txt      # Python dependencies
└── manage.py            # Django management script
```

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

## Usage Guide

### 1. Initial Setup

1. Login with superuser credentials
2. Navigate to "Manage Resources"
3. Add departments, classrooms, faculty, subjects, and batches
4. Configure time slots

### 2. Creating Timetables

1. Go to "Create Timetable"
2. Fill in basic information (name, academic year, etc.)
3. Select department and semester
4. Choose batches to include
5. Set optimization parameters
6. Click "Generate Timetable"

### 3. Managing Timetables

1. View generated timetables on the dashboard
2. Review and edit entries if needed
3. Export to CSV or print
4. Approve timetables (for authorized users)

## Customization

### Adding New Features

1. **Models**: Add new fields or models in `models.py`
2. **Views**: Create new views in `views.py`
3. **Templates**: Add HTML templates in `templates/scheduler/`
4. **Styles**: Modify CSS files in `static/css/`
5. **JavaScript**: Add functionality in `static/js/`

### Styling

The system uses a custom CSS framework built on Bootstrap 5:

- Color scheme: Primary (#667eea), Secondary (#764ba2)
- Components: Cards, buttons, forms, tables
- Responsive design for mobile devices
- Print-friendly styles

### Configuration

Key settings in `settings.py`:

- Database configuration
- Static files handling
- Security settings
- Installed apps

## Deployment

### Production Deployment

1. **Environment Variables**: Set production environment variables
2. **Database**: Configure PostgreSQL for production
3. **Static Files**: Configure static file serving (WhiteNoise)
4. **Security**: Update security settings
5. **Server**: Deploy on cloud platforms (AWS, Heroku, etc.)

### Docker Deployment (Optional)

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## API Endpoints

- `/api/department-batches/`: Get batches for a department
- `/api/update-entry/`: Update timetable entries
- `/admin/`: Django admin interface
- `/login/`: Authentication
- `/dashboard/`: Main dashboard
- `/create-timetable/`: Timetable generation
- `/manage-resources/`: Resource management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **Migration Errors**: Run `python manage.py makemigrations` then `python manage.py migrate`
2. **Static Files**: Run `python manage.py collectstatic` for production
3. **Permission Errors**: Ensure proper file permissions
4. **Database Issues**: Check database connection settings

### Debug Mode

Enable debug mode in development:

```python
DEBUG = True
```

## Support

For support and questions:

- Check the documentation
- Review the code comments
- Submit issues on the repository
- Contact the development team

## License

This project is developed for the Government of Jharkhand under the NEP 2020 initiative.

---

**Developed for**: Department of Higher and Technical Education, Government of Jharkhand  
**Version**: 1.0.0  
**Last Updated**: September 2025