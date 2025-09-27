/**
 * Notifications Hook for MyBrand Job Application Platform
 * 
 * This hook provides real-time notification functionality using WebSocket
 * connections with automatic reconnection and browser notification support.
 * 
 * @version 2.0
 * @author MyBrand Team
 */

// ============================================================================
// IMPORT STATEMENTS
// External and internal dependencies
// ============================================================================

import { useEffect, useState } from 'react';
import { createNotificationWebSocket } from '@/src/api/client';

// ============================================================================
// DATA INTERFACES
// TypeScript interfaces for notification data structures
// ============================================================================

/**
 * Notification message interface
 * 
 * Represents a single notification message with all relevant metadata
 */
interface NotificationMessage {
  id: string;
  title: string;
  message: string;
  type: string;
  timestamp: string;
  read?: boolean;
}

// ============================================================================
// HOOK IMPLEMENTATION
// Main hook function with comprehensive documentation
// ============================================================================

/**
 * Custom React hook for real-time notifications
 * 
 * This hook establishes a WebSocket connection to the notification service
 * and manages incoming notifications with automatic reconnection, browser
 * notifications, and state management.
 * 
 * @param userId - Optional user ID for personalized notifications
 * @returns Object containing notifications, connection status, and management functions
 * 
 * @example
 * ```typescript
 * const { notifications, unreadCount, isConnected, markAsRead, clearAll } = useNotifications('user123');
 * 
 * return (
 *   <div>
 *     <div>Connection: {isConnected ? 'Connected' : 'Disconnected'}</div>
 *     <div>Unread: {unreadCount}</div>
 *     {notifications.map(notification => (
 *       <NotificationItem
 *         key={notification.id}
 *         notification={notification}
 *         onMarkAsRead={markAsRead}
 *       />
 *     ))}
 *   </div>
 * );
 * ```
 */
export function useNotifications(userId?: string) {
  // State for storing notifications and connection status
  const [notifications, setNotifications] = useState<NotificationMessage[]>([]);
  const [isConnected, setIsConnected] = useState(false);

  /**
   * Effect for managing WebSocket connection lifecycle
   * 
   * Establishes WebSocket connection, handles events, and implements
   * automatic reconnection with proper cleanup.
   */
  useEffect(() => {
    // WebSocket connection and reconnection management variables
    let ws: WebSocket | null = null;
    let reconnectTimeout: NodeJS.Timeout | null = null;

    /**
     * Establish WebSocket connection to notification service
     * 
     * Creates a new WebSocket connection and sets up event handlers
     * for open, message, error, and close events.
     */
    const connect = () => {
      try {
        // Create WebSocket connection using API client utility
        ws = createNotificationWebSocket(userId);
        
        /**
         * Handle WebSocket connection open event
         * 
         * Updates connection status and logs successful connection.
         */
        ws.onopen = () => {
          setIsConnected(true);
          console.log('Connected to notification service');
        };

        /**
         * Handle incoming WebSocket messages
         * 
         * Processes notification messages, filters out keep-alive messages,
         * and displays browser notifications for important events.
         */
        ws.onmessage = (event) => {
          try {
            // Parse incoming notification message
            const notification = JSON.parse(event.data);
            
            // Skip keep-alive messages to avoid cluttering notifications
            if (notification.title === 'Keep Alive') {
              return;
            }

            // Add timestamp if not present in the notification
            if (!notification.timestamp) {
              notification.timestamp = new Date().toISOString();
            }

            // Generate unique ID if not present in the notification
            if (!notification.id) {
              notification.id = `notif_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
            }

            // Add new notification to the beginning of the list and limit to 50
            setNotifications(prev => [notification, ...prev].slice(0, 50));
            
            // Show browser notification for important notification types
            if (notification.type !== 'job_match' && 'Notification' in window && Notification.permission === 'granted') {
              new Notification(notification.title, {
                body: notification.message,
                icon: '/favicon.ico',
              });
            }
          } catch (error) {
            console.error('Error parsing notification:', error);
          }
        };

        /**
         * Handle WebSocket error events
         * 
         * Logs errors and updates connection status.
         */
        ws.onerror = (error) => {
          console.error('Notification stream error:', error);
          setIsConnected(false);
        };

        /**
         * Handle WebSocket close events
         * 
         * Updates connection status and schedules reconnection attempt.
         */
        ws.onclose = () => {
          setIsConnected(false);
          console.log('Notification service disconnected');
          
          // Schedule reconnection after 5 seconds
          reconnectTimeout = setTimeout(connect, 5000);
        };
      } catch (error) {
        console.error('Failed to connect to notification service:', error);
        setIsConnected(false);
        
        // Schedule reconnection after 5 seconds
        reconnectTimeout = setTimeout(connect, 5000);
      }
    };

    // Initial connection attempt
    connect();

    /**
     * Cleanup function for WebSocket connection
     * 
     * Closes WebSocket connection and clears reconnection timers
     * when component unmounts or dependencies change.
     */
    return () => {
      setIsConnected(false);
      if (ws) {
        try {
          ws.close();
        } catch (error) {
          console.error('Error closing notification stream:', error);
        }
      }
      if (reconnectTimeout) {
        clearTimeout(reconnectTimeout);
      }
    };
  }, [userId]);

  /**
   * Mark a notification as read
   * 
   * Updates the read status of a specific notification by ID.
   * 
   * @param notificationId - The ID of the notification to mark as read
   */
  const markAsRead = (notificationId: string) => {
    setNotifications(prev =>
      prev.map(n => n.id === notificationId ? { ...n, read: true } : n)
    );
  };

  /**
   * Clear all notifications
   * 
   * Removes all notifications from the notification list.
   */
  const clearAll = () => {
    setNotifications([]);
  };

  /**
   * Calculate unread notification count
   * 
   * Counts the number of notifications that have not been marked as read.
   */
  const unreadCount = notifications.filter(n => !n.read).length;

  /**
   * Return hook API
   * 
   * Provides access to notifications, connection status, and management functions.
   */
  return {
    notifications,
    unreadCount,
    isConnected,
    markAsRead,
    clearAll,
  };
}