/**
 * Loading Spinner Component for MyBrand Job Application Platform
 * 
 * This component provides a reusable loading spinner with different sizes
 * and optional text, using the Lucide React icon library.
 * 
 * @version 2.0
 * @author MyBrand Team
 */

// ============================================================================
// IMPORT STATEMENTS
// External and internal dependencies
// ============================================================================

import { Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';

// ============================================================================
// COMPONENT PROPS INTERFACE
// TypeScript interface for component properties
// ============================================================================

/**
 * Loading spinner component props interface
 * 
 * Defines the configurable properties for the loading spinner component
 */
interface LoadingSpinnerProps {
  /** Size of the spinner - small, medium, or large */
  size?: 'sm' | 'md' | 'lg';
  
  /** Additional CSS classes to apply to the container */
  className?: string;
  
  /** Optional text to display alongside the spinner */
  text?: string;
}

// ============================================================================
// COMPONENT IMPLEMENTATION
// Main component function with comprehensive documentation
// ============================================================================

/**
 * Loading spinner component with configurable size and text
 * 
 * This component displays a spinning loader icon with optional text,
 * commonly used to indicate loading states in the application.
 * 
 * @param props - Component properties
 * @param props.size - Size of the spinner (default: 'md')
 * @param props.className - Additional CSS classes for styling
 * @param props.text - Optional text to display with the spinner
 * @returns JSX element representing the loading spinner
 * 
 * @example
 * ```tsx
 * // Basic usage
 * <LoadingSpinner />
 * 
 * // With custom size and text
 * <LoadingSpinner size="lg" text="Loading jobs..." />
 * 
 * // With custom styling
 * <LoadingSpinner className="my-4" />
 * ```
 */
export default function LoadingSpinner({ size = 'md', className, text }: LoadingSpinnerProps) {
  /**
   * Size-specific CSS classes mapping
   * 
   * Defines the height and width classes for different spinner sizes
   */
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-6 w-6',
    lg: 'h-8 w-8',
  };

  /**
   * Render the loading spinner component
   * 
   * Returns a div containing the animated spinner icon and optional text
   */
  return (
    <div 
      className={cn('flex items-center justify-center', className)} 
      role="status" 
      aria-label="Loading"
    >
      <div className="flex items-center gap-2">
        <Loader2 
          className={cn('animate-spin text-muted-foreground', sizeClasses[size])} 
        />
        {text && <span className="text-sm text-muted-foreground">{text}</span>}
      </div>
    </div>
  );
}