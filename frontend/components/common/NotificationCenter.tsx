/**
 * Notification Center Component for MyBrand Job Application Platform
 * 
 * This component provides a notification center with real-time updates
 * using WebSocket connections, displaying job matches, application status,
 * and other important notifications.
 * 
 * @version 2.0
 * @author MyBrand Team
 */

// ============================================================================
// IMPORT STATEMENTS
// React component and utility imports
// ============================================================================

import { useState } from 'react';
import { Bell, Check, Trash2, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from '@/components/ui/sheet';
import { ScrollArea } from '@/components/ui/scroll-area';
import { useNotifications } from '../../hooks/useNotifications';
import { formatDistanceToNow } from 'date-fns';

// ============================================================================
// COMPONENT PROPS INTERFACE
// TypeScript interface for component properties
// ============================================================================

/**
 * Notification center component props interface
 * 
 * Defines the properties required to display the notification center
 */
interface NotificationCenterProps {
  /** Optional user ID for personalized notifications */
  userId?: string;
}

// ============================================================================
// COMPONENT IMPLEMENTATION
// Main component function with comprehensive documentation
// ============================================================================

/**
 * Notification center component for displaying real-time notifications
 * 
 * This component renders a slide-out panel with real-time notifications
 * using WebSocket connections. It displays job matches, application status
 * updates, and other important notifications with read/unread status
 * and connection indicators.
 * 
 * @param props - Component properties
 * @param props.userId - Optional user ID for personalized notifications
 * @returns JSX element representing the notification center
 * 
 * @example
 * ```tsx
 * <NotificationCenter userId="user123" />
 * ```
 */
export default function NotificationCenter({ userId }: NotificationCenterProps) {
  // State for managing the open/closed state of the notification sheet
  const [isOpen, setIsOpen] = useState(false);
  
  // Get notification data and functions from the useNotifications hook
  const { notifications, unreadCount, isConnected, markAsRead, clearAll } = useNotifications(userId);

  /**
   * Get appropriate icon for notification type
   * 
   * Returns an emoji icon based on the notification type for visual distinction
   * 
   * @param type - The type of notification
   * @returns Emoji string representing the notification type
   */
  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'job_match':
        return '🎯';
      case 'application_status':
        return '📋';
      case 'new_job':
        return '💼';
      default:
        return '🔔';
    }
  };

  /**
   * Render the notification center component
   * 
   * Returns a sheet component with notification list and management controls
   */
  return (
    <Sheet open={isOpen} onOpenChange={setIsOpen}>
      <SheetTrigger asChild>
        <Button
          variant="ghost"
          size="icon"
          className="relative"
          aria-label={`Notifications ${unreadCount > 0 ? `(${unreadCount} unread)` : ''}`}
        >
          <Bell className="h-5 w-5" />
          {unreadCount > 0 && (
            <Badge
              variant="destructive"
              className="absolute -top-1 -right-1 h-5 w-5 rounded-full p-0 flex items-center justify-center text-xs"
            >
              {unreadCount > 99 ? '99+' : unreadCount}
            </Badge>
          )}
        </Button>
      </SheetTrigger>
      <SheetContent side="right" className="w-[400px] sm:w-[500px]">
        <SheetHeader className="space-y-4">
          <div className="flex items-center justify-between">
            <SheetTitle>Notifications</SheetTitle>
            <div className="flex items-center gap-2">
              <div className={`h-2 w-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
              <span className="text-xs text-muted-foreground">
                {isConnected ? 'Connected' : 'Disconnected'}
              </span>
            </div>
          </div>
          {notifications.length > 0 && (
            <div className="flex items-center gap-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={clearAll}
                className="h-8 px-3"
              >
                <Trash2 className="h-4 w-4 mr-2" />
                Clear All
              </Button>
            </div>
          )}
        </SheetHeader>

        <ScrollArea className="h-[calc(100vh-120px)] mt-6">
          {notifications.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-64 text-center">
              <Bell className="h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-lg font-medium mb-2">No notifications</h3>
              <p className="text-sm text-muted-foreground">
                We'll notify you when there's something new!
              </p>
            </div>
          ) : (
            <div className="space-y-2">
              {notifications.map((notification) => (
                <div
                  key={notification.id}
                  className={`p-4 rounded-lg border transition-colors ${
                    notification.read 
                      ? 'bg-background border-border' 
                      : 'bg-primary/5 border-primary/20'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <span className="text-xl" role="img" aria-label={notification.type}>
                      {getNotificationIcon(notification.type)}
                    </span>
                    <div className="flex-1 space-y-1">
                      <div className="flex items-center justify-between">
                        <h4 className="text-sm font-medium">{notification.title}</h4>
                        {!notification.read && (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => markAsRead(notification.id)}
                            className="h-6 w-6 p-0"
                            aria-label="Mark as read"
                          >
                            <Check className="h-3 w-3" />
                          </Button>
                        )}
                      </div>
                      <p className="text-sm text-muted-foreground">{notification.message}</p>
                      <p className="text-xs text-muted-foreground">
                        {formatDistanceToNow(new Date(notification.timestamp), { addSuffix: true })}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </ScrollArea>
      </SheetContent>
    </Sheet>
  );
}