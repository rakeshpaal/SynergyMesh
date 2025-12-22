#!/usr/bin/env python3
"""
MachineNativeOps Auto-Monitor CLI Entry Point
機器原生運維自動監控 CLI 入口

Usage:
    python -m machinenativenops_auto_monitor [options]
    python -m machinenativenops_auto_monitor --config config.yaml
    python -m machinenativenops_auto_monitor --mode production
"""

import sys
import argparse
import logging
from pathlib import Path

from .app import AutoMonitorApp
from .config import MonitorConfig

def setup_logging(verbose: bool = False):
    """Configure logging for the application."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('auto-monitor.log')
        ]
    )

def main():
    """Main entry point for the auto-monitor application."""
    parser = argparse.ArgumentParser(
        description='MachineNativeOps Auto-Monitor - 自動監控系統',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start with default configuration
  python -m machinenativenops_auto_monitor
  
  # Start with custom config file
  python -m machinenativenops_auto_monitor --config /path/to/config.yaml
  
  # Start in production mode with verbose logging
  python -m machinenativenops_auto_monitor --mode production --verbose
        """
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file (YAML)'
    )
    parser.add_argument(
        '--mode',
        choices=['development', 'production'],
        default='development',
        help='Running mode (default: development)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8080,
        help='Port to run the monitoring server (default: 8080)'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    try:
        # Load configuration
        if args.config:
            config_path = Path(args.config)
            if not config_path.exists():
                logger.error(f"Config file not found: {config_path}")
                sys.exit(1)
            config = MonitorConfig.from_file(config_path)
        else:
            config = MonitorConfig.default()
        
        # Override with CLI arguments
        config.mode = args.mode
        config.port = args.port
        
        logger.info(f"🚀 Starting MachineNativeOps Auto-Monitor")
        logger.info(f"📊 Mode: {config.mode}")
        logger.info(f"🔌 Port: {config.port}")
        
        # Create and run the application
        app = AutoMonitorApp(config)
        app.run()
        
    except KeyboardInterrupt:
        logger.info("\n⏹️  Shutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
