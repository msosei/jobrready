/*
 * 3D Device Showcase Component
 * 
 * This component displays a collection of 3D device mockups (laptop, phone, tablet)
 * to showcase UI screens across different device types.
 * 
 * Features:
 * 1. Responsive grid layout for device mockups
 * 2. Interactive 3D models with orbit controls
 * 3. Smooth animations and transitions
 * 4. Performance optimized rendering
 * 5. Mobile-friendly design
 */

// Import required React components
import React from 'react';
import LaptopMockup from './LaptopMockup';
import PhoneMockup from './PhoneMockup';
import TabletMockup from './TabletMockup';

// Main device showcase component
export function DeviceShowcase({ 
  className = ""
}: { 
  className?: string;
}) {
  return (
    <div className={`grid grid-cols-1 md:grid-cols-3 gap-8 ${className}`}>
      {/* Laptop Mockup */}
      <div className="flex flex-col items-center">
        <h3 className="text-lg font-semibold mb-4">Desktop View</h3>
        <LaptopMockup />
      </div>
      
      {/* Phone Mockup */}
      <div className="flex flex-col items-center">
        <h3 className="text-lg font-semibold mb-4">Mobile View</h3>
        <PhoneMockup />
      </div>
      
      {/* Tablet Mockup */}
      <div className="flex flex-col items-center">
        <h3 className="text-lg font-semibold mb-4">Tablet View</h3>
        <TabletMockup />
      </div>
    </div>
  );
}

export default DeviceShowcase;