import { useEffect, useState } from 'react';
import backend from '~backend/client';
import type { NotificationMessage } from '~backend/notifications/stream';

export function useNotifications(userId?: string) {
  const [notifications, setNotifications] = useState<NotificationMessage[]>([]);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    let stream: any = null;
    let reconnectTimeout: NodeJS.Timeout | null = null;

    const connect = async () => {
      try {
        stream = await backend.notifications.notifications({ userId });
        setIsConnected(true);

        for await (const notification of stream) {
          // Skip keep-alive messages
          if (notification.title === 'Keep Alive') {
            continue;
          }

          setNotifications(prev => [notification, ...prev].slice(0, 50)); // Keep only last 50 notifications
          
          // Show browser notification for important types
          if (notification.type !== 'job_match' && 'Notification' in window && Notification.permission === 'granted') {
            new Notification(notification.title, {
              body: notification.message,
              icon: '/favicon.ico',
            });
          }
        }
      } catch (error) {
        console.error('Notification stream error:', error);
        setIsConnected(false);
        
        // Reconnect after 5 seconds
        reconnectTimeout = setTimeout(connect, 5000);
      }
    };

    connect();

    return () => {
      setIsConnected(false);
      if (stream) {
        try {
          stream.close?.();
        } catch (error) {
          console.error('Error closing notification stream:', error);
        }
      }
      if (reconnectTimeout) {
        clearTimeout(reconnectTimeout);
      }
    };
  }, [userId]);

  const markAsRead = (notificationId: string) => {
    setNotifications(prev =>
      prev.map(n => n.id === notificationId ? { ...n, read: true } : n)
    );
  };

  const clearAll = () => {
    setNotifications([]);
  };

  const unreadCount = notifications.filter(n => !n.read).length;

  return {
    notifications,
    unreadCount,
    isConnected,
    markAsRead,
    clearAll,
  };
}
