// College-specific enhancements for the Smart Scheduler

class CollegeEnhancements {
    constructor() {
        this.init();
    }

    init() {
        this.setupAnimations();
        this.setupInteractiveElements();
        this.setupNotificationSystem();
        this.setupSearchFunctionality();
        this.setupThemeToggle();
        this.setupAccessibility();
    }

    setupAnimations() {
        // Intersection Observer for fade-in animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                    
                    // Special handling for stat counters
                    if (entry.target.classList.contains('stat-number')) {
                        this.animateCounter(entry.target);
                    }
                }
            });
        }, observerOptions);

        // Observe elements for animation
        document.querySelectorAll('.card, .stat-item, .activity-item').forEach(el => {
            observer.observe(el);
        });
    }

    animateCounter(element) {
        const finalValue = parseInt(element.textContent) || 0;
        const duration = 2000;
        const increment = finalValue / (duration / 16);
        let currentValue = 0;

        const timer = setInterval(() => {
            currentValue += increment;
            if (currentValue >= finalValue) {
                element.textContent = finalValue;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(currentValue);
            }
        }, 16);
    }

    setupInteractiveElements() {
        // Enhanced hover effects for cards
        document.querySelectorAll('.card, .timetable-cell').forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px)';
                this.style.transition = 'all 0.3s ease';
            });

            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        });

        // Interactive timetable cells
        document.querySelectorAll('.timetable-cell.occupied').forEach(cell => {
            cell.addEventListener('click', function() {
                this.showCellDetails();
            });
        });

        // Progress bars animation
        document.querySelectorAll('.progress-bar').forEach(bar => {
            const width = bar.style.width;
            bar.style.width = '0%';
            setTimeout(() => {
                bar.style.width = width;
                bar.style.transition = 'width 1s ease-in-out';
            }, 500);
        });
    }

    setupNotificationSystem() {
        // Create notification container if it doesn't exist
        if (!document.querySelector('.notification-container')) {
            const container = document.createElement('div');
            container.className = 'notification-container position-fixed top-0 end-0 p-3';
            container.style.zIndex = '1060';
            document.body.appendChild(container);
        }

        // Auto-dismiss notifications
        this.setupAutoNotifications();
    }

    setupAutoNotifications() {
        // Show system status notifications
        setTimeout(() => {
            this.showNotification('System synchronized successfully', 'success', 3000);
        }, 2000);

        // Check for updates periodically
        setInterval(() => {
            this.checkSystemUpdates();
        }, 300000); // Check every 5 minutes
    }

    showNotification(message, type = 'info', duration = 5000) {
        const container = document.querySelector('.notification-container');
        if (!container) return;

        const notification = document.createElement('div');
        const id = 'notification-' + Date.now();
        
        const icons = {
            success: 'bi-check-circle',
            error: 'bi-exclamation-triangle',
            warning: 'bi-exclamation-circle',
            info: 'bi-info-circle'
        };

        notification.innerHTML = `
            <div id="${id}" class="toast align-items-center text-white bg-${type} border-0 mb-2" role="alert">
                <div class="d-flex">
                    <div class="toast-body">
                        <i class="bi ${icons[type]} me-2"></i>${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;

        container.appendChild(notification);

        const toast = new bootstrap.Toast(document.getElementById(id), {
            delay: duration
        });

        toast.show();

        // Remove from DOM after hiding
        document.getElementById(id).addEventListener('hidden.bs.toast', function() {
            this.remove();
        });
    }

    checkSystemUpdates() {
        // Simulate system status check
        const random = Math.random();
        if (random < 0.1) { // 10% chance of showing an update
            this.showNotification('New timetable optimization available', 'info');
        }
    }

    setupSearchFunctionality() {
        const searchInput = document.querySelector('input[type="search"]');
        if (searchInput) {
            let searchTimeout;
            
            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    this.performSearch(e.target.value);
                }, 300);
            });

            // Add search suggestions
            this.addSearchSuggestions(searchInput);
        }
    }

    performSearch(query) {
        if (query.length < 2) return;

        // Simulate search (in real app, this would be an API call)
        console.log('Searching for:', query);
        
        // Show search loading state
        const searchButton = document.querySelector('button[type="submit"]');
        if (searchButton) {
            const originalContent = searchButton.innerHTML;
            searchButton.innerHTML = '<i class="bi bi-hourglass-split"></i>';
            
            setTimeout(() => {
                searchButton.innerHTML = originalContent;
            }, 1000);
        }
    }

    addSearchSuggestions(searchInput) {
        const suggestions = [
            'Computer Science Department',
            'Faculty Workload Report',
            'Classroom Utilization',
            'Semester 3 Timetable',
            'Laboratory Schedules'
        ];

        searchInput.addEventListener('focus', () => {
            // Create and show suggestions dropdown
            this.showSearchSuggestions(searchInput, suggestions);
        });
    }

    showSearchSuggestions(input, suggestions) {
        // Remove existing dropdown
        const existing = document.querySelector('.search-suggestions');
        if (existing) existing.remove();

        const dropdown = document.createElement('div');
        dropdown.className = 'search-suggestions position-absolute bg-white border rounded shadow-lg';
        dropdown.style.cssText = `
            top: 100%;
            left: 0;
            right: 0;
            z-index: 1000;
            max-height: 200px;
            overflow-y: auto;
        `;

        suggestions.forEach(suggestion => {
            const item = document.createElement('div');
            item.className = 'dropdown-item';
            item.textContent = suggestion;
            item.style.cursor = 'pointer';
            
            item.addEventListener('click', () => {
                input.value = suggestion;
                dropdown.remove();
            });
            
            dropdown.appendChild(item);
        });

        input.parentElement.style.position = 'relative';
        input.parentElement.appendChild(dropdown);

        // Remove dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!input.parentElement.contains(e.target)) {
                dropdown.remove();
            }
        }, { once: true });
    }

    setupThemeToggle() {
        // Add theme toggle button to navigation
        const navbar = document.querySelector('.navbar .navbar-nav:last-child');
        if (navbar) {
            const themeToggle = document.createElement('li');
            themeToggle.className = 'nav-item';
            themeToggle.innerHTML = `
                <button class="nav-link btn btn-link" id="themeToggle" title="Toggle Theme">
                    <i class="bi bi-sun-fill"></i>
                </button>
            `;
            
            navbar.insertBefore(themeToggle, navbar.firstChild);
            
            document.getElementById('themeToggle').addEventListener('click', () => {
                this.toggleTheme();
            });
        }
        
        // Initialize theme from localStorage
        this.initTheme();
    }

    initTheme() {
        const savedTheme = localStorage.getItem('college-theme') || 'light';
        document.body.setAttribute('data-theme', savedTheme);
        this.updateThemeIcon(savedTheme);
    }

    toggleTheme() {
        const currentTheme = document.body.getAttribute('data-theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        document.body.setAttribute('data-theme', newTheme);
        localStorage.setItem('college-theme', newTheme);
        this.updateThemeIcon(newTheme);
    }

    updateThemeIcon(theme) {
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            const icon = themeToggle.querySelector('i');
            icon.className = theme === 'light' ? 'bi bi-moon-fill' : 'bi bi-sun-fill';
        }
    }

    setupAccessibility() {
        // Add keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                // Close any open modals or dropdowns
                const openModal = document.querySelector('.modal.show');
                if (openModal) {
                    bootstrap.Modal.getInstance(openModal).hide();
                }
            }
        });

        // Add focus indicators
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-navigation');
            }
        });

        document.addEventListener('mousedown', () => {
            document.body.classList.remove('keyboard-navigation');
        });

        // Add skip to main content link
        this.addSkipLink();
    }

    addSkipLink() {
        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.className = 'skip-link position-absolute';
        skipLink.textContent = 'Skip to main content';
        skipLink.style.cssText = `
            top: -40px;
            left: 6px;
            background: var(--primary-blue);
            color: white;
            padding: 8px;
            text-decoration: none;
            border-radius: 4px;
            z-index: 1000;
            transition: top 0.3s;
        `;

        skipLink.addEventListener('focus', () => {
            skipLink.style.top = '6px';
        });

        skipLink.addEventListener('blur', () => {
            skipLink.style.top = '-40px';
        });

        document.body.insertBefore(skipLink, document.body.firstChild);
    }
}

// Academic Calendar Integration
class AcademicCalendar {
    constructor() {
        this.currentSemester = this.getCurrentSemester();
        this.academicYear = '2024-25';
        this.init();
    }

    init() {
        this.displaySemesterInfo();
        this.setupCalendarWidget();
    }

    getCurrentSemester() {
        const now = new Date();
        const month = now.getMonth() + 1; // JavaScript months are 0-indexed
        
        if (month >= 7 && month <= 12) {
            return { number: 1, name: 'First Semester', season: 'Autumn' };
        } else {
            return { number: 2, name: 'Second Semester', season: 'Spring' };
        }
    }

    displaySemesterInfo() {
        const semesterInfo = document.querySelector('.current-semester-info');
        if (semesterInfo) {
            semesterInfo.innerHTML = `
                <h5 class="mb-2">Current Academic Session</h5>
                <p class="mb-1"><strong>${this.academicYear} | ${this.currentSemester.name}</strong></p>
                <small>Session ends in ${this.getDaysUntilSemesterEnd()} days</small>
            `;
        }
    }

    getDaysUntilSemesterEnd() {
        const now = new Date();
        const endDate = this.currentSemester.number === 1 
            ? new Date(now.getFullYear(), 11, 31) // December 31
            : new Date(now.getFullYear(), 4, 31); // May 31
        
        const diffTime = endDate - now;
        return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    }

    setupCalendarWidget() {
        // Add mini calendar to sidebar if exists
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            const calendarWidget = this.createCalendarWidget();
            sidebar.appendChild(calendarWidget);
        }
    }

    createCalendarWidget() {
        const widget = document.createElement('div');
        widget.className = 'sidebar-section';
        
        const now = new Date();
        const monthName = now.toLocaleString('default', { month: 'long' });
        
        widget.innerHTML = `
            <h5 class="sidebar-title mb-3">
                <i class="bi bi-calendar-month me-2"></i>Academic Calendar
            </h5>
            <div class="calendar-widget">
                <div class="calendar-header text-center mb-2">
                    <strong>${monthName} ${now.getFullYear()}</strong>
                </div>
                <div style="display:grid; grid-template-columns: 1fr 1fr 1fr;" class="calendar-events">
                    <div class="event-item mb-2">
                        <span class="event-date badge bg-primary">15</span>
                        <span class="event-title">Mid-term Exams</span>
                    </div>
                    <div class="event-item mb-2">
                        <span class="event-date badge bg-warning">22</span>
                        <span class="event-title">Faculty Meeting</span>
                    </div>
                    <div class="event-item mb-2">
                        <span class="event-date badge bg-success">30</span>
                        <span class="event-title">Semester Review</span>
                    </div>
                </div>
            </div>
        `;
        return widget;
    }
}

// Performance Monitor
class PerformanceMonitor {
    constructor() {
        this.metrics = {
            loadTime: 0,
            renderTime: 0,
            interactions: 0
        };
        this.init();
    }

    init() {
        this.measureLoadTime();
        this.setupInteractionTracking();
        this.monitorMemoryUsage();
    }

    measureLoadTime() {
        window.addEventListener('load', () => {
            this.metrics.loadTime = performance.now();
            console.log(`Page loaded in ${Math.round(this.metrics.loadTime)}ms`);
            
            // Show performance notification for slow loads
            if (this.metrics.loadTime > 3000) {
                this.showPerformanceWarning();
            }
        });
    }

    setupInteractionTracking() {
        document.addEventListener('click', () => {
            this.metrics.interactions++;
        });

        // Log performance metrics every 5 minutes
        setInterval(() => {
            console.log('Performance Metrics:', this.metrics);
        }, 300000);
    }

    monitorMemoryUsage() {
        if ('memory' in performance) {
            setInterval(() => {
                const memory = performance.memory;
                const memoryUsage = Math.round(memory.usedJSHeapSize / 1048576);
                
                if (memoryUsage > 50) { // Alert if using more than 50MB
                    console.warn(`High memory usage: ${memoryUsage}MB`);
                }
            }, 60000); // Check every minute
        }
    }

    showPerformanceWarning() {
        const warning = document.createElement('div');
        warning.className = 'alert alert-warning alert-dismissible fade show position-fixed';
        warning.style.cssText = 'top: 20px; right: 20px; z-index: 1060; max-width: 300px;';
        warning.innerHTML = `
            <i class="bi bi-speedometer2 me-2"></i>
            <strong>Slow Connection Detected</strong><br>
            The system may respond slowly due to network conditions.
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(warning);
        
        setTimeout(() => {
            if (warning.parentNode) {
                warning.remove();
            }
        }, 10000);
    }
}

// Initialize all enhancements when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new CollegeEnhancements();
    new AcademicCalendar();
    new PerformanceMonitor();
    
    // Add loading states to all forms
    document.querySelectorAll('form[method="post"]').forEach(form => {
        form.addEventListener('submit', function() {
            const loadingOverlay = document.getElementById('loadingOverlay');
            if (loadingOverlay) {
                loadingOverlay.classList.remove('d-none');
            }
        });
    });
});

// Export for global access
window.CollegeEnhancements = CollegeEnhancements;