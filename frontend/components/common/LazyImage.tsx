import { useState, useRef, useEffect } from 'react';
import { cn } from '@/lib/utils';

interface LazyImageProps extends React.ImgHTMLAttributes<HTMLImageElement> {
  src: string;
  alt: string;
  placeholder?: string;
  className?: string;
  fallback?: string;
}

export default function LazyImage({ 
  src, 
  alt, 
  placeholder, 
  className, 
  fallback, 
  ...props 
}: LazyImageProps) {
  const [isLoaded, setIsLoaded] = useState(false);
  const [hasError, setHasError] = useState(false);
  const [isInView, setIsInView] = useState(false);
  const imgRef = useRef<HTMLImageElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsInView(true);
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );

    if (imgRef.current) {
      observer.observe(imgRef.current);
    }

    return () => observer.disconnect();
  }, []);

  const handleLoad = () => {
    setIsLoaded(true);
  };

  const handleError = () => {
    setHasError(true);
  };

  const imageSrc = hasError && fallback ? fallback : src;
  const showImage = isInView && !hasError;

  return (
    <div ref={imgRef} className={cn('relative overflow-hidden', className)}>
      {/* Placeholder */}
      {(!isLoaded || !showImage) && (
        <div 
          className={cn(
            'absolute inset-0 bg-muted animate-pulse flex items-center justify-center',
            className
          )}
          aria-hidden="true"
        >
          {placeholder && (
            <span className="text-xs text-muted-foreground">{placeholder}</span>
          )}
        </div>
      )}
      
      {/* Actual image */}
      {showImage && (
        <img
          src={imageSrc}
          alt={alt}
          onLoad={handleLoad}
          onError={handleError}
          className={cn(
            'transition-opacity duration-300',
            isLoaded ? 'opacity-100' : 'opacity-0',
            className
          )}
          loading="lazy"
          {...props}
        />
      )}
    </div>
  );
}
