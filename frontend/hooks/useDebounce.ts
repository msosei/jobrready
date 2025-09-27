/**
 * Debounce Hook for MyBrand Job Application Platform
 * 
 * This hook provides debouncing functionality to delay execution of
 * functions or state updates until a specified time has passed.
 * 
 * @version 2.0
 * @author MyBrand Team
 */

// ============================================================================
// IMPORT STATEMENTS
// External dependencies
// ============================================================================

import { useEffect, useState } from 'react';

// ============================================================================
// HOOK IMPLEMENTATION
// Main hook function with comprehensive documentation
// ============================================================================

/**
 * Custom React hook for debouncing value changes
 * 
 * This hook delays updating a value until a specified time has passed
 * since the last change, which is useful for optimizing performance
 * in scenarios like search input handling.
 * 
 * @template T - The type of value to debounce
 * @param value - The value to debounce
 * @param delay - The delay in milliseconds before updating the debounced value
 * @returns The debounced value that updates after the delay
 * 
 * @example
 * ```typescript
 * const [searchTerm, setSearchTerm] = useState('');
 * const debouncedSearchTerm = useDebounce(searchTerm, 500);
 * 
 * useEffect(() => {
 *   // This will only run when searchTerm hasn't changed for 500ms
 *   performSearch(debouncedSearchTerm);
 * }, [debouncedSearchTerm]);
 * 
 * return (
 *   <input
 *     value={searchTerm}
 *     onChange={(e) => setSearchTerm(e.target.value)}
 *     placeholder="Search jobs..."
 *   />
 * );
 * ```
 */
export function useDebounce<T>(value: T, delay: number): T {
  // State to store the debounced value
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  /**
   * Effect for managing debounce timer
   * 
   * Sets up a timer to update the debounced value after the specified delay,
   * clearing any previous timers when the value or delay changes.
   */
  useEffect(() => {
    // Set up timer to update debounced value after delay
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    // Cleanup function to clear timer if value or delay changes
    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  // Return the debounced value
  return debouncedValue;
}