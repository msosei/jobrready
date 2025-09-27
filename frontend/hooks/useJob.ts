/**
 * Job Detail Hook for MyBrand Job Application Platform
 * 
 * This hook provides a React Query powered job detail functionality
 * with caching and error handling.
 * 
 * @version 2.0
 * @author MyBrand Team
 */

// ============================================================================
// IMPORT STATEMENTS
// External and internal dependencies
// ============================================================================

import { useQuery } from '@tanstack/react-query';
import { type Job } from '@/src/api/client';

// ============================================================================
// HOOK IMPLEMENTATION
// Main hook function with comprehensive documentation
// ============================================================================

/**
 * Custom React hook for fetching a specific job by ID
 * 
 * This hook provides job detail functionality with automatic caching,
 * background updates, and error handling through React Query. Since
 * there's no specific backend endpoint for single job retrieval, it
 * fetches all jobs and filters for the requested job.
 * 
 * @param id - The unique identifier of the job to fetch
 * @returns React Query query result object with job data
 * 
 * @example
 * ```typescript
 * const { data: job, isLoading, error } = useJob(123);
 * 
 * if (isLoading) return <div>Loading job...</div>;
 * if (error) return <div>Error: {error.message}</div>;
 * if (!job) return <div>Job not found</div>;
 * 
 * return (
 *   <div>
 *     <h1>{job.title}</h1>
 *     <p>{job.description}</p>
 *   </div>
 * );
 * ```
 */
export function useJob(id: number) {
  /**
   * React Query configuration for job detail fetching
   * 
   * Configures caching, retry behavior, and other React Query options
   * for optimal performance and user experience when fetching job details.
   */
  return useQuery<Job, Error>({
    queryKey: ['jobs', id],
    queryFn: async () => {
      // This is a simplified implementation - in a real app, you'd have a specific endpoint for getting a single job
      const response = await fetch(`http://localhost:8000/jobs/search`);
      if (!response.ok) {
        throw new Error('Failed to fetch job');
      }
      const data = await response.json();
      const job = data.jobs.find((j: Job) => j.id === id);
      if (!job) {
        throw new Error('Job not found');
      }
      return job;
    },
    staleTime: 10 * 60 * 1000, // 10 minutes
    gcTime: 15 * 60 * 1000, // 15 minutes
    retry: 3,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  });
}