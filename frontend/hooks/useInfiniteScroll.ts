/**
 * Infinite Scroll Hook for MyBrand Job Application Platform
 * 
 * This hook provides infinite scroll functionality using Intersection Observer
 * for efficient pagination and lazy loading of content.
 * 
 * @version 2.0
 * @author MyBrand Team
 */

// ============================================================================
// IMPORT STATEMENTS
// External dependencies
// ============================================================================

import { useCallback, useEffect, useRef } from 'react';

// ============================================================================
// DATA INTERFACES
// TypeScript interfaces for hook configuration
// ============================================================================

/**
 * Infinite scroll hook configuration interface
 * 
 * Defines the parameters and callbacks needed for infinite scroll functionality
 */
interface UseInfiniteScrollProps {
  /** Whether there are more items to load */
  hasNextPage: boolean;
  
  /** Whether the next page is currently being fetched */
  isFetchingNextPage: boolean;
  
  /** Function to fetch the next page of data */
  fetchNextPage: () => void;
  
  /** Distance from bottom to trigger loading (in pixels) */
  threshold?: number;
}

// ============================================================================
// HOOK IMPLEMENTATION
// Main hook function with comprehensive documentation
// ============================================================================

/**
 * Custom React hook for implementing infinite scroll pagination
 * 
 * This hook uses Intersection Observer to detect when a user has scrolled
 * near the bottom of a list and automatically triggers loading of the
 * next page of data.
 * 
 * @param props - Configuration object containing pagination state and callbacks
 * @returns Ref to attach to the sentinel element that triggers loading
 * 
 * @example
 * ```typescript
 * const { data, fetchNextPage, hasNextPage, isFetchingNextPage } = useInfiniteQuery(
 *   ['jobs'],
 *   fetchJobs,
 *   { getNextPageParam: (lastPage) => lastPage.nextCursor }
 * );
 * 
 * const loadMoreRef = useInfiniteScroll({
 *   hasNextPage,
 *   isFetchingNextPage,
 *   fetchNextPage
 * });
 * 
 * return (
 *   <div>
 *     {data?.pages.map(page => 
 *       page.jobs.map(job => <JobItem key={job.id} job={job} />)
 *     )}
 *     <div ref={loadMoreRef} />
 *     {isFetchingNextPage && <LoadingSpinner />}
 *   </div>
 * );
 * ```
 */
export function useInfiniteScroll({
  hasNextPage,
  isFetchingNextPage,
  fetchNextPage,
  threshold = 200,
}: UseInfiniteScrollProps) {
  // Ref for the sentinel element that triggers loading
  const loadMoreRef = useRef<HTMLDivElement>(null);

  /**
   * Handle intersection observer events
   * 
   * Triggered when the sentinel element enters the viewport,
   * indicating the user has scrolled near the bottom.
   */
  const handleIntersection = useCallback(
    (entries: IntersectionObserverEntry[]) => {
      const [entry] = entries;
      // Check if element is intersecting and we can load more data
      if (entry.isIntersecting && hasNextPage && !isFetchingNextPage) {
        fetchNextPage();
      }
    },
    [hasNextPage, isFetchingNextPage, fetchNextPage]
  );

  /**
   * Effect for managing Intersection Observer lifecycle
   * 
   * Creates and configures the Intersection Observer to watch
   * the sentinel element, with proper cleanup on unmount.
   */
  useEffect(() => {
    // Create Intersection Observer with specified threshold
    const observer = new IntersectionObserver(handleIntersection, {
      rootMargin: `${threshold}px`,
    });

    // Get current ref value for cleanup
    const currentRef = loadMoreRef.current;
    
    // Start observing the sentinel element
    if (currentRef) {
      observer.observe(currentRef);
    }

    // Cleanup function to stop observing
    return () => {
      if (currentRef) {
        observer.unobserve(currentRef);
      }
    };
  }, [handleIntersection, threshold]);

  // Return ref to attach to sentinel element
  return loadMoreRef;
}