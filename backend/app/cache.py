"""
Caching Module for MyBrand Job Application Platform
Version: v2
Purpose: Implements caching strategies for performance optimization
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for caching functionality
# ============================================================================

import redis
import json
import hashlib
import logging
from typing import Any, Optional, Dict, List
from functools import wraps
import asyncio
from datetime import datetime, timedelta

# Local imports
from .logging_config import StructuredLogger
from .config import redis_settings

# Create a structured logger for this module
logger = StructuredLogger(__name__)

# ============================================================================
# REDIS CLIENT SETUP
# Initialize Redis client for caching
# ============================================================================

class RedisClient:
    """Redis client wrapper with connection management."""
    
    def __init__(self):
        """Initialize the Redis client."""
        self.client = None
        self.connected = False
    
    def connect(self) -> bool:
        """
        Connect to Redis server.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.client = redis.Redis.from_url(redis_settings.url)
            # Test the connection
            self.client.ping()
            self.connected = True
            logger.info("Connected to Redis successfully")
            return True
        except Exception as e:
            logger.error("Failed to connect to Redis", error=str(e))
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnect from Redis server."""
        if self.client:
            self.client.close()
            self.connected = False
            logger.info("Disconnected from Redis")
    
    def is_connected(self) -> bool:
        """
        Check if Redis client is connected.
        
        Returns:
            bool: True if connected, False otherwise
        """
        if not self.connected or not self.client:
            return False
        
        try:
            self.client.ping()
            return True
        except:
            self.connected = False
            return False

# Global Redis client instance
redis_client = RedisClient()

# ============================================================================
# CACHE KEY GENERATION
# Functions for generating consistent cache keys
# ============================================================================

def generate_cache_key(prefix: str, *args, **kwargs) -> str:
    """
    Generate a cache key from function arguments.
    
    Args:
        prefix (str): Key prefix
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        str: Generated cache key
    """
    # Create a string representation of all arguments
    args_str = str(args)
    kwargs_str = str(sorted(kwargs.items()))
    combined = f"{prefix}:{args_str}:{kwargs_str}"
    
    # Generate a hash to ensure consistent key length
    key_hash = hashlib.md5(combined.encode()).hexdigest()
    
    return f"{prefix}:{key_hash}"

# ============================================================================
# CACHING DECORATORS
# Decorators for adding caching to functions
# ============================================================================

def cache_result(expiration: int = 300, key_prefix: str = "cache"):
    """
    Decorator to cache function results.
    
    Args:
        expiration (int): Cache expiration time in seconds (default: 300 seconds/5 minutes)
        key_prefix (str): Cache key prefix (default: "cache")
        
    Returns:
        The decorated function
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = generate_cache_key(f"{key_prefix}:{func.__name__}", *args, **kwargs)
            
            # Try to get from cache first
            if redis_client.is_connected() and redis_client.client is not None:
                try:
                    cached_result = redis_client.client.get(cache_key)
                    # Handle async response properly
                    if asyncio.iscoroutine(cached_result):
                        cached_result = await cached_result
                    
                    # Check if we have a valid result
                    if cached_result is not None:
                        logger.debug("Cache hit", key=cache_key)
                        # Safely decode and parse JSON
                        cached_result = _safe_decode(cached_result)
                        cached_result = _safe_json_loads(cached_result)
                        if cached_result is not None and not asyncio.iscoroutine(cached_result):
                            return cached_result
                except Exception as e:
                    logger.warning("Failed to get from cache", error=str(e))
            
            # Execute function and cache result
            try:
                result = await func(*args, **kwargs)
                
                # Cache the result
                if redis_client.is_connected() and redis_client.client is not None:
                    try:
                        set_result = redis_client.client.setex(
                            cache_key,
                            expiration,
                            json.dumps(result, default=str)
                        )
                        # Handle async response if needed
                        if asyncio.iscoroutine(set_result):
                            await set_result
                        logger.debug("Result cached", key=cache_key, expiration=expiration)
                    except Exception as e:
                        logger.warning("Failed to cache result", error=str(e))
                
                return result
            except Exception as e:
                logger.error("Function execution failed", function=func.__name__, error=str(e))
                raise
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = generate_cache_key(f"{key_prefix}:{func.__name__}", *args, **kwargs)
            
            # Try to get from cache first
            if redis_client.is_connected() and redis_client.client is not None:
                try:
                    cached_result = redis_client.client.get(cache_key)
                    # Check if we have a valid result
                    if cached_result is not None:
                        logger.debug("Cache hit", key=cache_key)
                        # Safely decode and parse JSON
                        cached_result = _safe_decode(cached_result)
                        cached_result = _safe_json_loads(cached_result)
                        if cached_result is not None:
                            return cached_result
                except Exception as e:
                    logger.warning("Failed to get from cache", error=str(e))
            
            # Execute function and cache result
            try:
                result = func(*args, **kwargs)
                
                # Cache the result
                if redis_client.is_connected() and redis_client.client is not None:
                    try:
                        redis_client.client.setex(
                            cache_key,
                            expiration,
                            json.dumps(result, default=str)
                        )
                        logger.debug("Result cached", key=cache_key, expiration=expiration)
                    except Exception as e:
                        logger.warning("Failed to cache result", error=str(e))
                
                return result
            except Exception as e:
                logger.error("Function execution failed", function=func.__name__, error=str(e))
                raise
        
        # Return appropriate wrapper based on function type
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    
    return decorator

