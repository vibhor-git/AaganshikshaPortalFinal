// Charts.js - Visualization scripts for Aaganshiksha dashboards

// Function to generate a random color
function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

// Convert hex color to rgba with opacity
function hexToRgba(hex, opacity) {
    let r = parseInt(hex.slice(1, 3), 16);
    let g = parseInt(hex.slice(3, 5), 16);
    let b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r}, ${g}, ${b}, ${opacity})`;
}

// Generate chart colors (primary, secondary, tertiary)
function generateChartColors(count) {
    const baseColors = [
        '#0d6efd', // primary blue
        '#198754', // success green
        '#dc3545', // danger red
        '#ffc107', // warning yellow
        '#0dcaf0', // info cyan
        '#6f42c1', // purple
        '#fd7e14', // orange
        '#20c997', // teal
        '#6c757d'  // secondary gray
    ];
    
    const colors = [];
    const backgroundColors = [];
    
    for (let i = 0; i < count; i++) {
        let color;
        if (i < baseColors.length) {
            color = baseColors[i];
        } else {
            color = getRandomColor();
        }
        colors.push(color);
        backgroundColors.push(hexToRgba(color, 0.2));
    }
    
    return {
        borders: colors,
        backgrounds: backgroundColors
    };
}

// Draw attendance trend chart for dashboard
function drawAttendanceTrendChart(canvasId, labels, datasets) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    // Create chart data
    const chartData = {
        labels: labels,
        datasets: datasets.map((dataset, index) => {
            const colors = generateChartColors(1);
            return {
                label: dataset.label,
                data: dataset.data,
                borderColor: colors.borders[0],
                backgroundColor: colors.backgrounds[0],
                borderWidth: 2,
                tension: 0.3,
                pointRadius: 3,
                pointHoverRadius: 5,
                fill: false
            };
        })
    };
    
    // Create chart configuration
    const config = {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                },
                title: {
                    display: true,
                    text: 'Attendance Trends'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Attendance Percentage (%)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            }
        }
    };
    
    // Create the chart
    new Chart(ctx, config);
}

// Draw student distribution chart
function drawStudentDistributionChart(canvasId, centerLabels, studentCounts) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    // Generate colors
    const colors = generateChartColors(centerLabels.length);
    
    // Create chart data
    const data = {
        labels: centerLabels,
        datasets: [{
            label: 'Number of Students',
            data: studentCounts,
            backgroundColor: colors.backgrounds,
            borderColor: colors.borders,
            borderWidth: 1
        }]
    };
    
    // Create chart configuration
    const config = {
        type: 'pie',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                title: {
                    display: true,
                    text: 'Student Distribution by Center'
                }
            }
        }
    };
    
    // Create the chart
    new Chart(ctx, config);
}

// Draw inventory status chart
function drawInventoryStatusChart(canvasId, itemLabels, quantities) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    // Generate colors
    const colors = generateChartColors(itemLabels.length);
    
    // Create chart data
    const data = {
        labels: itemLabels,
        datasets: [{
            label: 'Quantity',
            data: quantities,
            backgroundColor: colors.backgrounds,
            borderColor: colors.borders,
            borderWidth: 1
        }]
    };
    
    // Create chart configuration
    const config = {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Inventory Status'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Quantity'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Items'
                    }
                }
            }
        }
    };
    
    // Create the chart
    new Chart(ctx, config);
}

// Draw activity timeline chart
function drawActivityTimelineChart(canvasId, activityLabels, dates) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    // Parse dates to timestamps for chart
    const timestamps = dates.map(date => new Date(date).getTime());
    const minDate = Math.min(...timestamps);
    const maxDate = Math.max(...timestamps);
    
    // Generate colors
    const colors = generateChartColors(activityLabels.length);
    
    // Create chart data
    const data = {
        labels: activityLabels,
        datasets: [{
            label: 'Activities',
            data: timestamps.map((ts, index) => ({
                x: ts,
                y: index
            })),
            backgroundColor: colors.backgrounds,
            borderColor: colors.borders,
            borderWidth: 1,
            pointRadius: 6,
            pointHoverRadius: 8
        }]
    };
    
    // Create chart configuration
    const config = {
        type: 'scatter',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Activity Timeline'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const index = context.dataIndex;
                            const label = context.chart.data.labels[index];
                            const date = new Date(context.parsed.x).toLocaleDateString();
                            return `${label}: ${date}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: activityLabels.length,
                    ticks: {
                        stepSize: 1,
                        callback: function(value) {
                            if (value < activityLabels.length) {
                                return activityLabels[value];
                            }
                            return '';
                        }
                    },
                    grid: {
                        display: false
                    }
                },
                x: {
                    type: 'time',
                    time: {
                        unit: 'day'
                    },
                    min: minDate - 86400000, // one day before
                    max: maxDate + 86400000, // one day after
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            }
        }
    };
    
    // Create the chart
    new Chart(ctx, config);
}

