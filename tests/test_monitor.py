import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.monitor import APIMonitor

def test_monitor_creation():
    """Test that we can create a monitor instance"""
    monitor = APIMonitor(':memory:')  # Use in-memory database for testing
    assert monitor is not None

def test_add_monitor():
    """Test adding a new monitor"""
    monitor = APIMonitor(':memory:')
    monitor_id = monitor.add_monitor(
        name="Test API",
        url="https://api.example.com",
        check_interval=300
    )
    assert monitor_id > 0

def test_monitor_stats():
    """Test getting monitor statistics"""
    monitor = APIMonitor(':memory:')
    monitor_id = monitor.add_monitor(
        name="Test API",
        url="https://api.example.com"
    )
    stats = monitor.get_monitor_stats(monitor_id)
    assert stats['total_checks'] == 0
    assert stats['uptime_percentage'] == 0