def invalidate_cache(key_pattern: str):
    """
    Decorator to invalidate cache entries.
    
    Args:
        key_pattern (str): Pattern to match cache keys for invalidation
        
    Returns:
        The decorated function
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Execute function first
            result = await func(*args, **kwargs)
            
            # Invalidate cache entries
            if redis_client.is_connected() and redis_client.client is not None:
                try:
                    # Find and delete keys matching the pattern
                    keys_result = redis_client.client.keys(key_pattern)
                    # Handle async response properly
                    if asyncio.iscoroutine(keys_result):
                        keys = await keys_result
                    else:
                        keys = keys_result
                    
                    # Ensure keys is valid before using it
                    if keys is not None and _safe_iterable(keys):
                        try:
                            delete_result = _safe_delete_keys(redis_client.client, keys)
                            # Get count safely
                            count = _safe_len(keys)
                            logger.debug("Cache invalidated", pattern=key_pattern, count=count)
                        except Exception as e:
                            logger.warning("Failed to delete cache keys", error=str(e))
                except Exception as e:
                    logger.warning("Failed to invalidate cache", error=str(e))
            
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Execute function first
            result = func(*args, **kwargs)
            
            # Invalidate cache entries
            if redis_client.is_connected() and redis_client.client is not None:
                try:
                    # Find and delete keys matching the pattern
                    keys = redis_client.client.keys(key_pattern)
                    if keys is not None and _safe_iterable(keys):
                        try:
                            _safe_delete_keys(redis_client.client, keys)
                            # Get count safely
                            count = _safe_len(keys)
                            logger.debug("Cache invalidated", pattern=key_pattern, count=count)
                        except Exception as e:
                            logger.warning("Failed to delete cache keys", error=str(e))
                except Exception as e:
                    logger.warning("Failed to invalidate cache", error=str(e))
            
            return result
        
        # Return appropriate wrapper based on function type
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    
    return decorator

# ============================================================================
# CACHE MANAGEMENT
# Functions for managing cache entries
# ============================================================================

class CacheManager:
    """Cache management utilities."""
    
    @staticmethod
    def get(key: str) -> Optional[Any]:
        """
        Get a value from cache.
        
        Args:
            key (str): Cache key
            
        Returns:
            Optional[Any]: Cached value or None if not found
        """
        if not redis_client.is_connected() or redis_client.client is None:
            return None
        
        try:
            value = redis_client.client.get(key)
            # Handle async response if needed
            if asyncio.iscoroutine(value):
                value = asyncio.run(value)
            
            # Check if we have a valid result
            if value is not None:
                # Safely decode and parse JSON
                value = _safe_decode(value)
                value = _safe_json_loads(value)
                if value is not None and not asyncio.iscoroutine(value):
                    return value
            return None
        except Exception as e:
            logger.warning("Failed to get from cache", key=key, error=str(e))
            return None
    
    @staticmethod
    def set(key: str, value: Any, expiration: int = 300) -> bool:
        """
        Set a value in cache.
        
        Args:
            key (str): Cache key
            value (Any): Value to cache
            expiration (int): Expiration time in seconds (default: 300)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not redis_client.is_connected() or redis_client.client is None:
            return False
        
        try:
            redis_client.client.setex(key, expiration, json.dumps(value, default=str))
            return True
        except Exception as e:
            logger.warning("Failed to set cache", key=key, error=str(e))
            return False
    
    @staticmethod
    def delete(key: str) -> bool:
        """
        Delete a value from cache.
        
        Args:
            key (str): Cache key
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not redis_client.is_connected() or redis_client.client is None:
            return False
        
        try:
            result = redis_client.client.delete(key)
            # Handle async response if needed
            if asyncio.iscoroutine(result):
                result = asyncio.run(result)
            return _safe_int_bool(result)
        except Exception as e:
            logger.warning("Failed to delete from cache", key=key, error=str(e))
            return False
    
    @staticmethod
    def clear_pattern(pattern: str) -> int:
        """
        Clear cache entries matching a pattern.
        
        Args:
            pattern (str): Pattern to match cache keys
            
        Returns:
            int: Number of keys deleted
        """
        if not redis_client.is_connected() or redis_client.client is None:
            return 0
        
        try:
            keys_result = redis_client.client.keys(pattern)
            # Handle async response if needed
            if asyncio.iscoroutine(keys_result):
                keys = asyncio.run(keys_result)
            else:
                keys = keys_result
            
            if keys is not None and _safe_iterable(keys):
                try:
                    result = _safe_delete_keys(redis_client.client, keys)
                    # Get count safely
                    count = _safe_len(keys)
                    logger.info("Cache cleared", pattern=pattern, count=count)
                    return result
                except Exception as e:
                    logger.warning("Failed to delete cache keys", error=str(e))
            return 0
        except Exception as e:
            logger.warning("Failed to clear cache pattern", pattern=pattern, error=str(e))
            return 0
    
    @staticmethod
    def get_stats() -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dict[str, Any]: Cache statistics
        """
        if not redis_client.is_connected() or redis_client.client is None:
            return {"connected": False}
        
        try:
            info_result = redis_client.client.info()
            # Handle async response if needed
            if asyncio.iscoroutine(info_result):
                info = asyncio.run(info_result)
            else:
                info = info_result
            
            return {
                "connected": True,
                "used_memory": _safe_dict_get(info, "used_memory_human", "N/A"),
                "connected_clients": _safe_dict_get(info, "connected_clients", "N/A"),
                "total_commands_processed": _safe_dict_get(info, "total_commands_processed", "N/A"),
                "keyspace_hits": _safe_dict_get(info, "keyspace_hits", "N/A"),
                "keyspace_misses": _safe_dict_get(info, "keyspace_misses", "N/A")
            }
        except Exception as e:
            logger.warning("Failed to get cache stats", error=str(e))
            return {"connected": True, "error": str(e)}

