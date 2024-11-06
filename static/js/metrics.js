// ...existing code...

let metricsData = null;
let chart = null;

function initializeMetricsControls() {
    const timeSlider = document.getElementById('timeSlider');
    const startDate = document.getElementById('startDate');
    const endDate = document.getElementById('endDate');

    // Set initial dates
    const today = new Date();
    const thirtyDaysAgo = new Date(today);
    thirtyDaysAgo.setDate(today.getDate() - 30);
    
    startDate.value = thirtyDaysAgo.toISOString().split('T')[0];
    endDate.value = today.toISOString().split('T')[0];
    
    timeSlider.addEventListener('input', function() {
        updateChartRange(this.value);
    });
}

function updateDateRange() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    
    fetchAndUpdateMetrics(startDate, endDate);
}

function updateChartRange(sliderValue) {
    if (!metricsData) return;
    
    const dataLength = metricsData.length;
    const windowSize = Math.max(Math.floor(dataLength * (sliderValue / 100)), 1);
    const startIdx = dataLength - windowSize;
    
    const visibleData = metricsData.slice(startIdx);
    updateChart(visibleData);
    updateSliderLabels(visibleData[0].date, visibleData[visibleData.length - 1].date);
}

function updateSliderLabels(startDate, endDate) {
    document.getElementById('sliderStartDate').textContent = formatDate(startDate);
    document.getElementById('sliderEndDate').textContent = formatDate(endDate);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString();
}

async function fetchAndUpdateMetrics(startDate, endDate) {
    try {
        const response = await fetch(`/api/metrics?start=${startDate}&end=${endDate}`);
        metricsData = await response.json();
        updateChart(metricsData);
        document.getElementById('timeSlider').value = 100;
    } catch (error) {
        console.error('Error fetching metrics:', error);
    }
}

// Initialize controls when document loads
document.addEventListener('DOMContentLoaded', initializeMetricsControls);
// ...existing code...
