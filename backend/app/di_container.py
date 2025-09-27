"""
Dependency Injection Container for MyBrand Job Application Platform
Version: v2
Purpose: Centralized dependency injection container for managing service dependencies
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for dependency injection
# ============================================================================

from typing import Dict, Type, Any, Callable, Optional
import logging

# Set up logging for this module
logger = logging.getLogger(__name__)

# ============================================================================
# DEPENDENCY INJECTION CONTAINER
# A simple dependency injection container for managing service dependencies
# ============================================================================

class DIContainer:
    """
    A simple dependency injection container for managing service dependencies.
    
    This container allows registering and resolving dependencies by name or type,
    with support for singleton instances and factory functions.
    """
    
    def __init__(self):
        """Initialize the dependency injection container."""
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable[[], Any]] = {}
        self._singletons: Dict[str, Any] = {}
        
    def register(self, name: str, service: Any = None, factory: Optional[Callable[[], Any]] = None, singleton: bool = False):
        """
        Register a service with the container.
        
        Args:
            name (str): The name to register the service under
            service (Any, optional): The service instance to register
            factory (Callable, optional): A factory function to create the service
            singleton (bool): Whether to treat this as a singleton (default: False)
        """
        if service is not None:
            if singleton:
                self._singletons[name] = service
            else:
                self._services[name] = service
        elif factory is not None:
            self._factories[name] = factory
        else:
            raise ValueError("Either service or factory must be provided")
            
        logger.debug(f"Registered service: {name}")
        
    def resolve(self, name: str):
        """
        Resolve a service from the container.
        
        Args:
            name (str): The name of the service to resolve
            
        Returns:
            Any: The resolved service instance
            
        Raises:
            KeyError: If the service is not registered
        """
        # Check for singleton instance first
        if name in self._singletons:
            logger.debug(f"Resolved singleton service: {name}")
            return self._singletons[name]
            
        # Check for regular service instance
        if name in self._services:
            logger.debug(f"Resolved service: {name}")
            return self._services[name]
            
        # Check for factory function
        if name in self._factories:
            logger.debug(f"Resolved factory service: {name}")
            service = self._factories[name]()
            return service
            
        raise KeyError(f"Service '{name}' not registered")
        
    def unregister(self, name: str):
        """
        Unregister a service from the container.
        
        Args:
            name (str): The name of the service to unregister
        """
        if name in self._singletons:
            del self._singletons[name]
        if name in self._services:
            del self._services[name]
        if name in self._factories:
            del self._factories[name]
            
        logger.debug(f"Unregistered service: {name}")

# ============================================================================
# GLOBAL CONTAINER INSTANCE
# A global instance of the dependency injection container
# ============================================================================

# Create a global container instance
container = DIContainer()

# ============================================================================
# DECORATORS
# Decorators for easy service registration
# ============================================================================

def service(name: Optional[str] = None, singleton: bool = False):
    """
    Decorator for registering a class as a service.
    
    Args:
        name (str, optional): The name to register the service under
        singleton (bool): Whether to treat this as a singleton (default: False)
    """
    def decorator(cls):
        service_name = name or cls.__name__
        container.register(service_name, factory=lambda: cls(), singleton=singleton)
        return cls
    return decorator

def singleton(name: Optional[str] = None):
    """
    Decorator for registering a class as a singleton service.
    
    Args:
        name (str, optional): The name to register the service under
    """
    return service(name, singleton=True)

# ============================================================================
# UTILITY FUNCTIONS
# Helper functions for common dependency injection patterns
# ============================================================================

def inject(name: str):
    """
    Decorator for injecting a service into a function or method.
    
    Args:
        name (str): The name of the service to inject
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            service = container.resolve(name)
            return func(service, *args, **kwargs)
        return wrapper
    return decorator

def get_service(name: str):
    """
    Get a service from the container.
    
    Args:
        name (str): The name of the service to get
        
    Returns:
        Any: The service instance
    """
    return container.resolve(name)

def register_service(name: str, service: Any = None, factory: Optional[Callable[[], Any]] = None, singleton: bool = False):
    """
    Register a service with the container.
    
    Args:
        name (str): The name to register the service under
        service (Any, optional): The service instance to register
        factory (Callable, optional): A factory function to create the service
        singleton (bool): Whether to treat this as a singleton (default: False)
    """
    container.register(name, service, factory, singleton)