# ============================================================================
# PERFORMANCE MONITORING
# Functions for monitoring performance and cache effectiveness
# ============================================================================

class PerformanceMonitor:
    """Performance monitoring utilities."""
    
    def __init__(self):
        """Initialize the performance monitor."""
        self.metrics = {
            "cache_hits": 0,
            "cache_misses": 0,
            "function_calls": 0,
            "average_response_time": 0.0
        }
    
    def record_cache_hit(self):
        """Record a cache hit."""
        self.metrics["cache_hits"] += 1
    
    def record_cache_miss(self):
        """Record a cache miss."""
        self.metrics["cache_misses"] += 1
    
    def record_function_call(self, response_time: float):
        """
        Record a function call with response time.
        
        Args:
            response_time (float): Response time in seconds
        """
        self.metrics["function_calls"] += 1
        # Update average response time
        current_avg = self.metrics["average_response_time"]
        calls = self.metrics["function_calls"]
        self.metrics["average_response_time"] = ((current_avg * (calls - 1)) + response_time) / calls
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get performance metrics.
        
        Returns:
            Dict[str, Any]: Performance metrics
        """
        # Calculate cache hit ratio
        total_cache_ops = self.metrics["cache_hits"] + self.metrics["cache_misses"]
        cache_hit_ratio = (
            self.metrics["cache_hits"] / total_cache_ops 
            if total_cache_ops > 0 else 0
        )
        
        return {
            **self.metrics,
            "cache_hit_ratio": cache_hit_ratio,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

# ============================================================================
# UTILITY FUNCTIONS
# Helper functions for common caching operations
# ============================================================================

def _safe_await(obj):
    """Safely await an object if it's a coroutine, otherwise return as-is."""
    if asyncio.iscoroutine(obj):
        # This should only be called in async contexts
        raise RuntimeError("_safe_await should not be called directly, use await")
    return obj

