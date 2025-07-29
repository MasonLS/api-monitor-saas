#!/usr/bin/env python3
"""
Simple Web Dashboard for API Monitor
Using Flask for quick deployment
"""

from flask import Flask, render_template_string, jsonify, request
import sqlite3
import json
from datetime import datetime, timedelta

app = Flask(__name__)

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
        .pricing { display: flex; justify-content: space-around; margin: 40px 0; }
        .price-card { background: white; padding: 30px; border-radius: 5px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .price-card h3 { color: #2c3e50; }
        .price { font-size: 2em; color: #3498db; margin: 10px 0; }
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
        
        <div class="pricing">
            <div class="price-card">
                <h3>Free Tier</h3>
                <div class="price">$0/mo</div>
                <ul style="text-align: left;">
                    <li>5 monitors</li>
                    <li>5-minute checks</li>
                    <li>Basic email alerts</li>
                    <li>24-hour history</li>
                </ul>
                <a href="#" class="cta">Start Free</a>
            </div>
            <div class="price-card">
                <h3>Pro</h3>
                <div class="price">$19/mo</div>
                <ul style="text-align: left;">
                    <li>50 monitors</li>
                    <li>1-minute checks</li>
                    <li>Email & webhook alerts</li>
                    <li>30-day history</li>
                    <li>Status pages</li>
                </ul>
                <a href="#" class="cta">Start Pro Trial</a>
            </div>
            <div class="price-card">
                <h3>Business</h3>
                <div class="price">$49/mo</div>
                <ul style="text-align: left;">
                    <li>Unlimited monitors</li>
                    <li>30-second checks</li>
                    <li>SMS & phone alerts</li>
                    <li>1-year history</li>
                    <li>API access</li>
                    <li>Custom integrations</li>
                </ul>
                <a href="#" class="cta">Contact Sales</a>
            </div>
        </div>
        
        <div style="text-align: center; margin: 40px 0;">
            <h2>Why Choose API Monitor?</h2>
            <p>✓ Simple setup - Add your API endpoint and we'll start monitoring immediately</p>
            <p>✓ Instant alerts - Get notified within seconds when your API goes down</p>
            <p>✓ Detailed analytics - Track response times and uptime percentages</p>
            <p>✓ No credit card required for free tier</p>
        </div>
    </div>
    
    <script>
        function loadMonitors() {
            fetch('/api/monitors')
                .then(response => response.json())
                .then(data => {
                    const container = document.getElementById('monitors');
                    container.innerHTML = '';
                    
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
    # Read the latest report
    try:
        with open('/home/daytona/data/monitor_report.json', 'r') as f:
            report = json.load(f)
        return jsonify(report)
    except:
        return jsonify({'monitors': []})

if __name__ == '__main__':
    print("Starting web dashboard on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
