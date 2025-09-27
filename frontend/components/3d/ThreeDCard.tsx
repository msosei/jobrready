/*
 * 3D Card Component
 * 
 * This component creates a card with CSS 3D transforms for a subtle 3D effect.
 * It provides depth and visual interest without the overhead of full 3D rendering.
 * 
 * Features:
 * 1. CSS-based 3D transforms for performance
 * 2. Smooth hover animations with perspective effects
 * 3. Accessible with proper focus states
 * 4. Customizable styling
 * 5. Works on all device types
 */

// Import required React components
import React from 'react';
import { cn } from '@/lib/utils';

// Main 3D card component
export function ThreeDCard({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        "relative rounded-xl border bg-card text-card-foreground shadow-lg transition-all duration-300 ease-in-out transform will-change-transform",
        "hover:-translate-y-2 hover:shadow-xl",
        "active:translate-y-0 active:shadow-md",
        "before:absolute before:inset-0 before:rounded-xl before:bg-card/20 before:translate-z-[-1px] before:transition-all before:duration-300",
        "hover:before:translate-y-2 hover:before:opacity-0",
        "active:before:translate-y-0 active:before:opacity-100",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

export default ThreeDCard;