/**
 * Job Search Hook for MyBrand Job Application Platform
 * 
 * This hook provides a React Query powered job search functionality
 * with caching, pagination, and error handling.
 * 
 * @version 2.0
 * @author MyBrand Team
 */

// ============================================================================
// IMPORT STATEMENTS
// External and internal dependencies
// ============================================================================

import { useQuery } from '@tanstack/react-query';
import { useMemo } from 'react';
import { searchJobs, type JobSearchRequest, type JobSearchResponse } from '@/src/api/client';

// ============================================================================
// HOOK IMPLEMENTATION
// Main hook function with comprehensive documentation
// ============================================================================

/**
 * Custom React hook for job searching with React Query integration
 * 
 * This hook provides job search functionality with automatic caching,
 * background updates, and error handling through React Query. It also
 * sanitizes and optimizes search parameters for better performance.
 * 
 * @param params - Job search parameters for filtering results
 * @returns React Query query result object with job search data
 * 
 * @example
 * ```typescript
 * const { data, isLoading, error } = useJobSearch({
 *   keyword: 'software engineer',
 *   location: 'San Francisco',
 *   remote: true,
 *   limit: 20
 * });
 * 
 * if (isLoading) return <div>Loading jobs...</div>;
 * if (error) return <div>Error: {error.message}</div>;
 * 
 * return (
 *   <div>
 *     {data?.jobs.map(job => (
 *       <JobCard key={job.id} job={job} />
 *     ))}
 *   </div>
 * );
 * ```
 */
export function useJobSearch(params: JobSearchRequest) {
  // Create a stable query key for React Query caching
  const queryKey = ['jobs', 'search', params];
  
  /**
   * Create a stable query params object
   * 
   * This useMemo hook ensures that the query parameters object
   * is only recreated when the actual values change, preventing
   * unnecessary re-renders and API calls.
   */
  const stableParams = useMemo(() => {
    // Initialize clean parameters object
    const cleanParams: JobSearchRequest = {};
    
    // Only include parameters that have meaningful values
    if (params.keyword?.trim()) cleanParams.keyword = params.keyword.trim();
    if (params.location?.trim()) cleanParams.location = params.location.trim();
    if (params.jobType) cleanParams.jobType = params.jobType;
    if (params.company?.trim()) cleanParams.company = params.company.trim();
    if (params.remote !== undefined) cleanParams.remote = params.remote;
    if (params.limit) cleanParams.limit = params.limit;
    if (params.offset) cleanParams.offset = params.offset;
    
    return cleanParams;
  }, [params]);

  /**
   * React Query configuration for job search
   * 
   * Configures caching, retry behavior, and other React Query options
   * for optimal performance and user experience.
   */
  return useQuery<JobSearchResponse, Error>({
    queryKey: ['jobs', 'search', stableParams],
    queryFn: () => searchJobs(stableParams),
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 10 * 60 * 1000, // 10 minutes
    retry: 3,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  });
}