def _safe_decode(obj):
    """Safely decode an object if it has decode method and is not a coroutine."""
    if obj is None or asyncio.iscoroutine(obj) or asyncio.iscoroutinefunction(obj):
        return obj
    if isinstance(obj, bytes):
        return obj.decode('utf-8')
    if hasattr(obj, 'decode'):
        try:
            return obj.decode('utf-8')
        except:
            return obj
    return obj

def _safe_json_loads(obj):
    """Safely parse JSON from an object if it's a string and not a coroutine."""
    if obj is None or asyncio.iscoroutine(obj) or asyncio.iscoroutinefunction(obj):
        return obj
    if isinstance(obj, str):
        try:
            return json.loads(obj)
        except json.JSONDecodeError:
            return obj
    return obj

def _safe_len(obj):
    """Safely get the length of an object if it's sized and not a coroutine."""
    if obj is None or asyncio.iscoroutine(obj) or asyncio.iscoroutinefunction(obj):
        return 0
    if hasattr(obj, '__len__'):
        try:
            return len(obj)
        except:
            return 0
    return 0

def _safe_int_bool(obj):
    """Safely convert an object to int and check if > 0, handling coroutines."""
    if obj is None or asyncio.iscoroutine(obj) or asyncio.iscoroutinefunction(obj):
        return False
    try:
        return int(obj) > 0
    except (ValueError, TypeError):
        return False

def _safe_int(obj):
    """Safely convert an object to int, handling coroutines."""
    if obj is None or asyncio.iscoroutine(obj) or asyncio.iscoroutinefunction(obj):
        return 0
    try:
        return int(obj)
    except (ValueError, TypeError):
        return 0

def _safe_iterable(obj):
    """Check if an object is iterable and not a coroutine."""
    if obj is None or asyncio.iscoroutine(obj) or asyncio.iscoroutinefunction(obj):
        return False
    return hasattr(obj, '__iter__')

def _safe_dict_get(obj, key, default=None):
    """Safely get a value from a dict-like object, handling coroutines."""
    if obj is None or asyncio.iscoroutine(obj) or asyncio.iscoroutinefunction(obj):
        return default
    if hasattr(obj, 'get'):
        try:
            return obj.get(key, default)
        except:
            return default
    return default

def _safe_delete_keys(client, keys):
    """Safely delete keys from Redis, handling coroutines and unpacking issues."""
    if client is None or keys is None:
        return 0
    
    try:
        # Check if keys is iterable and not a coroutine
        if not _safe_iterable(keys):
            return 0
            
        # Convert keys to a list to avoid unpacking issues
        keys_list = list(keys)
        if not keys_list:
            return 0
            
        result = client.delete(*keys_list)
        # Handle async response if needed
        if asyncio.iscoroutine(result):
            result = asyncio.run(result)
        return _safe_int(result)
    except Exception as e:
        logger.warning("Failed to delete keys", error=str(e))
        return 0

def initialize_cache():
    """Initialize the cache system."""
    logger.info("Initializing cache system")
    return redis_client.connect()

def shutdown_cache():
    """Shutdown the cache system."""
    logger.info("Shutting down cache system")
    redis_client.disconnect()

def get_cache_status() -> Dict[str, Any]:
    """
    Get cache system status.
    
    Returns:
        Dict[str, Any]: Cache system status
    """
    return {
        "redis_connected": redis_client.is_connected(),
        "cache_stats": CacheManager.get_stats(),
        "performance_metrics": performance_monitor.get_metrics()
    }