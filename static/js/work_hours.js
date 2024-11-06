let workHoursChart = null;

function initializeWorkHoursChart() {
    const ctx = document.getElementById('workHoursPieChart').getContext('2d');
    workHoursChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: []
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                tooltip: {
                    callbacks: {
                        label: (context) => {
                            const hours = context.raw;
                            return `${context.label}: ${hours.toFixed(1)} hours`;
                        }
                    }
                }
            }
        }
    });

    document.getElementById('timeframeSelect').addEventListener('change', (e) => {
        loadWorkHoursData(e.target.value);
    });

    // Load initial data
    loadWorkHoursData('day');
}

async function loadWorkHoursData(timeframe) {
    try {
        const response = await fetch(`/api/work-hours/${timeframe}`);
        const data = await response.json();
        updateWorkHoursChart(data);
    } catch (error) {
        console.error('Error loading work hours data:', error);
    }
}

function updateWorkHoursChart(data) {
    workHoursChart.data.labels = data.categories;
    workHoursChart.data.datasets[0].data = data.hours;
    workHoursChart.data.datasets[0].backgroundColor = generateColors(data.categories.length);
    workHoursChart.update();
}

function generateColors(count) {
    return Array.from({ length: count }, (_, i) => 
        `hsl(${(i * 360 / count) % 360}, 70%, 60%)`
    );
}

document.addEventListener('DOMContentLoaded', initializeWorkHoursChart);
