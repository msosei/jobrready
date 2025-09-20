import { useQuery } from '@tanstack/react-query';
import backend from '~backend/client';
import type { Job } from '~backend/jobs/search';

export function useJob(id: number) {
  return useQuery<Job, Error>({
    queryKey: ['jobs', id],
    queryFn: () => backend.jobs.get({ id }),
    staleTime: 10 * 60 * 1000, // 10 minutes
    gcTime: 15 * 60 * 1000, // 15 minutes
    retry: 3,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  });
}
