import { useMemo } from 'react';
import { FixedSizeList as List } from 'react-window';
import type { Job } from '@/src/api/client';
import JobCard from './JobCard';

interface VirtualJobListProps {
  jobs: Job[];
  onJobClick: (job: Job) => void;
  height: number;
  itemHeight?: number;
}

export default function VirtualJobList({ 
  jobs, 
  onJobClick, 
  height, 
  itemHeight = 300 
}: VirtualJobListProps) {
  const Row = useMemo(() => {
    return ({ index, style }: { index: number; style: React.CSSProperties }) => {
      const job = jobs[index];
      if (!job) return null;

      return (
        <div style={style} className="p-3">
          <div onClick={() => onJobClick(job)} className="cursor-pointer">
            <JobCard job={job} />
          </div>
        </div>
      );
    };
  }, [jobs, onJobClick]);

  if (jobs.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-muted-foreground">No jobs found</p>
      </div>
    );
  }

  return (
    <List
      height={height}
      width="100%"
      itemCount={jobs.length}
      itemSize={itemHeight}
      itemData={jobs}
      aria-label="Job listings"
    >
      {Row}
    </List>
  );
}
