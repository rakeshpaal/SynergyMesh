"""
MachineNativeOps Auto-Monitor Package
機器原生運維自動監控套件

This package provides automated monitoring capabilities for MachineNativeOps infrastructure.
"""

__version__ = "1.0.0"
__author__ = "MachineNativeOps"

from .app import AutoMonitorApp
from .collectors import MetricsCollector, LogCollector, EventCollector
from .alerts import AlertManager, AlertRule
from .config import MonitorConfig

__all__ = [
    'AutoMonitorApp',
    'MetricsCollector',
    'LogCollector',
    'EventCollector',
    'AlertManager',
    'AlertRule',
    'MonitorConfig',
]
