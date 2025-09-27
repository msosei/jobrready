/*
 * 3D Button Component
 * 
 * This component creates a button with CSS 3D transforms for a subtle 3D effect.
 * It provides depth and visual interest without the overhead of full 3D rendering.
 * 
 * Features:
 * 1. CSS-based 3D transforms for performance
 * 2. Smooth hover and active animations
 * 3. Accessible with proper focus states
 * 4. Customizable styling and sizes
 * 5. Works on all device types
 */

// Import required React components
import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

// Define button variants using class-variance-authority
const buttonVariants = cva(
  "relative inline-flex items-center justify-center rounded-md font-medium transition-all duration-300 ease-in-out transform will-change-transform",
  {
    variants: {
      variant: {
        default: [
          "bg-primary text-primary-foreground shadow-lg",
          "hover:-translate-y-1 hover:shadow-xl",
          "active:translate-y-0 active:shadow-md",
          "before:absolute before:inset-0 before:rounded-md before:bg-primary/20 before:translate-z-[-1px] before:transition-all before:duration-300",
          "hover:before:translate-y-1 hover:before:opacity-0",
          "active:before:translate-y-0 active:before:opacity-100"
        ],
        secondary: [
          "bg-secondary text-secondary-foreground shadow-md",
          "hover:-translate-y-1 hover:shadow-lg",
          "active:translate-y-0 active:shadow-md",
          "before:absolute before:inset-0 before:rounded-md before:bg-secondary/20 before:translate-z-[-1px] before:transition-all before:duration-300",
          "hover:before:translate-y-1 hover:before:opacity-0",
          "active:before:translate-y-0 active:before:opacity-100"
        ],
        outline: [
          "border border-input bg-background shadow-sm",
          "hover:-translate-y-1 hover:shadow-md",
          "active:translate-y-0 active:shadow-sm",
          "before:absolute before:inset-0 before:rounded-md before:bg-background/20 before:translate-z-[-1px] before:transition-all before:duration-300",
          "hover:before:translate-y-1 hover:before:opacity-0",
          "active:before:translate-y-0 active:before:opacity-100"
        ],
        ghost: [
          "hover:bg-accent hover:text-accent-foreground",
          "hover:-translate-y-0.5",
          "active:translate-y-0"
        ]
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10"
      }
    },
    defaultVariants: {
      variant: "default",
      size: "default"
    }
  }
);

// Define props interface
interface ThreeDButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

// Main 3D button component
const ThreeDButton = React.forwardRef<HTMLButtonElement, ThreeDButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);

ThreeDButton.displayName = "ThreeDButton";

export { ThreeDButton, buttonVariants };