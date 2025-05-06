// Main JavaScript file for Aaganshiksha

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Flash message auto-dismiss
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');

    // Initialize Bootstrap modals properly
    var modalElements = document.querySelectorAll('.modal');
    modalElements.forEach(function(modalElement) {
        var modal = new bootstrap.Modal(modalElement, {
            backdrop: true,
            keyboard: true,
            focus: true
        });

        // Prevent multiple backdrop issues
        modalElement.addEventListener('show.bs.modal', function() {
            const backdrop = document.querySelector('.modal-backdrop');
            if (backdrop) {
                document.body.classList.add('modal-open');
            }
        });
    });

        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Handle date inputs
    var dateInputs = document.querySelectorAll('input[type="date"]');
    if (dateInputs.length > 0) {
        dateInputs.forEach(function(input) {
            if (!input.value) {
                var today = new Date();
                var year = today.getFullYear();
                var month = String(today.getMonth() + 1).padStart(2, '0');
                var day = String(today.getDate()).padStart(2, '0');
                input.value = `${year}-${month}-${day}`;
            }
        });
    }

    // Add required asterisk to required form fields
    var requiredFields = document.querySelectorAll('input[required], select[required], textarea[required]');
    requiredFields.forEach(function(field) {
        var label = field.previousElementSibling;
        if (label && label.classList.contains('form-label')) {
            label.innerHTML += ' <span class="text-danger">*</span>';
        }
    });

    // Confirm form submission for critical actions
    var dangerForms = document.querySelectorAll('form.confirm-submit');
    dangerForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!confirm('Are you sure you want to perform this action?')) {
                e.preventDefault();
                return false;
            }
        });
    });

    // Table row highlighting on hover
    var tableRows = document.querySelectorAll('table.table-hover tbody tr');
    tableRows.forEach(function(row) {
        row.addEventListener('mouseover', function() {
            this.classList.add('table-active');
        });
        row.addEventListener('mouseout', function() {
            this.classList.remove('table-active');
        });
    });

    // Mobile navigation enhancements
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            document.body.classList.toggle('navbar-open');
        });
    }

    // Form validation enhancement
    const forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();

    // Modal handling - complete rewrite
    document.addEventListener('DOMContentLoaded', function() {
        // Find all modals
        const pageModals = document.querySelectorAll('.modal, .custom-modal');

        if (pageModals.length > 0) {
            // Create backdrop if it doesn't exist
            let modalBackdrop = document.querySelector('.modal-backdrop');
            if (!modalBackdrop) {
                modalBackdrop = document.createElement('div');
                modalBackdrop.className = 'modal-backdrop';
                document.body.appendChild(modalBackdrop);
                modalBackdrop.style.display = 'none';
            }

            // Function to open modal
            function openModal(modal) {
                // Hide all other modals first
                pageModals.forEach(m => {
                    m.style.display = 'none';
                    m.classList.remove('show');
                });

                // Show this modal

// Bootstrap's built-in modal handling is used instead of custom code
// This ensures smoother modal transitions without flickering

                modal.style.display = 'block';
                modal.classList.add('show');
                document.body.classList.add('modal-open');
                modalBackdrop.style.display = 'block';

                // Focus on first input if exists
                const firstInput = modal.querySelector('input, select, textarea');
                if (firstInput) {
                    setTimeout(() => {
                        firstInput.focus();
                    }, 100);
                }
            }

            // Function to close modal
            function closeModal(modal) {
                modal.style.display = 'none';
                modal.classList.remove('show');
                document.body.classList.remove('modal-open');
                modalBackdrop.style.display = 'none';
            }

            // Set up each modal
            pageModals.forEach(function(modal) {
                // Set up triggers
                const modalId = modal.id;
                const modalTriggers = document.querySelectorAll(`[data-bs-target="#${modalId}"]`);

                modalTriggers.forEach(trigger => {
                    trigger.addEventListener('click', function(e) {
                        e.preventDefault();
                        openModal(modal);
                    });
                });

                // Set up close buttons
                const closeButtons = modal.querySelectorAll('.close-modal, .btn-close, [data-dismiss="modal"]');
                closeButtons.forEach(button => {
                    button.addEventListener('click', function() {
                        closeModal(modal);
                    });
                });
            });

            // Close modal when clicking on backdrop
            modalBackdrop.addEventListener('click', function() {
                const visibleModal = document.querySelector('.modal.show, .custom-modal.show');
                if (visibleModal) {
                    closeModal(visibleModal);
                }
            });

            // Close modal on ESC key
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    const visibleModal = document.querySelector('.modal.show, .custom-modal.show');
                    if (visibleModal) {
                        closeModal(visibleModal);
                    }
                }
            });
        }
    });

            }
            form.classList.add('was-validated');
        }, false);
    });

    // Attendance form enhancement
    const statusSelects = document.querySelectorAll('select[name="status"]');
    if (statusSelects.length > 0) {
        statusSelects.forEach(function(select) {
            select.addEventListener('change', function() {
                const row = this.closest('tr');
                // Remove existing status classes
                row.classList.remove('status-present', 'status-absent', 'status-late');
                // Add new status class
                row.classList.add('status-' + this.value);

                // Set default remarks based on status
                const remarksInput = row.querySelector('input[name="remarks"]');
                if (remarksInput) {
                    if (this.value === 'absent' && !remarksInput.value) {
                        remarksInput.value = 'Absent';
                    } else if (this.value === 'late' && !remarksInput.value) {
                        remarksInput.value = 'Late arrival';
                    } else if (this.value === 'present' && (remarksInput.value === 'Absent' || remarksInput.value === 'Late arrival')) {
                        remarksInput.value = '';
                    }
                }
            });
        });
    }

    // Add any custom JavaScript here

