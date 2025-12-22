"""
Data Collectors Module
數據收集模組

Collects metrics, logs, and events from various sources for monitoring.
"""

import logging
import psutil
import platform
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class MetricData:
    """Represents a metric data point."""
    name: str
    value: float
    timestamp: datetime
    labels: Dict[str, str]
    
    def to_dict(self) -> Dict:
        return {
            **asdict(self),
            'timestamp': self.timestamp.isoformat(),
        }


@dataclass
class LogEntry:
    """Represents a log entry."""
    level: str
    message: str
    timestamp: datetime
    source: str
    metadata: Dict
    
    def to_dict(self) -> Dict:
        return {
            **asdict(self),
            'timestamp': self.timestamp.isoformat(),
        }


@dataclass
class Event:
    """Represents a system event."""
    type: str
    description: str
    timestamp: datetime
    severity: str
    metadata: Dict
    
    def to_dict(self) -> Dict:
        return {
            **asdict(self),
            'timestamp': self.timestamp.isoformat(),
        }


class MetricsCollector:
    """Collects system and application metrics."""
    
    def __init__(self, interval: int = 10):
        self.interval = interval
        self.last_collection = None
    
    def collect(self) -> Dict:
        """Collect current metrics."""
        try:
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': psutil.cpu_percent(interval=1),
                'cpu_count': psutil.cpu_count(),
                'memory_percent': psutil.virtual_memory().percent,
                'memory_available_gb': psutil.virtual_memory().available / (1024**3),
                'memory_total_gb': psutil.virtual_memory().total / (1024**3),
                'disk_percent': psutil.disk_usage('/').percent,
                'disk_free_gb': psutil.disk_usage('/').free / (1024**3),
                'disk_total_gb': psutil.disk_usage('/').total / (1024**3),
                'network_sent_mb': psutil.net_io_counters().bytes_sent / (1024**2),
                'network_recv_mb': psutil.net_io_counters().bytes_recv / (1024**2),
                'process_count': len(psutil.pids()),
                'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat(),
            }
            
            self.last_collection = datetime.now()
            return metrics
            
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
            return {}
    
    def collect_process_metrics(self, pid: Optional[int] = None) -> Dict:
        """Collect metrics for a specific process."""
        try:
            process = psutil.Process(pid) if pid else psutil.Process()
            
            return {
                'pid': process.pid,
                'name': process.name(),
                'cpu_percent': process.cpu_percent(interval=0.1),
                'memory_percent': process.memory_percent(),
                'memory_mb': process.memory_info().rss / (1024**2),
                'num_threads': process.num_threads(),
                'status': process.status(),
                'create_time': datetime.fromtimestamp(process.create_time()).isoformat(),
            }
        except Exception as e:
            logger.error(f"Error collecting process metrics: {e}")
            return {}


class LogCollector:
    """Collects logs from various sources."""
    
    def __init__(self):
        self.log_buffer: List[LogEntry] = []
    
    def collect(self) -> List[LogEntry]:
        """Collect recent logs."""
        # In a real implementation, this would collect from log files,
        # syslog, or other log sources
        logs = self.log_buffer.copy()
        self.log_buffer.clear()
        return logs
    
    def add_log(self, level: str, message: str, source: str, metadata: Dict = None):
        """Add a log entry to the buffer."""
        entry = LogEntry(
            level=level,
            message=message,
            timestamp=datetime.now(),
            source=source,
            metadata=metadata or {},
        )
        self.log_buffer.append(entry)


class EventCollector:
    """Collects system events."""
    
    def __init__(self):
        self.event_buffer: List[Event] = []
        self._last_check = datetime.now()
    
    def collect(self) -> List[Event]:
        """Collect recent events."""
        events = self.event_buffer.copy()
        self.event_buffer.clear()
        
        # Auto-detect system events
        self._detect_system_events()
        
        return events
    
    def _detect_system_events(self):
        """Detect and record system events."""
        # Check for high resource usage
        cpu_usage = psutil.cpu_percent(interval=0.1)
        if cpu_usage > 90:
            self.add_event(
                type='high_cpu',
                description=f'High CPU usage detected: {cpu_usage}%',
                severity='warning'
            )
        
        memory_usage = psutil.virtual_memory().percent
        if memory_usage > 90:
            self.add_event(
                type='high_memory',
                description=f'High memory usage detected: {memory_usage}%',
                severity='warning'
            )
    
    def add_event(self, type: str, description: str, severity: str, metadata: Dict = None):
        """Add an event to the buffer."""
        event = Event(
            type=type,
            description=description,
            timestamp=datetime.now(),
            severity=severity,
            metadata=metadata or {},
        )
        self.event_buffer.append(event)


class KubernetesCollector:
    """Collects metrics from Kubernetes clusters."""
    
    def __init__(self):
        self.enabled = False
        # In a real implementation, initialize k8s client here
    
    def collect_pod_metrics(self) -> List[Dict]:
        """Collect metrics from all pods."""
        # Placeholder for Kubernetes integration
        return []
    
    def collect_node_metrics(self) -> List[Dict]:
        """Collect metrics from all nodes."""
        # Placeholder for Kubernetes integration
        return []
