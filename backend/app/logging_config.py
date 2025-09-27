"""
Logging Configuration Module for MyBrand Job Application Platform
Version: v2
Purpose: Centralized logging configuration with structured logging and monitoring
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for logging configuration
# ============================================================================

import logging
import logging.config
import json
import os
from typing import Dict, Any, Optional

# ============================================================================
# LOGGING CONFIGURATION
# Centralized logging configuration for the entire application
# ============================================================================

def setup_logging(log_level: str = "INFO", log_file: str = "app.log") -> None:
    """
    Set up comprehensive logging configuration for the application.
    
    This function configures logging with multiple handlers including console,
    file, and structured JSON logging for better monitoring and debugging.
    
    Args:
        log_level (str): The logging level (default: "INFO")
        log_file (str): The log file path (default: "app.log")
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Define logging configuration
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            },
            "detailed": {
                "format": "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s"
            },
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(asctime)s %(name)s %(levelname)s %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "standard",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": log_level,
                "formatter": "detailed",
                "filename": log_file,
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5
            },
            "json_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": log_level,
                "formatter": "json",
                "filename": f"{log_file}.json",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5
            }
        },
        "loggers": {
            "": {  # root logger
                "handlers": ["console", "file", "json_file"],
                "level": log_level,
                "propagate": False
            },
            "uvicorn": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False
            },
            "uvicorn.error": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False
            },
            "uvicorn.access": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False
            }
        }
    }
    
    # Apply the logging configuration
    logging.config.dictConfig(logging_config)

# ============================================================================
# STRUCTURED LOGGING UTILITY
# Helper functions for structured logging with context
# ============================================================================

class StructuredLogger:
    """
    A wrapper around the standard logger that provides structured logging capabilities.
    
    This class adds context to log messages and supports structured data logging
    for better monitoring and debugging.
    """
    
    def __init__(self, name: str):
        """Initialize the structured logger with a specific name."""
        self.logger = logging.getLogger(name)
    
    def _log_with_context(self, level: int, message: str, context: Optional[Dict[str, Any]] = None, **kwargs) -> None:
        """
        Log a message with structured context.
        
        Args:
            level (int): The logging level
            message (str): The log message
            context (Dict[str, Any]): Additional context data
            **kwargs: Additional keyword arguments to include in the log
        """
        # Combine context and kwargs
        log_data = {}
        if context:
            log_data.update(context)
        log_data.update(kwargs)
        
        # If we have structured data, include it in the message
        if log_data:
            full_message = f"{message} | Context: {json.dumps(log_data, default=str)}"
            self.logger.log(level, full_message)
        else:
            self.logger.log(level, message)
    
    def debug(self, message: str, context: Optional[Dict[str, Any]] = None, **kwargs) -> None:
        """Log a debug message with context."""
        self._log_with_context(logging.DEBUG, message, context or {}, **kwargs)
    
    def info(self, message: str, context: Optional[Dict[str, Any]] = None, **kwargs) -> None:
        """Log an info message with context."""
        self._log_with_context(logging.INFO, message, context or {}, **kwargs)
    
    def warning(self, message: str, context: Optional[Dict[str, Any]] = None, **kwargs) -> None:
        """Log a warning message with context."""
        self._log_with_context(logging.WARNING, message, context or {}, **kwargs)
    
    def error(self, message: str, context: Optional[Dict[str, Any]] = None, **kwargs) -> None:
        """Log an error message with context."""
        self._log_with_context(logging.ERROR, message, context or {}, **kwargs)
    
    def critical(self, message: str, context: Optional[Dict[str, Any]] = None, **kwargs) -> None:
        """Log a critical message with context."""
        self._log_with_context(logging.CRITICAL, message, context or {}, **kwargs)

# ============================================================================
# MONITORING INTEGRATION
# Integration with monitoring and observability tools
# ============================================================================

class MetricsCollector:
    """
    A simple metrics collector for application monitoring.
    
    This class provides basic metrics collection capabilities that can be
    extended to integrate with monitoring systems like Prometheus.
    """
    
    def __init__(self):
        """Initialize the metrics collector."""
        self.counters = {}
        self.timers = {}
    
    def increment_counter(self, name: str, value: int = 1, labels: Optional[Dict[str, str]] = None) -> None:
        """
        Increment a counter metric.
        
        Args:
            name (str): The name of the counter
            value (int): The value to increment by (default: 1)
            labels (Dict[str, str]): Optional labels for the metric
        """
        counter_key = f"{name}_{labels}" if labels else name
        if counter_key not in self.counters:
            self.counters[counter_key] = 0
        self.counters[counter_key] += value
        
        # Log the counter increment
        logger = StructuredLogger("metrics")
        logger.info("Counter incremented: {name}".format(name=name), 
                   value=value, 
                   total=self.counters[counter_key],
                   labels=labels or {})

    def start_timer(self, name: str) -> str:
        """
        Start a timer for measuring duration.
        
        Args:
            name (str): The name of the timer
            
        Returns:
            str: A unique timer ID
        """
        import uuid
        import time
        
        timer_id = str(uuid.uuid4())
        self.timers[timer_id] = {
            "name": name,
            "start_time": time.time()
        }
        return timer_id
    
    def stop_timer(self, timer_id: str) -> float:
        """
        Stop a timer and return the elapsed time.
        
        Args:
            timer_id (str): The timer ID returned by start_timer
            
        Returns:
            float: The elapsed time in seconds
            
        Raises:
            KeyError: If the timer ID is not found
        """
        import time
        
        if timer_id not in self.timers:
            raise KeyError(f"Timer {timer_id} not found")
        
        timer_data = self.timers.pop(timer_id)
        elapsed_time = time.time() - timer_data["start_time"]
        
        # Log the timing
        logger = StructuredLogger("metrics")
        logger.info(f"Timer stopped: {timer_data['name']}", 
                   duration_seconds=elapsed_time)
        
        return elapsed_time

# ============================================================================
# GLOBAL INSTANCES
# Global instances for application-wide use
# ============================================================================

# Create a global metrics collector instance
metrics_collector = MetricsCollector()

# ============================================================================
# UTILITY FUNCTIONS
# Helper functions for common logging patterns
# ============================================================================

def log_api_request(method: str, path: str, status_code: int, duration: float, user_id: Optional[str] = None) -> None:
    """
    Log an API request with structured data.
    
    Args:
        method (str): HTTP method
        path (str): Request path
        status_code (int): HTTP status code
        duration (float): Request duration in seconds
        user_id (str): Optional user ID
    """
    logger = StructuredLogger("api")
    logger.info("API request completed",
                method=method,
                path=path,
                status_code=status_code,
                duration_seconds=duration,
                user_id=user_id or "")

def log_error_with_context(error: Exception, context: Optional[Dict[str, Any]] = None) -> None:
    """
    Log an error with structured context.
    
    Args:
        error (Exception): The exception to log
        context (Dict[str, Any]): Additional context data
    """
    logger = StructuredLogger("error")
    error_context = {
        "error_type": type(error).__name__,
        "error_message": str(error)
    }
    if context:
        error_context.update(context)
    
    logger.error("Application error occurred", context=error_context)