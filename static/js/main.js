document.addEventListener('DOMContentLoaded', function() {
    // Initialize animation on scroll
    initAnimations();
    
    // Initialize charts if they exist
    if (document.getElementById('usageChart')) {
        initUsageChart();
    }
    
    if (document.getElementById('savingsChart')) {
        initSavingsChart();
    }
    
    if (document.getElementById('monthlyProgressChart')) {
        initMonthlyProgressChart();
    }
    
    if (document.getElementById('energyBreakdownChart')) {
        initEnergyBreakdownChart();
    }
    
    if (document.getElementById('historyChart')) {
        initHistoryChart();
    }
    
    // Initialize new tip button
    const newTipBtn = document.getElementById('newTipBtn');
    if (newTipBtn) {
        newTipBtn.addEventListener('click', getNewTip);
    }
});

// Animation on scroll
function initAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });
    
    animatedElements.forEach(element => {
        observer.observe(element);
    });
}

// Get a new energy saving tip
function getNewTip() {
    const tipElement = document.getElementById('tip-text') || document.getElementById('currentTip');
    if (!tipElement) return;
    
    fetch('/api/energy-tip/')
        .then(response => response.json())
        .then(data => {
            tipElement.textContent = data.tip;
        })
        .catch(error => {
            console.error('Error fetching tip:', error);
        });
}

// Initialize usage chart
function initUsageChart() {
    fetch('/api/chart-data/')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('usageChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Electricity (kWh)',
                        data: data.electricity,
                        backgroundColor: 'rgba(59, 130, 246, 0.2)',
                        borderColor: 'rgb(59, 130, 246)',
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error fetching chart data:', error);
        });
}

// Initialize savings chart
function initSavingsChart() {
    fetch('/api/chart-data/')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('savingsChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Energy Saved (kWh)',
                        data: data.saved,
                        backgroundColor: 'rgba(34, 197, 94, 0.2)',
                        borderColor: 'rgb(34, 197, 94)',
                        tension: 0.3,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error fetching chart data:', error);
        });
}

// Initialize monthly progress chart
function initMonthlyProgressChart() {
    fetch('/api/chart-data/')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('monthlyProgressChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Energy Saved (kWh)',
                        data: data.saved,
                        backgroundColor: 'rgba(34, 197, 94, 0.2)',
                        borderColor: 'rgb(34, 197, 94)',
                        tension: 0.3,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error fetching chart data:', error);
        });
}

// Initialize energy breakdown chart
function initEnergyBreakdownChart() {
    fetch('/api/chart-data/')
        .then(response => response.json())
        .then(data => {
            // Calculate totals
            const totalElectricity = data.electricity.reduce((a, b) => a + b, 0);
            const totalGas = data.gas.reduce((a, b) => a + b, 0);
            const totalSaved = data.saved.reduce((a, b) => a + b, 0);
            
            const ctx = document.getElementById('energyBreakdownChart').getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Electricity', 'Gas', 'Saved'],
                    datasets: [{
                        data: [totalElectricity, totalGas, totalSaved],
                        backgroundColor: [
                            'rgba(59, 130, 246, 0.7)',
                            'rgba(249, 115, 22, 0.7)',
                            'rgba(34, 197, 94, 0.7)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error fetching chart data:', error);
        });
}

// Initialize history chart
function initHistoryChart() {
    fetch('/api/chart-data/')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('historyChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            label: 'Electricity (kWh)',
                            data: data.electricity,
                            backgroundColor: 'rgba(59, 130, 246, 0.7)'
                        },
                        {
                            label: 'Gas (therms)',
                            data: data.gas,
                            backgroundColor: 'rgba(249, 115, 22, 0.7)'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error fetching chart data:', error);
        });
} 