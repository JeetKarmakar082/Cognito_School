// Main JavaScript for Smart Scheduler

// Global configuration
const SmartScheduler = {
    config: {
        apiEndpoints: {
            getDepartmentBatches: '/api/department-batches/',
            updateTimetableEntry: '/api/update-entry/',
        },
        csrf_token: document.querySelector('[name=csrfmiddlewaretoken]')?.value || '',
    },
    
    // Initialize the application
    init: function() {
        this.bindEvents();
        this.initializeComponents();
    },
    
    // Bind global event listeners
    bindEvents: function() {
        // Auto-dismiss alerts after 5 seconds
        document.querySelectorAll('.alert').forEach(alert => {
            setTimeout(() => {
                if (alert.querySelector('.btn-close')) {
                    alert.querySelector('.btn-close').click();
                }
            }, 5000);
        });
        
        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            });
        });
        
        // Form validation enhancement
        this.enhanceFormValidation();
    },
    
    // Initialize components
    initializeComponents: function() {
        // Initialize tooltips
        this.initTooltips();
        
        // Initialize modals
        this.initModals();
        
        // Initialize notifications
        this.initNotifications();
    },
    
    // Enhanced form validation
    enhanceFormValidation: function() {
        const forms = document.querySelectorAll('.needs-validation');
        
        forms.forEach(form => {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                    
                    // Focus on first invalid field
                    const firstInvalid = form.querySelector(':invalid');
                    if (firstInvalid) {
                        firstInvalid.focus();
                        firstInvalid.scrollIntoView({
                            behavior: 'smooth',
                            block: 'center'
                        });
                    }
                }
                form.classList.add('was-validated');
            });
            
            // Real-time validation
            const inputs = form.querySelectorAll('input, select, textarea');
            inputs.forEach(input => {
                input.addEventListener('blur', function() {
                    if (this.checkValidity()) {
                        this.classList.remove('is-invalid');
                        this.classList.add('is-valid');
                    } else {
                        this.classList.remove('is-valid');
                        this.classList.add('is-invalid');
                    }
                });
            });
        });
    },
    
    // Initialize tooltips
    initTooltips: function() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    },
    
    // Initialize modals
    initModals: function() {
        // Auto-focus first input in modals
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('shown.bs.modal', function() {
                const firstInput = this.querySelector('input, select, textarea');
                if (firstInput) {
                    firstInput.focus();
                }
            });
        });
    },
    
    // Initialize notifications
    initNotifications: function() {
        // Create notification container if it doesn't exist
        if (!document.querySelector('.notification-container')) {
            const container = document.createElement('div');
            container.className = 'notification-container position-fixed top-0 end-0 p-3';
            container.style.zIndex = '1055';
            document.body.appendChild(container);
        }
    },
    
    // Show notification
    showNotification: function(message, type = 'info', duration = 5000) {
        const container = document.querySelector('.notification-container');
        if (!container) return;
        
        const notification = document.createElement('div');
        const id = 'notification-' + Date.now();
        
        notification.innerHTML = `
            <div id="${id}" class="toast align-items-center text-white bg-${type} border-0" role="alert">
                <div class="d-flex">
                    <div class="toast-body">
                        ${message}
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
    },
    
    // Loading state management
    setLoadingState: function(element, loading = true) {
        if (loading) {
            element.disabled = true;
            element.classList.add('loading');
            
            // Add spinner if it's a button
            if (element.tagName === 'BUTTON') {
                const spinner = document.createElement('span');
                spinner.className = 'spinner-border spinner-border-sm me-2';
                spinner.setAttribute('role', 'status');
                element.insertBefore(spinner, element.firstChild);
            }
        } else {
            element.disabled = false;
            element.classList.remove('loading');
            
            // Remove spinner
            const spinner = element.querySelector('.spinner-border');
            if (spinner) {
                spinner.remove();
            }
        }
    },
    
    // AJAX utility
    ajax: function(url, options = {}) {
        const defaults = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.config.csrf_token,
            },
        };
        
        const config = Object.assign(defaults, options);
        
        return fetch(url, config)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .catch(error => {
                console.error('AJAX Error:', error);
                this.showNotification('An error occurred. Please try again.', 'danger');
                throw error;
            });
    },
    
    // Utility functions
    utils: {
        // Debounce function
        debounce: function(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },
        
        // Format date
        formatDate: function(date, format = 'YYYY-MM-DD') {
            if (!(date instanceof Date)) {
                date = new Date(date);
            }
            
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            
            return format
                .replace('YYYY', year)
                .replace('MM', month)
                .replace('DD', day);
        },
        
        // Format time
        formatTime: function(time) {
            if (typeof time === 'string') {
                return time;
            }
            
            const hours = String(time.getHours()).padStart(2, '0');
            const minutes = String(time.getMinutes()).padStart(2, '0');
            return `${hours}:${minutes}`;
        },
        
        // Capitalize first letter
        capitalize: function(str) {
            return str.charAt(0).toUpperCase() + str.slice(1);
        },
        
        // Generate random ID
        generateId: function() {
            return Math.random().toString(36).substr(2, 9);
        }
    }
};

// Department-Batch filtering functionality
const DepartmentBatchFilter = {
    init: function() {
        const departmentSelect = document.querySelector('[name="department"]');
        const semesterSelect = document.querySelector('[name="semester"]');
        const batchesSelect = document.querySelector('[name="batches"]');
        
        if (departmentSelect && semesterSelect && batchesSelect) {
            departmentSelect.addEventListener('change', () => this.updateBatches());
            semesterSelect.addEventListener('change', () => this.updateBatches());
        }
    },
    
    updateBatches: function() {
        const departmentSelect = document.querySelector('[name="department"]');
        const semesterSelect = document.querySelector('[name="semester"]');
        const batchesSelect = document.querySelector('[name="batches"]');
        
        const departmentId = departmentSelect.value;
        const semester = semesterSelect.value;
        
        if (!departmentId || !semester) {
            this.clearBatches();
            return;
        }
        
        SmartScheduler.setLoadingState(batchesSelect);
        
        SmartScheduler.ajax(
            `${SmartScheduler.config.apiEndpoints.getDepartmentBatches}?department_id=${departmentId}&semester=${semester}`
        )
        .then(data => {
            this.populateBatches(data.batches);
        })
        .catch(error => {
            console.error('Error fetching batches:', error);
        })
        .finally(() => {
            SmartScheduler.setLoadingState(batchesSelect, false);
        });
    },
    
    clearBatches: function() {
        const batchesSelect = document.querySelector('[name="batches"]');
        batchesSelect.innerHTML = '<option value="">Select Department and Semester first</option>';
    },
    
    populateBatches: function(batches) {
        const batchesSelect = document.querySelector('[name="batches"]');
        
        if (batches.length === 0) {
            batchesSelect.innerHTML = '<option value="">No batches found</option>';
            return;
        }
        
        batchesSelect.innerHTML = '';
        batches.forEach(batch => {
            const option = document.createElement('option');
            option.value = batch.id;
            option.textContent = `${batch.name} - Semester ${batch.semester}`;
            batchesSelect.appendChild(option);
        });
    }
};

// Timetable viewer functionality
const TimetableViewer = {
    init: function() {
        this.bindEvents();
        this.initializeFilters();
    },
    
    bindEvents: function() {
        // Export functionality
        document.querySelectorAll('[data-action="export"]').forEach(btn => {
            btn.addEventListener('click', this.exportTimetable);
        });
        
        // Print functionality
        document.querySelectorAll('[data-action="print"]').forEach(btn => {
            btn.addEventListener('click', this.printTimetable);
        });
        
        // Edit cell functionality
        document.querySelectorAll('.timetable-cell[data-editable="true"]').forEach(cell => {
            cell.addEventListener('click', this.editCell);
        });
    },
    
    initializeFilters: function() {
        const filterForm = document.querySelector('#timetableFilters');
        if (filterForm) {
            filterForm.addEventListener('change', this.applyFilters);
        }
    },
    
    exportTimetable: function(event) {
        const templateId = event.target.dataset.templateId;
        if (templateId) {
            window.location.href = `/timetable/${templateId}/export/`;
        }
    },
    
    printTimetable: function() {
        window.print();
    },
    
    editCell: function(event) {
        const cell = event.currentTarget;
        const entryId = cell.dataset.entryId;
        
        if (!entryId) return;
        
        // Show edit modal or inline editor
        console.log('Editing cell:', entryId);
    },
    
    applyFilters: function(event) {
        const formData = new FormData(event.target.closest('form'));
        const params = new URLSearchParams(formData);
        
        // Reload page with filters
        window.location.search = params.toString();
    }
};

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    SmartScheduler.init();
    DepartmentBatchFilter.init();
    TimetableViewer.init();
});

// Global error handler
window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
    SmartScheduler.showNotification('An unexpected error occurred.', 'danger');
});

// Service worker registration (for offline functionality)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(error) {
                console.log('ServiceWorker registration failed');
            });
    });
}

// Export for use in other modules
window.SmartScheduler = SmartScheduler;