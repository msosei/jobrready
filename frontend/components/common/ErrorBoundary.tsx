/**
 * Error Boundary Component for MyBrand Job Application Platform
 * 
 * This component provides error boundary functionality to catch JavaScript
 * errors in child components and display a fallback UI instead of crashing
 * the entire application.
 * 
 * @version 2.0
 * @author MyBrand Team
 */

// ============================================================================
// IMPORT STATEMENTS
// React component and utility imports
// ============================================================================

import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

// ============================================================================
// COMPONENT PROPS AND STATE INTERFACES
// TypeScript interfaces for component properties and state
// ============================================================================

/**
 * Error boundary component props interface
 * 
 * Defines the properties for the error boundary component
 */
interface Props {
  /** Child components to wrap with error boundary */
  children: ReactNode;
  
  /** Optional fallback UI to display when an error occurs */
  fallback?: ReactNode;
}

/**
 * Error boundary component state interface
 * 
 * Defines the state for the error boundary component
 */
interface State {
  /** Whether an error has been caught */
  hasError: boolean;
  
  /** The error that was caught, if any */
  error?: Error;
}

// ============================================================================
// COMPONENT IMPLEMENTATION
// Main component class with comprehensive documentation
// ============================================================================

/**
 * Error boundary component for catching and handling component errors
 * 
 * This component implements React's error boundary functionality to catch
 * JavaScript errors in child components, log them, and display a fallback UI
 * instead of letting the entire application crash.
 * 
 * @example
 * ```tsx
 * <ErrorBoundary>
 *   <MyComponent />
 * </ErrorBoundary>
 * ```
 */
export class ErrorBoundary extends Component<Props, State> {
  /**
   * Initial component state
   * 
   * Sets the initial state with no error caught
   */
  public state: State = {
    hasError: false,
  };

  /**
   * Static method to update state when an error is caught
   * 
   * This lifecycle method is called when an error is thrown in any child component
   * 
   * @param error - The error that was thrown
   * @returns New state with error information
   */
  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  /**
   * Lifecycle method called after an error is caught
   * 
   * This method is called after an error is caught and logged for debugging purposes
   * 
   * @param error - The error that was thrown
   * @param errorInfo - Information about the error and component stack
   */
  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  /**
   * Handle retry action to reset the error boundary
   * 
   * Resets the error state to allow the component tree to re-render
   */
  private handleRetry = () => {
    this.setState({ hasError: false, error: undefined });
  };

  /**
   * Render the error boundary component
   * 
   * Returns either the fallback UI when an error has occurred or the child components
   * 
   * @returns JSX element representing the error boundary or its children
   */
  public render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="flex items-center justify-center min-h-[400px] p-4">
          <Card className="w-full max-w-md">
            <CardHeader className="text-center">
              <AlertTriangle className="h-12 w-12 text-destructive mx-auto mb-4" />
              <CardTitle className="text-destructive">Something went wrong</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-sm text-muted-foreground text-center">
                An unexpected error occurred. Please try refreshing the page.
              </p>
              {process.env.NODE_ENV === 'development' && this.state.error && (
                <details className="text-xs bg-muted p-2 rounded">
                  <summary>Error Details</summary>
                  <pre className="mt-2 whitespace-pre-wrap">{this.state.error.stack}</pre>
                </details>
              )}
              <div className="flex gap-2">
                <Button
                  onClick={this.handleRetry}
                  className="flex-1"
                  size="sm"
                >
                  <RefreshCw className="h-4 w-4 mr-2" />
                  Try Again
                </Button>
                <Button
                  onClick={() => window.location.reload()}
                  variant="outline"
                  className="flex-1"
                  size="sm"
                >
                  Refresh Page
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      );
    }

    return this.props.children;
  }
}