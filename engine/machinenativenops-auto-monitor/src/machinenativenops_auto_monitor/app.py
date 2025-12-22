"""
Auto-Monitor Application Core
自動監控應用核心

Main application logic for the MachineNativeOps auto-monitoring system.
"""

import logging
import asyncio
from typing import Dict, Optional
from datetime import datetime

from .config import MonitorConfig
from .collectors import MetricsCollector, LogCollector, EventCollector
from .alerts import AlertManager, create_default_rules
from .儲存 import StorageBackend, InMemoryStorage

logger = logging.getLogger(__name__)


class AutoMonitorApp:
    """Main auto-monitor application."""
    
    def __init__(self, config: MonitorConfig):
        self.config = config
        self.running = False
        
        # Initialize components
        self.metrics_collector = MetricsCollector(
            interval=config.collection_interval
        )
        self.log_collector = LogCollector()
        self.event_collector = EventCollector()
        
        self.alert_manager = AlertManager()
        self.storage: StorageBackend = InMemoryStorage()
        
        # Setup default alert rules
        for rule in create_default_rules():
            self.alert_manager.add_rule(rule)
        
        # Register alert handler
        self.alert_manager.add_handler(self._handle_alert)
        
        logger.info("✅ AutoMonitorApp initialized")
    
    def _handle_alert(self, alert):
        """Handle fired alerts."""
        # Store alert
        self.storage.store_alert(alert)
        
        # Log alert
        logger.warning(f"🚨 {alert.severity.value.upper()}: {alert.message}")
        
        # Additional handling (webhooks, notifications, etc.) can be added here
    
    async def collect_metrics(self):
        """Continuously collect metrics."""
        while self.running:
            try:
                metrics = self.metrics_collector.collect()
                
                # Store metrics
                self.storage.store_metrics(metrics)
                
                # Evaluate alert rules
                self.alert_manager.evaluate_rules(metrics)
                
                # Log metrics in development mode
                if self.config.mode == 'development':
                    logger.debug(f"📊 Metrics: {metrics}")
                
                await asyncio.sleep(self.config.collection_interval)
                
            except Exception as e:
                logger.error(f"Error collecting metrics: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def collect_logs(self):
        """Continuously collect logs."""
        while self.running:
            try:
                logs = self.log_collector.collect()
                
                if logs:
                    self.storage.store_logs(logs)
                
                await asyncio.sleep(self.config.log_collection_interval)
                
            except Exception as e:
                logger.error(f"Error collecting logs: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def collect_events(self):
        """Continuously collect events."""
        while self.running:
            try:
                events = self.event_collector.collect()
                
                if events:
                    self.storage.store_events(events)
                
                await asyncio.sleep(self.config.event_collection_interval)
                
            except Exception as e:
                logger.error(f"Error collecting events: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def run_async(self):
        """Run the application asynchronously."""
        self.running = True
        
        logger.info("🚀 Starting auto-monitor collectors...")
        
        # Create tasks for all collectors
        tasks = [
            asyncio.create_task(self.collect_metrics()),
            asyncio.create_task(self.collect_logs()),
            asyncio.create_task(self.collect_events()),
        ]
        
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            logger.info("⏹️  Shutting down collectors...")
            self.running = False
    
    def run(self):
        """Run the application (blocking)."""
        try:
            asyncio.run(self.run_async())
        except KeyboardInterrupt:
            logger.info("\n⏹️  Received shutdown signal")
            self.running = False
    
    def get_status(self) -> Dict:
        """Get application status."""
        return {
            'running': self.running,
            'mode': self.config.mode,
            'uptime': 'N/A',  # TODO: Track uptime
            'active_alerts': len(self.alert_manager.get_active_alerts()),
            'metrics_collected': self.storage.get_metrics_count(),
            'logs_collected': self.storage.get_logs_count(),
            'events_collected': self.storage.get_events_count(),
        }
