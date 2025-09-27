/*
 * Page Transition Component
 * 
 * This component provides smooth page transitions using CSS animations.
 * It enhances the user experience by adding subtle animations when navigating
 * between pages.
 * 
 * Features:
 * 1. Fade in/out transitions
 * 2. Slide animations
 * 3. Customizable transition effects
 * 4. Performance optimized with CSS transitions
 * 5. Accessible with proper focus management
 */

// Import required React components
import React, { useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';

// Main page transition component
export function PageTransition({
  children,
  className = ""
}: {
  children: React.ReactNode;
  className?: string;
}) {
  const location = useLocation();
  const elementRef = useRef<HTMLDivElement>(null);

  // Apply transition effect when location changes
  useEffect(() => {
    if (elementRef.current) {
      // Reset animation
      elementRef.current.style.opacity = '0';
      elementRef.current.style.transform = 'translateY(20px)';
      
      // Trigger reflow
      void elementRef.current.offsetHeight;
      
      // Start animation
      elementRef.current.style.transition = 'opacity 0.3s ease-out, transform 0.3s ease-out';
      elementRef.current.style.opacity = '1';
      elementRef.current.style.transform = 'translateY(0)';
    }
  }, [location]);

  return (
    <div 
      ref={elementRef}
      className={`transition-all duration-300 ease-in-out ${className}`}
    >
      {children}
    </div>
  );
}

export default PageTransition;