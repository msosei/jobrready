/**
 * Error Message Component for MyBrand Job Application Platform
 * 
 * This component provides a standardized error display with optional
 * retry functionality, using the UI library components.
 * 
 * @version 2.0
 * @author MyBrand Team
 */

// ============================================================================
// IMPORT STATEMENTS
// External and internal dependencies
// ============================================================================

import { AlertCircle, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';

// ============================================================================
// COMPONENT PROPS INTERFACE
// TypeScript interface for component properties
// ============================================================================

/**
 * Error message component props interface
 * 
 * Defines the configurable properties for the error message component
 */
interface ErrorMessageProps {
  /** Title for the error message (default: 'Error') */
  title?: string;
  
  /** Detailed error message to display */
  message: string;
  
  /** Optional retry callback function */
  onRetry?: () => void;
  
  /** Additional CSS classes to apply to the alert */
  className?: string;
}

// ============================================================================
// COMPONENT IMPLEMENTATION
// Main component function with comprehensive documentation
// ============================================================================

/**
 * Error message component with optional retry functionality
 * 
 * This component displays a standardized error message with an optional
 * retry button, commonly used to handle and display error states in the application.
 * 
 * @param props - Component properties
 * @param props.title - Title for the error message (default: 'Error')
 * @param props.message - Detailed error message to display
 * @param props.onRetry - Optional callback function for retry action
 * @param props.className - Additional CSS classes for styling
 * @returns JSX element representing the error message
 * 
 * @example
 * ```tsx
 * // Basic usage
 * <ErrorMessage message="Failed to load jobs" />
 * 
 * // With custom title and retry
 * <ErrorMessage 
 *   title="Connection Error" 
 *   message="Unable to connect to the server" 
 *   onRetry={retryFunction}
 * />
 * ```
 */
export default function ErrorMessage({ 
  title = 'Error', 
  message, 
  onRetry, 
  className 
}: ErrorMessageProps) {
  /**
   * Render the error message component
   * 
   * Returns an alert component with error styling, message content,
   * and optional retry button.
   */
  return (
    <Alert 
      variant="destructive" 
      className={className} 
      role="alert"
    >
      <AlertCircle className="h-4 w-4" />
      <AlertDescription className="flex items-center justify-between">
        <div>
          <div className="font-medium">{title}</div>
          <div className="text-sm">{message}</div>
        </div>
        {onRetry && (
          <Button
            variant="outline"
            size="sm"
            onClick={onRetry}
            className="ml-4 border-destructive text-destructive hover:bg-destructive hover:text-destructive-foreground"
          >
            <RefreshCw className="h-4 w-4 mr-2" />
            Retry
          </Button>
        )}
      </AlertDescription>
    </Alert>
  );
}