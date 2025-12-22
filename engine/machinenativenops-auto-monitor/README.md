# MachineNativeOps Auto-Monitor

機器原生運維自動監控系統 (MachineNativeOps Auto-Monitor System)

## 📋 概述 (Overview)

The MachineNativeOps Auto-Monitor is an automated monitoring solution designed for machine-native operations infrastructure. It provides real-time metrics collection, log aggregation, event tracking, and intelligent alerting.

MachineNativeOps 自動監控是為機器原生運維基礎設施設計的自動監控解決方案。它提供實時指標收集、日誌聚合、事件追蹤和智能警報功能。

## 🎯 Features (特性)

- **📊 Metrics Collection**: System and application metrics collection
- **📝 Log Aggregation**: Centralized log collection and storage
- **🔔 Alert Management**: Intelligent alerting based on customizable rules
- **📈 Event Tracking**: System event detection and recording
- **💾 Flexible Storage**: Multiple storage backends (memory, file, database)
- **🚀 Async Operations**: Efficient async data collection

## 🚀 Quick Start (快速開始)

### Installation (安裝)

```bash
# Install dependencies
pip install -r requirements.txt

# Or install with optional features
pip install -r requirements.txt -r requirements-optional.txt
```

### Basic Usage (基本使用)

```bash
# Start with default configuration
python -m machinenativenops_auto_monitor

# Start with custom config
python -m machinenativenops_auto_monitor --config config.yaml

# Start in production mode
python -m machinenativenops_auto_monitor --mode production
```

### Configuration (配置)

Create a `config.yaml` file:

```yaml
# Application settings
mode: production
port: 8080
host: 0.0.0.0

# Collection intervals (seconds)
collection_interval: 10
log_collection_interval: 5
event_collection_interval: 15

# Storage settings
storage_backend: file
storage_path: /var/lib/machinenativeops/monitor
retention_days: 7

# Alert settings
enable_alerts: true
alert_channels:
  - type: webhook
    url: https://alerts.example.com/webhook

# Namespace configuration
namespace: machinenativeops
registry: registry.machinenativeops.io
certificate_path: etc/machinenativeops/pkl
cluster_token: super-agent-etcd-cluster
```

## 📁 Project Structure (項目結構)

```
machinenativenops-auto-monitor/
├── src/
│   └── machinenativenops_auto_monitor/
│       ├── __init__.py          # Package initialization
│       ├── __main__.py          # CLI entry point
│       ├── app.py               # Main application logic
│       ├── alerts.py            # Alert management
│       ├── collectors.py        # Data collectors
│       ├── config.py            # Configuration management
│       └── 儲存.py              # Storage backends
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## 🔧 Architecture (架構)

### Components (組件)

1. **MetricsCollector** (指標收集器)
   - Collects system metrics (CPU, memory, disk, network)
   - Supports process-level metrics
   - Extensible for custom metrics

2. **LogCollector** (日誌收集器)
   - Aggregates logs from multiple sources
   - Supports structured logging
   - Buffered collection for efficiency

3. **EventCollector** (事件收集器)
   - Detects and records system events
   - Auto-detection of anomalies
   - Custom event support

4. **AlertManager** (警報管理器)
   - Rule-based alerting
   - Multiple severity levels
   - Alert routing and handling

5. **StorageBackend** (儲存後端)
   - In-memory storage for development
   - File-based storage for production
   - Database support (optional)

### Data Flow (數據流)

```
Collectors → Storage Backend → Alert Manager → Handlers
    ↓             ↓                 ↓             ↓
 Metrics        Logs             Alerts      Notifications
 Events     Persistence         Rules       Actions
```

## 📊 Metrics Collected (收集的指標)

- **System Metrics** (系統指標)
  - CPU usage percentage
  - Memory usage and availability
  - Disk usage and space
  - Network I/O statistics
  - Process count

- **Process Metrics** (進程指標)
  - Per-process CPU usage
  - Per-process memory usage
  - Thread count
  - Process status

## 🔔 Default Alert Rules (默認警報規則)

1. **high_cpu_usage**: Triggers when CPU > 80%
2. **high_memory_usage**: Triggers when memory > 85%
3. **disk_space_low**: Triggers when disk > 90%
4. **service_down**: Triggers when service health check fails

## 🛠️ Development (開發)

### Adding Custom Collectors (添加自定義收集器)

```python
from machinenativenops_auto_monitor.collectors import MetricsCollector

class CustomCollector(MetricsCollector):
    def collect(self):
        metrics = super().collect()
        metrics['custom_metric'] = self.get_custom_value()
        return metrics
```

### Adding Custom Alert Rules (添加自定義警報規則)

```python
from machinenativenops_auto_monitor.alerts import AlertRule, AlertSeverity

rule = AlertRule(
    name="custom_rule",
    condition=lambda m: m.get('custom_metric', 0) > 100,
    severity=AlertSeverity.WARNING,
    message_template="Custom metric exceeded: {custom_metric}",
)

alert_manager.add_rule(rule)
```

## 🧪 Testing (測試)

```bash
# Run in development mode with verbose logging
python -m machinenativenops_auto_monitor --mode development --verbose

# Check metrics collection
curl http://localhost:8080/metrics

# Check active alerts
curl http://localhost:8080/alerts
```

## 📝 License (許可證)

Copyright © 2024 MachineNativeOps

## 🤝 Contributing (貢獻)

Contributions are welcome! Please follow the MachineNativeOps contribution guidelines.

## 📞 Support (支持)

For issues and questions, please refer to the MachineNativeOps documentation or open an issue in the main repository.

---

**Namespace Alignment (命名空間對齊)**

This module follows MachineNativeOps namespace standards:
- Domain: `machinenativeops.io`
- Namespace: `machinenativeops`
- Registry: `registry.machinenativeops.io`
- Certificate Path: `etc/machinenativeops/pkl`
- Cluster Token: `super-agent-etcd-cluster`
