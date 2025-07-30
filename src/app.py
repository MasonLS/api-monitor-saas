"""
Combined web dashboard and monitoring service
Runs monitoring in a background thread
"""

from flask import Flask, render_template_string, jsonify
import sqlite3
import json
import threading
import time
import os
from datetime import datetime

# Import our monitor
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from monitor import APIMonitor

app = Flask(__name__)

# HTML template (same as before)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>API Monitor Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
        .monitor-card { background: white; padding: 20px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .status-ok { color: #27ae60; font-weight: bold; }
        .status-error { color: #e74c3c; font-weight: bold; }
        .stats { display: flex; justify-content: space-between; margin-top: 10px; }
        .stat-box { text-align: center; padding: 10px; background: #ecf0f1; border-radius: 3px; }
        .cta { background: #3498db; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>API Monitor - Simple Uptime Monitoring</h1>
            <p>Monitor your APIs and get instant alerts when they go down</p>
        </div>
        
        <h2>Live Demo - Monitoring Popular APIs</h2>
        <div id="monitors"></div>
        
        <div style="text-align: center; margin: 40px 0;">
            <h3>Free Tier Demo</h3>
            <p>This is running on Render's free tier. Data resets on restart.</p>
            <p>Upgrade to paid tier for persistent monitoring and more features!</p>
        </div>
    </div>
    
    <script>
        function loadMonitors() {
            fetch('/api/monitors')
                .then(response => response.json())
                .then(data => {
                    const container = document.getElementById('monitors');
                    container.innerHTML = '';
                    
                    if (!data.monitors || data.monitors.length === 0) {
                        container.innerHTML = '<p>No monitors yet. Monitoring will start shortly...</p>';
                        return;
                    }
                    
                    data.monitors.forEach(monitor => {
                        const uptime = monitor.stats_24h.uptime_percentage.toFixed(2);
                        const avgResponse = monitor.stats_24h.avg_response_time ? monitor.stats_24h.avg_response_time.toFixed(3) : 'N/A';
                        const statusClass = uptime == 100 ? 'status-ok' : 'status-error';
                        const statusText = uptime == 100 ? 'Operational' : 'Issues Detected';
                        
                        const card = `
                            <div class="monitor-card">
                                <h3>${monitor.name}</h3>
                                <p>URL: ${monitor.url}</p>
                                <p>Status: <span class="${statusClass}">${statusText}</span></p>
                                <div class="stats">
                                    <div class="stat-box">
                                        <strong>${uptime}%</strong><br>
                                        <small>Uptime (24h)</small>
                                    </div>
                                    <div class="stat-box">
                                        <strong>${avgResponse}s</strong><br>
                                        <small>Avg Response</small>
                                    </div>
                                    <div class="stat-box">
                                        <strong>${monitor.stats_24h.total_checks}</strong><br>
                                        <small>Total Checks</small>
                                    </div>
                                </div>
                            </div>
                        `;
                        container.innerHTML += card;
                    });
                });
        }
        
        // Load monitors on page load and refresh every 30 seconds
        loadMonitors();
        setInterval(loadMonitors, 30000);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/monitors')
def api_monitors():
    # Generate report on the fly
    monitor = APIMonitor(os.environ.get('DATABASE_PATH', '/tmp/api_monitor.db'))
    report = monitor.generate_report()
    return jsonify(report)

def run_monitoring():
    """Background thread for monitoring"""
    monitor = APIMonitor(os.environ.get('DATABASE_PATH', '/tmp/api_monitor.db'))
    
    # Add initial monitors if database is empty
    conn = sqlite3.connect(monitor.db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM monitors')
    count = cursor.fetchone()[0]
    conn.close()
    
    if count == 0:
        print("Adding initial monitors...")
        monitor.add_monitor("GitHub API", "https://api.github.com", check_interval=300)
        monitor.add_monitor("JSONPlaceholder", "https://jsonplaceholder.typicode.com/posts/1", check_interval=300)
        monitor.add_monitor("httpbin.org", "https://httpbin.org/status/200", check_interval=300)
    
    # Run monitoring loop
    while True:
        try:
            conn = sqlite3.connect(monitor.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM monitors WHERE is_active = 1')
            monitors = cursor.fetchall()
            conn.close()
            
            for (monitor_id,) in monitors:
                monitor.check_endpoint(monitor_id)
            
            # Wait 5 minutes before next check
            time.sleep(300)
        except Exception as e:
            print(f"Monitoring error: {e}")
            time.sleep(60)  # Wait 1 minute on error

# Start monitoring in background thread
monitoring_thread = threading.Thread(target=run_monitoring, daemon=True)
monitoring_thread.start()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