// Draw attendance status distribution chart
function drawAttendanceStatusChart(canvasId, presentCount, absentCount, lateCount) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    // Create chart data
    const data = {
        labels: ['Present', 'Absent', 'Late'],
        datasets: [{
            data: [presentCount, absentCount, lateCount],
            backgroundColor: [
                'rgba(40, 167, 69, 0.7)',  // green for present
                'rgba(220, 53, 69, 0.7)',  // red for absent
                'rgba(255, 193, 7, 0.7)'   // yellow for late
            ],
            borderColor: [
                'rgb(40, 167, 69)',
                'rgb(220, 53, 69)',
                'rgb(255, 193, 7)'
            ],
            borderWidth: 1
        }]
    };
    
    // Create chart configuration
    const config = {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                title: {
                    display: true,
                    text: 'Attendance Status Distribution'
                }
            }
        }
    };
    
    // Create the chart
    new Chart(ctx, config);
}

// Initialize dashboard charts 
function initializeDashboardCharts() {
    // If we're on admin or teacher dashboard
    if (document.querySelector('.dashboard-charts')) {
        // Sample data for demonstration - this will be replaced with actual data from API
        const weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
        
        // Attendance trends (for both admin and teacher dashboards)
        if (document.getElementById('attendanceTrendChart')) {
            const attendanceData = [
                {
                    label: 'Center 1',
                    data: [85, 82, 88, 90, 86, 70, 75]
                },
                {
                    label: 'Center 2',
                    data: [78, 80, 75, 82, 84, 65, 70]
                }
            ];
            
            drawAttendanceTrendChart('attendanceTrendChart', weekdays, attendanceData);
        }
        
        // Student distribution chart (admin dashboard)
        if (document.getElementById('studentDistributionChart')) {
            const centerLabels = ['Center 1', 'Center 2', 'Center 3', 'Center 4'];
            const studentCounts = [45, 30, 25, 20];
            
            drawStudentDistributionChart('studentDistributionChart', centerLabels, studentCounts);
        }
        
        // Inventory status chart (admin/teacher dashboard)
        if (document.getElementById('inventoryStatusChart')) {
            const itemLabels = ['Rice', 'Milk', 'Notebooks', 'Pencils', 'Toys'];
            const quantities = [50, 20, 100, 200, 30];
            
            drawInventoryStatusChart('inventoryStatusChart', itemLabels, quantities);
        }
        
        // Activity timeline chart (admin dashboard)
        if (document.getElementById('activityTimelineChart')) {
            const activityLabels = [
                'Story Telling Session',
                'Art and Craft',
                'Sports Day',
                'Parents Meeting',
                'Health Checkup'
            ];
            const activityDates = [
                '2023-07-05',
                '2023-07-07',
                '2023-07-10',
                '2023-07-15',
                '2023-07-20'
            ];
            
            drawActivityTimelineChart('activityTimelineChart', activityLabels, activityDates);
        }
    }
    
    // If we're on the attendance view page
    if (document.getElementById('attendanceStatusChart')) {
        // Get attendance counts from page
        const presentCount = parseInt(document.getElementById('presentCount').textContent);
        const absentCount = parseInt(document.getElementById('absentCount').textContent);
        const lateCount = parseInt(document.getElementById('lateCount').textContent);
        
        drawAttendanceStatusChart('attendanceStatusChart', presentCount, absentCount, lateCount);
    }
}

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Check if Chart.js is loaded and if we have charts to initialize
    if (typeof Chart !== 'undefined' && 
        (document.querySelector('.dashboard-charts') || 
         document.getElementById('attendanceStatusChart'))) {
        initializeDashboardCharts();
    }
});

// Update charts when window is resized
window.addEventListener('resize', function() {
    if (typeof Chart !== 'undefined' && 
        (document.querySelector('.dashboard-charts') || 
         document.getElementById('attendanceStatusChart'))) {
        // Destroy and reinitialize charts for better responsiveness
        Chart.instances.forEach(instance => instance.destroy());
        initializeDashboardCharts();
    }
});