// Search auto-suggest functionality
    const searchInput = document.getElementById('searchInput');
    const searchSuggestions = document.getElementById('searchSuggestions');

    if (searchInput) {
        let debounceTimer;

        searchInput.addEventListener('input', function(e) {
            clearTimeout(debounceTimer);
            const query = e.target.value.trim();

            // Clear suggestions if query is too short
            if (query.length < 2) {
                if (searchSuggestions) {
                    searchSuggestions.innerHTML = '';
                    searchSuggestions.style.display = 'none';
                }
                return;
            }

            // Debounce the API call to avoid too many requests
            debounceTimer = setTimeout(() => {
                // Check if we're in the admin or teacher section
                const isAdmin = window.location.pathname.includes('/admin');
                const endpoint = isAdmin ? '/api/admin/search-suggestions' : '/api/teacher/search-suggestions';

                fetch(`${endpoint}?query=${encodeURIComponent(query)}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Search API error');
                        }
                        return response.json();
                    })
                    .then(data => {
                        if (searchSuggestions) {
                            // Clear previous suggestions
                            searchSuggestions.innerHTML = '';

                            if (data.length > 0) {
                                // Create and add suggestion items
                                data.forEach(item => {
                                    const div = document.createElement('div');
                                    div.className = 'search-suggestion-item';

                                    let html = `<strong>${item.name}</strong>`;
                                    if (item.type) {
                                        html += ` <span class="badge bg-secondary">${item.type}</span>`;
                                    }
                                    if (item.aadhar) {
                                        html += ` <small>${item.aadhar}</small>`;
                                    }

                                    div.innerHTML = html;

                                    // Add click event
                                    div.addEventListener('click', () => {
                                        const urlPrefix = isAdmin ? '/admin' : '/teacher';
                                        const urlSuffix = item.type === 'teacher' ? 'user' : 'student';
                                        window.location.href = `${urlPrefix}/search/${urlSuffix}/${item.id}`;
                                    });

                                    searchSuggestions.appendChild(div);
                                });

                                // Show suggestions
                                searchSuggestions.style.display = 'block';
                            } else {
                                // No results
                                const div = document.createElement('div');
                                div.className = 'search-suggestion-item no-results';
                                div.textContent = 'No results found';
                                searchSuggestions.appendChild(div);
                                searchSuggestions.style.display = 'block';
                            }
                        }
                    })
                    .catch(error => {
                        console.error('Search error:', error);
                    });
            }, 300); // 300ms debounce
        });

        // Hide suggestions when clicking outside
        document.addEventListener('click', function(e) {
            if (searchSuggestions && !searchInput.contains(e.target) && !searchSuggestions.contains(e.target)) {
                searchSuggestions.style.display = 'none';
            }
        });
    }
});

// Function to set all status dropdowns at once
function setAllStatuses(status) {
    const statusSelects = document.querySelectorAll('select[name="status"]');
    statusSelects.forEach(function(select) {
        select.value = status;
        // Trigger change event
        const event = new Event('change');
        select.dispatchEvent(event);
    });
}

// Function to toggle password visibility
function togglePasswordVisibility(inputId, iconId) {
    const passwordInput = document.getElementById(inputId);
    const icon = document.getElementById(iconId);

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}