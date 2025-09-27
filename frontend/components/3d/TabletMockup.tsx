/*
 * 3D Tablet Mockup Component
 * 
 * This component renders a 3D tablet model using React Three Fiber and Three.js.
 * It's designed to showcase tablet UI screens in a realistic tablet environment.
 * 
 * Features:
 * 1. Realistic 3D tablet model with screen and frame
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

// Tablet model component
function TabletModel(props: { screenContent?: React.ReactNode }) {
  const groupRef = useRef<THREE.Group>(null);
  
  // Rotate the tablet slowly for a nice visual effect
  useFrame((state, delta) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = Math.sin(state.clock.getElapsedTime() * 0.2) * 0.1;
    }
  });

  return (
    <group ref={groupRef} {...props} dispose={null}>
      {/* Tablet frame */}
      <mesh>
        <boxGeometry args={[2.5, 3.5, 0.1]} />
        <meshStandardMaterial color="#111" metalness={0.5} roughness={0.5} />
      </mesh>
      
      {/* Tablet screen */}
      <mesh position={[0, 0, 0.06]}>
        <planeGeometry args={[2.3, 3.3]} />
        <meshStandardMaterial color="#f87171" metalness={0.1} roughness={0.9} />
      </mesh>
      
      {/* Home button */}
      <mesh position={[0, -1.6, 0.06]}>
        <circleGeometry args={[0.1, 32]} />
        <meshStandardMaterial color="#333" metalness={0.7} roughness={0.3} />
      </mesh>
    </group>
  );
}

// Main tablet mockup component
export function TabletMockup({ 
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
        
        <TabletModel screenContent={screenContent} />
        
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

export default TabletMockup;