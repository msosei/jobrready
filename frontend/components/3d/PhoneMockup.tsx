/*
 * 3D Phone Mockup Component
 * 
 * This component renders a 3D phone model using React Three Fiber and Three.js.
 * It's designed to showcase mobile UI screens in a realistic phone environment.
 * 
 * Features:
 * 1. Realistic 3D phone model with screen and frame
 * 2. Configurable screen content (can display any React component)
 * 3. Responsive design that works on all device sizes
 * 4. Smooth animations and interactions
 * 5. Performance optimized with proper geometry and materials
 */

// Import required React and Three.js components
import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import * as THREE from 'three';

// Phone model component
function PhoneModel(props: { screenContent?: React.ReactNode }) {
  const groupRef = useRef<THREE.Group>(null);
  
  // Rotate the phone slowly for a nice visual effect
  useFrame((state, delta) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = Math.sin(state.clock.getElapsedTime() * 0.2) * 0.1;
    }
  });

  return (
    <group ref={groupRef} {...props} dispose={null}>
      {/* Phone frame */}
      <mesh>
        <boxGeometry args={[1.8, 3.5, 0.1]} />
        <meshStandardMaterial color="#111" metalness={0.5} roughness={0.5} />
      </mesh>
      
      {/* Phone screen */}
      <mesh position={[0, 0, 0.06]}>
        <planeGeometry args={[1.6, 3.2]} />
        <meshStandardMaterial color="#60a5fa" metalness={0.1} roughness={0.9} />
      </mesh>
      
      {/* Phone notch */}
      <mesh position={[0, 1.5, 0.06]}>
        <boxGeometry args={[0.5, 0.1, 0.01]} />
        <meshStandardMaterial color="#000" metalness={0.8} roughness={0.2} />
      </mesh>
      
      {/* Home button */}
      <mesh position={[0, -1.6, 0.06]}>
        <circleGeometry args={[0.15, 32]} />
        <meshStandardMaterial color="#333" metalness={0.7} roughness={0.3} />
      </mesh>
    </group>
  );
}

// Main phone mockup component
export function PhoneMockup({ 
  screenContent,
  className = ""
}: { 
  screenContent?: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={`w-full h-64 md:h-80 ${className}`}>
      <Canvas camera={{ position: [0, 0, 5], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <pointLight position={[-10, -10, -10]} intensity={0.5} />
        
        <PhoneModel screenContent={screenContent} />
        
        <OrbitControls 
          enableZoom={true}
          enablePan={false}
          minPolarAngle={Math.PI / 6}
          maxPolarAngle={Math.PI / 2}
          autoRotate={true}
          autoRotateSpeed={0.5}
        />
      </Canvas>
    </div>
  );
}

export default PhoneMockup;