let currentDate = new Date();
let dailyChart = null;
let dailyData = null;

function initializeDailyControls() {
    document.getElementById('prevDay').addEventListener('click', () => navigateDay(-1));
    document.getElementById('nextDay').addEventListener('click', () => navigateDay(1));
    document.getElementById('visualRange').addEventListener('input', updateVisualRange);
    updateDateDisplay();
    loadDailyData();
}

function navigateDay(offset) {
    currentDate.setDate(currentDate.getDate() + offset);
    updateDateDisplay();
    loadDailyData();
}

function updateDateDisplay() {
    document.getElementById('currentDate').textContent = 
        currentDate.toLocaleDateString('en-US', { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        });
}

function updateVisualRange(e) {
    const value = e.target.value;
    // Convert slider value (0-100) to hours (0-24)
    const startHour = Math.floor((value / 100) * 24);
    const endHour = 24;
    updateGraphTimeframe(startHour, endHour);
}

function updateGraphTimeframe(startHour, endHour) {
    if (!dailyData || !dailyChart) return;

    // Filter data points within the selected time range
    const filteredData = dailyData.filter(point => {
        const hour = new Date(point.timestamp).getHours();
        return hour >= startHour && hour <= endHour;
    });

    // Update chart with filtered data
    dailyChart.data.labels = filteredData.map(point => {
        const date = new Date(point.timestamp);
        return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    });

    dailyChart.data.datasets.forEach((dataset, i) => {
        dataset.data = filteredData.map(point => point.values[i]);
    });

    dailyChart.update();
}

function updateGraphData(data) {
    dailyData = data;
    
    if (!dailyChart) {
        const ctx = document.getElementById('dailyMetricsGraph').getContext('2d');
        dailyChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: data.metrics.map(metric => ({
                    label: metric.name,
                    data: [],
                    borderColor: metric.color || generateColor(),
                    fill: false,
                    tension: 0.4
                }))
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Time'
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Value'
                        }
                    }
                }
            }
        });
    }

    // Initialize with full day view
    updateGraphTimeframe(0, 24);
}

function generateColor() {
    return `hsl(${Math.random() * 360}, 70%, 50%)`;
}

async function loadDailyData() {
    try {
        const response = await fetch(`/api/daily-data/${currentDate.toISOString().split('T')[0]}`);
        const data = await response.json();
        updateGraphData(data);
    } catch (error) {
        console.error('Error loading daily data:', error);
    }
}

document.addEventListener('DOMContentLoaded', initializeDailyControls);
