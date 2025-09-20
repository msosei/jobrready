import { useQuery } from '@tanstack/react-query';
import { useMemo } from 'react';
import backend from '~backend/client';
import type { JobSearchRequest, JobSearchResponse } from '~backend/jobs/search';

export function useJobSearch(params: JobSearchRequest) {
  const queryKey = ['jobs', 'search', params];
  
  // Create a stable query params object
  const stableParams = useMemo(() => {
    const cleanParams: JobSearchRequest = {};
    
    if (params.keyword?.trim()) cleanParams.keyword = params.keyword.trim();
    if (params.location?.trim()) cleanParams.location = params.location.trim();
    if (params.jobType) cleanParams.jobType = params.jobType;
    if (params.experience) cleanParams.experience = params.experience;
    if (params.salary) cleanParams.salary = params.salary;
    if (params.company?.trim()) cleanParams.company = params.company.trim();
    if (params.datePosted) cleanParams.datePosted = params.datePosted;
    if (params.remote !== undefined) cleanParams.remote = params.remote;
    if (params.limit) cleanParams.limit = params.limit;
    if (params.offset) cleanParams.offset = params.offset;
    
    return cleanParams;
  }, [params]);

  return useQuery<JobSearchResponse, Error>({
    queryKey: ['jobs', 'search', stableParams],
    queryFn: () => backend.jobs.search(stableParams),
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 10 * 60 * 1000, // 10 minutes
    retry: 3,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  });
}
