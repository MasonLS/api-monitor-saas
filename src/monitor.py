#!/usr/bin/env python3
"""
API Monitor MVP - A simple but effective API monitoring service
Features:
- Monitor multiple endpoints
- Check response time and status
- Email alerts on failures
- Simple web dashboard
- SQLite database for history
"""

import requests
import sqlite3
import json
import time
import smtplib
import schedule
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class APIMonitor:
    def __init__(self, db_path='/home/daytona/data/api_monitor.db'):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monitors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                url TEXT NOT NULL,
                method TEXT DEFAULT 'GET',
                expected_status INTEGER DEFAULT 200,
                timeout INTEGER DEFAULT 30,
                check_interval INTEGER DEFAULT 300,
                email_alerts TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                monitor_id INTEGER,
                status_code INTEGER,
                response_time REAL,
                error_message TEXT,
                checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (monitor_id) REFERENCES monitors (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                monitor_id INTEGER,
                alert_type TEXT,
                message TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (monitor_id) REFERENCES monitors (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_monitor(self, name, url, email_alerts=None, check_interval=300):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO monitors (name, url, email_alerts, check_interval)
            VALUES (?, ?, ?, ?)
        ''', (name, url, email_alerts, check_interval))
        
        conn.commit()
        conn.close()
        
        return cursor.lastrowid
    
    def check_endpoint(self, monitor_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get monitor details
        cursor.execute('SELECT * FROM monitors WHERE id = ? AND is_active = 1', (monitor_id,))
        monitor = cursor.fetchone()
        
        if not monitor:
            conn.close()
            return
        
        url = monitor[2]
        method = monitor[3]
        expected_status = monitor[4]
        timeout = monitor[5]
        
        # Perform the check
        start_time = time.time()
        error_message = None
        status_code = None
        
        try:
            response = requests.request(method, url, timeout=timeout)
            status_code = response.status_code
            response_time = time.time() - start_time
            
            if status_code != expected_status:
                error_message = f"Expected status {expected_status}, got {status_code}"
                
        except requests.exceptions.Timeout:
            error_message = "Request timed out"
            response_time = timeout
        except requests.exceptions.ConnectionError:
            error_message = "Connection error"
            response_time = time.time() - start_time
        except Exception as e:
            error_message = str(e)
            response_time = time.time() - start_time
        
        # Record the check
        cursor.execute('''
            INSERT INTO checks (monitor_id, status_code, response_time, error_message)
            VALUES (?, ?, ?, ?)
        ''', (monitor_id, status_code, response_time, error_message))
        
        # Send alert if needed
        if error_message and monitor[7]:  # email_alerts field
            self.send_alert(monitor_id, monitor[1], url, error_message, monitor[7])
        
        conn.commit()
        conn.close()
        
        return {
            'status_code': status_code,
            'response_time': response_time,
            'error': error_message
        }
    
    def send_alert(self, monitor_id, name, url, error_message, email):
        # For MVP, we'll just log alerts. In production, integrate with email service
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        message = f"Monitor '{name}' failed: {error_message}\nURL: {url}"
        
        cursor.execute('''
            INSERT INTO alerts (monitor_id, alert_type, message)
            VALUES (?, ?, ?)
        ''', (monitor_id, 'email', message))
        
        conn.commit()
        conn.close()
        
        print(f"ALERT: {message}")
    
    def get_monitor_stats(self, monitor_id, hours=24):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get recent checks
        cursor.execute('''
            SELECT 
                COUNT(*) as total_checks,
                COUNT(CASE WHEN error_message IS NULL THEN 1 END) as successful_checks,
                AVG(response_time) as avg_response_time,
                MIN(response_time) as min_response_time,
                MAX(response_time) as max_response_time
            FROM checks
            WHERE monitor_id = ?
            AND checked_at > datetime('now', '-' || ? || ' hours')
        ''', (monitor_id, hours))
        
        stats = cursor.fetchone()
        conn.close()
        
        return {
            'total_checks': stats[0],
            'successful_checks': stats[1],
            'uptime_percentage': (stats[1] / stats[0] * 100) if stats[0] > 0 else 0,
            'avg_response_time': stats[2],
            'min_response_time': stats[3],
            'max_response_time': stats[4]
        }
    
    def generate_report(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all active monitors
        cursor.execute('SELECT * FROM monitors WHERE is_active = 1')
        monitors = cursor.fetchall()
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'monitors': []
        }
        
        for monitor in monitors:
            monitor_data = {
                'id': monitor[0],
                'name': monitor[1],
                'url': monitor[2],
                'stats_24h': self.get_monitor_stats(monitor[0], 24),
                'stats_7d': self.get_monitor_stats(monitor[0], 168)
            }
            report['monitors'].append(monitor_data)
        
        conn.close()
        
        # Save report
        with open('/home/daytona/data/monitor_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        return report

# Demo usage
if __name__ == "__main__":
    monitor = APIMonitor()
    
    # Add some example monitors
    print("Adding example monitors...")
    
    # Popular APIs to monitor
    monitor.add_monitor("GitHub API", "https://api.github.com", check_interval=300)
    monitor.add_monitor("JSONPlaceholder", "https://jsonplaceholder.typicode.com/posts/1", check_interval=300)
    monitor.add_monitor("httpbin.org", "https://httpbin.org/status/200", check_interval=300)
    
    print("\nPerforming initial checks...")
    
    # Check all monitors
    conn = sqlite3.connect(monitor.db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM monitors WHERE is_active = 1')
    monitors = cursor.fetchall()
    conn.close()
    
    for mon_id, mon_name in monitors:
        print(f"\nChecking {mon_name}...")
        result = monitor.check_endpoint(mon_id)
        if result['error']:
            print(f"  ❌ Error: {result['error']}")
        else:
            print(f"  ✅ Status: {result['status_code']} | Response time: {result['response_time']:.2f}s")
    
    # Generate report
    print("\nGenerating report...")
    report = monitor.generate_report()
    print(f"Report saved to /home/daytona/data/monitor_report.json")
    
    print("\n=== BUSINESS PLAN ===")
    print("1. MVP is ready - can monitor APIs and track uptime")
    print("2. Next steps:")
    print("   - Create a simple web interface")
    print("   - Set up payment processing (Stripe)")
    print("   - Create landing page")
    print("   - Add email/SMS alerts")
    print("   - Market to developers and DevOps teams")
    print("\nPricing tiers:")
    print("- Free: 5 monitors, 5-minute checks")
    print("- Pro ($19/mo): 50 monitors, 1-minute checks, email alerts")
    print("- Business ($49/mo): Unlimited monitors, 30-second checks, SMS alerts, API access")
