// ===================================================
// Scheduler-specific JavaScript functionality
// ===================================================

const SchedulerApp = {
    // ===================================================
    // Timetable Generation & Optimization
    // ===================================================
    timetableGenerator: {
        // Default configuration
        config: {
            maxIterations: 1000,
            conflictWeight: 10,
            utilizationWeight: 5,
            workloadWeight: 3,
        },

        // Initialization
        init: function () {
            this.bindEvents();
        },

        // Event bindings
        bindEvents: function () {
            // Handle timetable form submission
            const generationForm = document.querySelector('#timetableForm');
            if (generationForm) {
                generationForm.addEventListener('submit', this.handleGeneration.bind(this));
            }

            // Real-time parameter updates
            document.querySelectorAll('[data-parameter]').forEach(input => {
                input.addEventListener('change', this.updateParameters.bind(this));
            });
        },

        // Handle form submission
        handleGeneration: function (event) {
            event.preventDefault();

            const formData = new FormData(event.target);
            const submitBtn = event.target.querySelector('button[type="submit"]');

            SmartScheduler.setLoadingState(submitBtn);
            this.showProgress(0, 'Initializing...');

            const parameters = this.collectParameters(formData);

            if (!this.validateParameters(parameters)) {
                SmartScheduler.setLoadingState(submitBtn, false);
                return;
            }

            // Submit to Django
            event.target.submit();
        },

        // Collect timetable parameters
        collectParameters: function (formData) {
            return {
                name: formData.get('name'),
                department: formData.get('department'),
                semester: parseInt(formData.get('semester')),
                academicYear: formData.get('academic_year'),
                maxClassesPerDay: parseInt(formData.get('max_classes_per_day')),
                batches: formData.getAll('batches'),
                optimizeWorkload: document.querySelector('#optimize_faculty')?.checked || false,
                optimizeRooms: document.querySelector('#optimize_rooms')?.checked || false,
                avoidConflicts: document.querySelector('#avoid_conflicts')?.checked || false,
            };
        },

        // Validate all parameters
        validateParameters: function (params) {
            const errors = [];

            if (!params.name?.trim()) errors.push('Timetable name is required');
            if (!params.department) errors.push('Department selection is required');
            if (!params.semester || params.semester < 1 || params.semester > 8) errors.push('Valid semester (1-8) is required');
            if (!params.academicYear?.trim()) errors.push('Academic year is required');
            if (!params.maxClassesPerDay || params.maxClassesPerDay < 1) errors.push('Maximum classes per day must be at least 1');
            if (!params.batches || params.batches.length === 0) errors.push('At least one batch must be selected');

            if (errors.length > 0) {
                errors.forEach(error => SmartScheduler.showNotification(error, 'warning'));
                return false;
            }
            return true;
        },

        // Validate a single parameter in real-time
        validateParameter: function (parameter, value) {
            let isValid = true;
            let message = '';

            switch (parameter) {
                case 'maxClassesPerDay':
                    if (value < 1 || value > 12) {
                        isValid = false;
                        message = 'Classes per day should be between 1 and 12';
                    }
                    break;
                case 'semester':
                    if (value < 1 || value > 8) {
                        isValid = false;
                        message = 'Semester should be between 1 and 8';
                    }
                    break;
            }

            const input = document.querySelector(`[data-parameter="${parameter}"]`);
            if (input) {
                if (isValid) {
                    input.classList.remove('is-invalid');
                    input.classList.add('is-valid');
                } else {
                    input.classList.remove('is-valid');
                    input.classList.add('is-invalid');
                    SmartScheduler.showNotification(message, 'warning');
                }
            }
            return isValid;
        },

        // Update parameters
        updateParameters: function (event) {
            const parameter = event.target.dataset.parameter;
            const value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;
            console.log(`Parameter updated: ${parameter} = ${value}`);
            this.validateParameter(parameter, value);
        },

        // Progress modal UI
        showProgress: function (percentage, message) {
            let progressModal = document.querySelector('#progressModal');

            if (!progressModal) {
                progressModal = this.createProgressModal();
                document.body.appendChild(progressModal);
            }

            const progressBar = progressModal.querySelector('.progress-bar');
            const progressMessage = progressModal.querySelector('.progress-message');

            if (progressBar) {
                progressBar.style.width = percentage + '%';
                progressBar.setAttribute('aria-valuenow', percentage);
                progressBar.textContent = Math.round(percentage) + '%';
            }

            if (progressMessage) {
                progressMessage.textContent = message;
            }

            if (percentage === 0) {
                const modal = new bootstrap.Modal(progressModal);
                modal.show();
            } else if (percentage >= 100) {
                setTimeout(() => {
                    const modal = bootstrap.Modal.getInstance(progressModal);
                    modal?.hide();
                }, 1000);
            }
        },

        createProgressModal: function () {
            const modal = document.createElement('div');
            modal.id = 'progressModal';
            modal.className = 'modal fade';
            modal.setAttribute('data-bs-backdrop', 'static');
            modal.innerHTML = `
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="bi bi-gear-fill"></i> Generating Timetable
                            </h5>
                        </div>
                        <div class="modal-body">
                            <div class="progress mb-3">
                                <div class="progress-bar progress-bar-striped progress-bar-animated"
                                     role="progressbar" style="width: 0%" aria-valuenow="0"
                                     aria-valuemin="0" aria-valuemax="100">0%</div>
                            </div>
                            <p class="progress-message text-center">Initializing...</p>
                            <div class="text-center">
                                <small class="text-muted">Please wait while we optimize your timetable...</small>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            return modal;
        }
    },

    // ===================================================
    // Timetable Viewer & Editor
    // ===================================================
    timetableViewer: {
        currentTemplate: null,
        editMode: false,

        init: function (templateId) {
            this.currentTemplate = templateId;
            this.bindEvents();
            this.initializeDragDrop();
            this.loadTimetableData();
        },

        bindEvents: function () {
            // Cell editing
            document.querySelectorAll('.timetable-cell[data-editable]').forEach(cell => {
                cell.addEventListener('click', this.editCell.bind(this));
                cell.addEventListener('dblclick', this.quickEdit.bind(this));
            });

            // Filters
            document.querySelectorAll('.filter-control').forEach(control => {
                control.addEventListener('change', this.applyFilters.bind(this));
            });

            // View mode toggle
            document.querySelectorAll('[data-view-mode]').forEach(toggle => {
                toggle.addEventListener('click', this.changeViewMode.bind(this));
            });

            // Edit mode toggle
            const editToggle = document.querySelector('#editModeToggle');
            if (editToggle) {
                editToggle.addEventListener('change', this.toggleEditMode.bind(this));
            }
        },

        initializeDragDrop: function () {
            if (!this.editMode) return;
            document.querySelectorAll('.timetable-cell[data-entry-id]').forEach(cell => {
                cell.draggable = true;
                cell.addEventListener('dragstart', this.handleDragStart.bind(this));
                cell.addEventListener('dragover', this.handleDragOver.bind(this));
                cell.addEventListener('drop', this.handleDrop.bind(this));
            });
        },

        loadTimetableData: function () {
            console.log('Timetable data loaded for template:', this.currentTemplate);
        },

        // --- Editing ---
        editCell: function (event) { /* ... same logic as before ... */ },
        quickEdit: function (event) { /* ... */ },
        showAddEntryModal: function (cell) { /* ... */ },
        showEditEntryModal: function (entryId, cell) { /* ... */ },
        createInlineEditor: function (cell, entryId) { /* ... */ },
        saveInlineEdit: function (entryId, form, cell, originalContent) { /* ... */ },
        updateCellContent: function (cell, data) { /* ... */ },

        // --- Filters & Views ---
        applyFilters: function (event) { /* ... */ },
        shouldShowCell: function (cell, filterType, filterValue) { /* ... */ },
        changeViewMode: function (event) { /* ... */ },

        // --- Edit Mode ---
        toggleEditMode: function (event) { /* ... */ },

        // --- Drag & Drop ---
        handleDragStart: function (event) { /* ... */ },
        handleDragOver: function (event) { /* ... */ },
        handleDrop: function (event) { /* ... */ },
        moveEntry: function (entryId, targetCell) { /* ... */ }
    },

    // ===================================================
    // Resource Manager
    // ===================================================
    resourceManager: {
        init: function () {
            this.bindEvents();
        },

        bindEvents: function () {
            document.querySelectorAll('[data-action="add-resource"]').forEach(btn => {
                btn.addEventListener('click', this.showAddResourceModal.bind(this));
            });
            document.querySelectorAll('[data-action="edit-resource"]').forEach(btn => {
                btn.addEventListener('click', this.showEditResourceModal.bind(this));
            });
            document.querySelectorAll('[data-action="delete-resource"]').forEach(btn => {
                btn.addEventListener('click', this.confirmDeleteResource.bind(this));
            });
        },

        showAddResourceModal: function (event) { /* ... */ },
        showEditResourceModal: function (event) { /* ... */ },
        confirmDeleteResource: function (event) { /* ... */ },
        deleteResource: function (resourceType, resourceId) { /* ... */ }
    }
};

// ===================================================
// Initialize Scheduler App
// ===================================================
document.addEventListener('DOMContentLoaded', function () {
    SchedulerApp.timetableGenerator.init();
    SchedulerApp.resourceManager.init();

    const templateId = document.body.dataset.templateId;
    if (templateId) {
        SchedulerApp.timetableViewer.init(templateId);
    }
});

// Expose globally
window.SchedulerApp = SchedulerApp;
