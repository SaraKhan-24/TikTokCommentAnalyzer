let cumulativeStats = {};
let barChart;
let lineChart;

function initCharts() {
    const barCtx = document.getElementById('barChart').getContext('2d');
    barChart = new Chart(barCtx, {
        type: 'bar',
        data: { labels: [], datasets: [{ label: 'Mentions', data: [], backgroundColor: '#3b82f6' }] },
        options: { animation: false }
    });

    const lineCtx = document.getElementById('trendChart').getContext('2d');
    lineChart = new Chart(lineCtx, {
        type: 'line',
        data: { labels: [], datasets: [{ label: 'Batch Hits', data: [], borderColor: '#10b981', tension: 0.1 }] }
    });
}

async function startScan() {
    const keywords = document.getElementById('keywordsInput').value.split(',').map(k => k.trim().toLowerCase());
    
    cumulativeStats = {};
    keywords.forEach(k => cumulativeStats[k] = 0);
    document.getElementById('feed').innerHTML = "";
    
    const res = await fetch('/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'start', keywords: keywords })
    });
    
    const data = await res.json();
    console.log(data.message);
    initCharts();
}

async function refreshData() {
    const keywords = document.getElementById('keywordsInput').value.split(',').map(k => k.trim().toLowerCase());
    
    const res = await fetch('/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'refresh', keywords: keywords })
    });

    const data = await res.json();
    if (data.error) return alert(data.error);
    if (data.new_comments_count === 0) return;

    document.getElementById('totalCount').innerText = data.total_scanned_so_far;
    document.getElementById('batchCount').innerText = data.new_comments_count;

    updateUI(data, keywords);
}

function updateUI(data, keywords) {
    // Update Bar Chart
    keywords.forEach(k => {
        cumulativeStats[k] = (cumulativeStats[k] || 0) + (data.batch_stats[k] || 0);
    });

    barChart.data.labels = Object.keys(cumulativeStats);
    barChart.data.datasets[0].data = Object.values(cumulativeStats);
    barChart.update();

    // Update Line Chart
    const totalHits = Object.values(data.batch_stats).reduce((a, b) => a + b, 0);
    lineChart.data.labels.push(new Date().toLocaleTimeString());
    lineChart.data.datasets[0].data.push(totalHits);
    
    if (lineChart.data.labels.length > 15) {
        lineChart.data.labels.shift();
        lineChart.data.datasets[0].data.shift();
    }
    lineChart.update();

    // Update Feed
    const feed = document.getElementById('feed');
    data.recent_matches.forEach(m => {
        const row = document.createElement('div');
        let border = "border-gray-200";
        if (m.sentiment === "Positive") border = "border-green-500";
        if (m.sentiment === "Negative") border = "border-red-500";

        row.className = `p-3 mb-2 bg-white rounded border-l-4 ${border} shadow-sm text-sm`;
        row.innerHTML = `
            <div class="flex justify-between font-bold mb-1">
                <span>${m.user}</span>
                <span class="text-xs uppercase">${m.sentiment}</span>
            </div>
            <div class="text-gray-600 italic">"${m.text}"</div>
            <div class="text-xs text-blue-500 mt-1">Keywords: ${m.matches.join(', ')}</div>
        `;
        feed.prepend(row);
    });
}