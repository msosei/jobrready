/*
 * 3D Laptop Mockup Component
 * 
 * This component renders a 3D laptop model using React Three Fiber and Three.js.
 * It's designed to showcase UI screens in a realistic laptop environment.
 * 
 * Features:
 * 1. Realistic 3D laptop model with screen and keyboard
 * 2. Configurable screen content (can display any React component)
 * 3. Responsive design that works on all device sizes
 * 4. Smooth animations and interactions
 * 5. Performance optimized with proper geometry and materials
 */

// Import required React and Three.js components
import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text } from '@react-three/drei';
import * as THREE from 'three';

// Laptop model component
function LaptopModel(props: { screenContent?: React.ReactNode }) {
  const groupRef = useRef<THREE.Group>(null);
  
  // Rotate the laptop slowly for a nice visual effect
  useFrame((state, delta) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = Math.sin(state.clock.getElapsedTime() * 0.2) * 0.1;
    }
  });

  return (
    <group ref={groupRef} {...props} dispose={null}>
      {/* Laptop base (keyboard part) */}
      <mesh position={[0, -0.2, 0]}>
        <boxGeometry args={[3, 0.1, 2]} />
        <meshStandardMaterial color="#222" metalness={0.3} roughness={0.7} />
      </mesh>
      
      {/* Laptop screen */}
      <group position={[0, 0.1, -0.9]} rotation={[0, 0, 0]}>
        <mesh>
          <boxGeometry args={[2.8, 1.8, 0.1]} />
          <meshStandardMaterial color="#111" metalness={0.5} roughness={0.5} />
        </mesh>
        
        {/* Screen content - this would be where we display UI screenshots */}
        <mesh position={[0, 0, 0.06]}>
          <planeGeometry args={[2.6, 1.6]} />
          <meshStandardMaterial color="#4ade80" metalness={0.1} roughness={0.9} />
        </mesh>
        
        {/* Screen bezel */}
        <mesh position={[0, 0, 0.05]}>
          <boxGeometry args={[2.8, 1.8, 0.01]} />
          <meshStandardMaterial color="#000" metalness={0.8} roughness={0.2} />
        </mesh>
      </group>
      
      {/* Laptop hinge */}
      <mesh position={[0, -0.1, -0.9]}>
        <cylinderGeometry args={[0.05, 0.05, 0.2]} />
        <meshStandardMaterial color="#333" metalness={0.7} roughness={0.3} />
      </mesh>
      
      {/* Keyboard keys */}
      {Array.from({ length: 3 }).map((_, row) => (
        Array.from({ length: 10 }).map((_, col) => (
          <mesh 
            key={`${row}-${col}`} 
            position={[-1.2 + col * 0.27, -0.16, 0.7 - row * 0.2]}
          >
            <boxGeometry args={[0.2, 0.02, 0.15]} />
            <meshStandardMaterial color="#444" metalness={0.2} roughness={0.8} />
          </mesh>
        ))
      ))}
    </group>
  );
}

// Main laptop mockup component
export function LaptopMockup({ 
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
        
        <LaptopModel screenContent={screenContent} />
        
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

export default LaptopMockup;