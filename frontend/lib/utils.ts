/**
 * Shared Utilities Module for MyBrand Job Application Platform
 * 
 * This module provides common utility functions and helpers used across the frontend application.
 * 
 * @version 2.0
 * @author MyBrand Team
 */

// ============================================================================
// IMPORT STATEMENTS
// External dependencies
// ============================================================================

import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

// ============================================================================
// STRING UTILITIES
// Functions for string manipulation and processing
// ============================================================================

/**
 * Truncate text to a maximum length with a suffix
 * 
 * @param text - The text to truncate
 * @param maxLength - Maximum length of the text (default: 100)
 * @param suffix - Suffix to append if text is truncated (default: "...")
 * @returns The truncated text
 * 
 * @example
 * ```typescript
 * const result = truncateText("This is a very long text", 10);
 * console.log(result); // "This is a..."
 * ```
 */
export function truncateText(text: string, maxLength: number = 100, suffix: string = "..."): string {
  if (!text) return "";
  
  if (text.length <= maxLength) {
    return text;
  }
  
  return text.substring(0, maxLength - suffix.length) + suffix;
}

/**
 * Generate a URL-friendly slug from text
 * 
 * @param text - The text to convert to a slug
 * @returns The generated slug
 * 
 * @example
 * ```typescript
 * const slug = generateSlug("Job Title Here");
 * console.log(slug); // "job-title-here"
 * ```
 */
export function generateSlug(text: string): string {
  if (!text) return "";
  
  // Convert to lowercase and replace spaces/special characters with hyphens
  let slug = text.toLowerCase().replace(/[^a-zA-Z0-9]+/g, '-');
  
  // Remove leading/trailing hyphens
  slug = slug.replace(/^-+|-+$/g, '');
  
  return slug;
}

// ============================================================================
// DATE/TIME UTILITIES
// Functions for date and time operations
// ============================================================================

/**
 * Format a date as a relative time string
 * 
 * @param date - The date to format
 * @returns A relative time string (e.g., "2 days ago")
 * 
 * @example
 * ```typescript
 * const relativeTime = formatRelativeTime(new Date(Date.now() - 86400000));
 * console.log(relativeTime); // "1 day ago"
 * ```
 */
export function formatRelativeTime(date: Date): string {
  if (!date) return "";
  
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
  const diffMinutes = Math.floor(diffMs / (1000 * 60));
  
  if (diffDays > 0) {
    return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
  } else if (diffHours > 0) {
    return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
  } else if (diffMinutes > 0) {
    return `${diffMinutes} minute${diffMinutes > 1 ? 's' : ''} ago`;
  } else {
    return "Just now";
  }
}

/**
 * Format a date as a readable string
 * 
 * @param date - The date to format
 * @param options - Formatting options
 * @returns A formatted date string
 * 
 * @example
 * ```typescript
 * const formatted = formatDate(new Date());
 * console.log(formatted); // "January 1, 2023"
 * ```
 */
export function formatDate(date: Date, options?: Intl.DateTimeFormatOptions): string {
  if (!date) return "";
  
  const defaultOptions: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  };
  
  return date.toLocaleDateString(undefined, options || defaultOptions);
}

// ============================================================================
// ARRAY UTILITIES
// Functions for array manipulation and processing
// ============================================================================

/**
 * Remove duplicates from an array while preserving order
 * 
 * @param array - The array to remove duplicates from
 * @returns The array with duplicates removed
 * 
 * @example
 * ```typescript
 * const unique = removeDuplicates([1, 2, 2, 3, 3, 4]);
 * console.log(unique); // [1, 2, 3, 4]
 * ```
 */
export function removeDuplicates<T>(array: T[]): T[] {
  if (!array || array.length === 0) return [];
  
  return Array.from(new Set(array));
}

/**
 * Chunk an array into smaller arrays of a specified size
 * 
 * @param array - The array to chunk
 * @param size - The size of each chunk
 * @returns An array of chunked arrays
 * 
 * @example
 * ```typescript
 * const chunks = chunkArray([1, 2, 3, 4, 5], 2);
 * console.log(chunks); // [[1, 2], [3, 4], [5]]
 * ```
 */
export function chunkArray<T>(array: T[], size: number): T[][] {
  if (!array || array.length === 0) return [];
  
  const chunks: T[][] = [];
  for (let i = 0; i < array.length; i += size) {
    chunks.push(array.slice(i, i + size));
  }
  
  return chunks;
}

// ============================================================================
// VALIDATION UTILITIES
// Functions for validating user input
// ============================================================================

/**
 * Validate email format using regex
 * 
 * @param email - The email to validate
 * @returns True if email is valid, false otherwise
 * 
 * @example
 * ```typescript
 * const isValid = validateEmail("user@example.com");
 * console.log(isValid); // true
 * ```
 */
export function validateEmail(email: string): boolean {
  if (!email) return false;
  
  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return pattern.test(email);
}

/**
 * Validate phone number format
 * 
 * @param phone - The phone number to validate
 * @returns True if phone number is valid, false otherwise
 * 
 * @example
 * ```typescript
 * const isValid = validatePhone("123-456-7890");
 * console.log(isValid); // true
 * ```
 */
export function validatePhone(phone: string): boolean {
  if (!phone) return false;
  
  // Remove common separators and check if remaining characters are digits
  const cleaned = phone.replace(/[\s\-\(\)\+]/g, '');
  return /^\d{7,15}$/.test(cleaned);
}

// ============================================================================
// UI UTILITIES
// Functions for UI-related operations
// ============================================================================

/**
 * Merge CSS classes with proper handling of conditional classes
 * 
 * @param inputs - Class values to merge
 * @returns Merged class string
 * 
 * @example
 * ```typescript
 * const className = cn("base-class", isActive && "active", "another-class");
 * console.log(className); // "base-class active another-class"
 * ```
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Generate a random ID
 * 
 * @returns A random ID string
 * 
 * @example
 * ```typescript
 * const id = generateId();
 * console.log(id); // "abc123xyz"
 * ```
 */
export function generateId(): string {
  return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
}