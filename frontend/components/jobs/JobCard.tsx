/**
 * Job Card Component for MyBrand Job Application Platform
 * 
 * This component displays a compact job listing card with essential information
 * including title, company, location, salary, and key tags.
 * 
 * @version 2.0
 * @author MyBrand Team
 */

// ============================================================================
// IMPORT STATEMENTS
// React component and utility imports
// ============================================================================

import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { MapPin, DollarSign, Clock, Bookmark } from 'lucide-react';
import type { Job } from '@/src/api/client';

// ============================================================================
// COMPONENT PROPS INTERFACE
// TypeScript interface for component properties
// ============================================================================

/**
 * Job card component props interface
 * 
 * Defines the properties required to display a job card
 */
interface JobCardProps {
  /** Job data to display in the card */
  job: Job;
}

// ============================================================================
// COMPONENT IMPLEMENTATION
// Main component function with comprehensive documentation
// ============================================================================

/**
 * Job card component for displaying job listings
 * 
 * This component renders a compact job listing card with essential information
 * including job title, company, location, salary, and key tags. It also includes
 * action buttons for applying to the job and saving it for later.
 * 
 * @param props - Component properties
 * @param props.job - Job data to display in the card
 * @returns JSX element representing the job card
 * 
 * @example
 * ```tsx
 * <JobCard job={jobData} />
 * ```
 */
export default function JobCard({ job }: JobCardProps) {
  /**
   * Render the job card component
   * 
   * Returns a card component with job information and action buttons
   */
  return (
    <Card className="hover:shadow-lg transition-shadow h-full" role="article" tabIndex={0}>
      <CardHeader className="pb-3">
        <div className="flex justify-between items-start mb-2">
          <div className="flex-1">
            <h3 className="font-semibold text-lg leading-tight mb-1">{job.title}</h3>
            <p className="text-muted-foreground">{job.company}</p>
          </div>
          <div className="flex gap-2 ml-2">
            {job.isNew && (
              <Badge variant="secondary" className="bg-green-100 text-green-700" aria-label="New job posting">
                NEW
              </Badge>
            )}
            {job.urgent && (
              <Badge variant="destructive" aria-label="Urgent hiring">
                URGENT
              </Badge>
            )}
          </div>
        </div>

        <div className="flex flex-wrap gap-2">
          {job.remote && <Badge variant="outline">Remote</Badge>}
          <Badge variant="outline">{job.type}</Badge>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        <div className="space-y-2 text-sm text-muted-foreground">
          <div className="flex items-center">
            <MapPin className="h-4 w-4 mr-2" aria-hidden="true" />
            <span>{job.location}</span>
          </div>
          {job.salary && (
            <div className="flex items-center">
              <DollarSign className="h-4 w-4 mr-2" aria-hidden="true" />
              <span>{job.salary}</span>
            </div>
          )}
          <div className="flex items-center">
            <Clock className="h-4 w-4 mr-2" aria-hidden="true" />
            <span>{job.posted}</span>
          </div>
        </div>

        <p className="text-sm text-muted-foreground line-clamp-2">
          {job.description}
        </p>

        <div className="flex gap-2 pt-2">
          <Button className="flex-1" aria-label={`Apply to ${job.title} at ${job.company}`}>
            Apply Now
          </Button>
          <Button 
            variant="ghost" 
            size="icon" 
            aria-label={`Save ${job.title} job`}
          >
            <Bookmark className="h-4 w-4" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}