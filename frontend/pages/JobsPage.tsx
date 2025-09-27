/**
 * Jobs Page for MyBrand Job Application Platform
 * 
 * This page provides comprehensive job search functionality with advanced
 * filtering, pagination, and job details viewing capabilities.
 * 
 * @version 2.0
 * @author MyBrand Team
 */

// ============================================================================
// IMPORT STATEMENTS
// React, component, hook, and utility imports
// ============================================================================

import { useState, useEffect, useMemo } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from '@/components/ui/sheet';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Search, MapPin, Filter, X } from 'lucide-react';
import { useJobSearch } from '../hooks/useJobSearch';
import { useDebounce } from '../hooks/useDebounce';
import JobCard from '../components/jobs/JobCard';
import JobDetailsModal from '../components/jobs/JobDetailsModal';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ErrorMessage from '../components/common/ErrorMessage';
import { ErrorBoundary } from '../components/common/ErrorBoundary';
import SEOHead from '../components/seo/SEOHead';
import type { Job } from '@/src/api/client';

// ============================================================================
// PAGE COMPONENT
// Main page component implementation
// ============================================================================

/**
 * Jobs page component for job searching and browsing
 * 
 * This component provides a comprehensive job search interface with:
 * - Search by keyword and location
 * - Advanced filtering options
 * - Pagination and infinite loading
 * - Job details modal
 * - Responsive design for all devices
 * 
 * @returns JSX element representing the jobs page
 * 
 * @example
 * ```tsx
 * <JobsPage />
 * ```
 */
export default function JobsPage() {
  // ============================================================================
  // STATE MANAGEMENT
  // Component state for search parameters, filters, and UI state
  // ============================================================================

  /** Search keyword for job titles, descriptions, and companies */
  const [searchKeyword, setSearchKeyword] = useState('');
  
  /** Search location for job locations */
  const [searchLocation, setSearchLocation] = useState('');
  
  /** Selected job type filter (Full-time, Part-time, etc.) */
  const [selectedJobType, setSelectedJobType] = useState('');
  
  /** Selected experience level filter */
  const [selectedExperience, setSelectedExperience] = useState('');
  
  /** Selected salary range filter */
  const [selectedSalary, setSelectedSalary] = useState('');
  
  /** Selected company filter */
  const [selectedCompany, setSelectedCompany] = useState('');
  
  /** Selected date posted filter */
  const [selectedDatePosted, setSelectedDatePosted] = useState('');
  
  /** Mobile filters panel open state */
  const [isFiltersOpen, setIsFiltersOpen] = useState(false);
  
  /** Currently selected job for detailed view */
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  
  /** Current pagination page */
  const [page, setPage] = useState(0);

  // ============================================================================
  // HOOKS AND DATA FETCHING
  // Custom hooks for search functionality and data management
  // ============================================================================

  /**
   * Debounce search inputs to prevent excessive API calls
   * 
   * Delays the execution of search queries until the user has stopped typing
   * for a specified period, improving performance and user experience.
   */
  const debouncedKeyword = useDebounce(searchKeyword, 500);
  const debouncedLocation = useDebounce(searchLocation, 500);
  const debouncedCompany = useDebounce(selectedCompany, 500);

  /**
   * Reset pagination when search parameters change
   * 
   * Ensures that when users modify search criteria, they see the first page
   * of results for the new search rather than continuing from a previous page.
   */
  useEffect(() => {
    setPage(0);
  }, [debouncedKeyword, debouncedLocation, selectedJobType, selectedExperience, selectedSalary, debouncedCompany, selectedDatePosted]);

  /**
   * Build search parameters for the job search API
   * 
   * Constructs the search parameters object from component state,
   * using debounced values to prevent excessive API calls.
   */
  const searchParams = useMemo(() => ({
    keyword: debouncedKeyword || undefined,
    location: debouncedLocation || undefined,
    jobType: selectedJobType || undefined,
    experience: selectedExperience || undefined,
    salary: selectedSalary || undefined,
    company: debouncedCompany || undefined,
    datePosted: selectedDatePosted || undefined,
    limit: 20,
    offset: page * 20,
  }), [
    debouncedKeyword,
    debouncedLocation,
    selectedJobType,
    selectedExperience,
    selectedSalary,
    debouncedCompany,
    selectedDatePosted,
    page
  ]);

  /**
   * Fetch job search results using the useJobSearch hook
   * 
   * Handles data fetching, loading states, and error handling for job searches.
   */
  const { data, isLoading, error, refetch } = useJobSearch(searchParams);

  // ============================================================================
  // FILTER MANAGEMENT
  // Functions for managing active filters and filter state
  // ============================================================================

  /**
   * Compute active filters for display
   * 
   * Creates an array of currently active filters for display to the user.
   */
  const activeFilters = useMemo(() => {
    const filters = [];
    if (selectedJobType) filters.push({ type: 'jobType', value: selectedJobType, label: selectedJobType });
    if (selectedExperience) filters.push({ type: 'experience', value: selectedExperience, label: selectedExperience });
    if (selectedSalary) filters.push({ type: 'salary', value: selectedSalary, label: selectedSalary });
    if (debouncedCompany) filters.push({ type: 'company', value: debouncedCompany, label: debouncedCompany });
    if (selectedDatePosted) filters.push({ type: 'datePosted', value: selectedDatePosted, label: getDateLabel(selectedDatePosted) });
    return filters;
  }, [selectedJobType, selectedExperience, selectedSalary, debouncedCompany, selectedDatePosted]);

  /**
   * Clear a specific filter by type
   * 
   * Resets the state for a specific filter type to its default value.
   * 
   * @param type - The type of filter to clear
   */
  const clearFilter = (type: string) => {
    switch (type) {
      case 'jobType':
        setSelectedJobType('');
        break;
      case 'experience':
        setSelectedExperience('');
        break;
      case 'salary':
        setSelectedSalary('');
        break;
      case 'company':
        setSelectedCompany('');
        break;
      case 'datePosted':
        setSelectedDatePosted('');
        break;
    }
  };

  /**
   * Clear all active filters
   * 
   * Resets all filter states to their default values.
   */
  const clearAllFilters = () => {
    setSelectedJobType('');
    setSelectedExperience('');
    setSelectedSalary('');
    setSelectedCompany('');
    setSelectedDatePosted('');
  };

  // ============================================================================
  // EVENT HANDLERS
  // Functions for handling user interactions and events
  // ============================================================================

  /**
   * Handle search form submission
   * 
   * Prevents default form submission and resets pagination to first page.
   * 
   * @param e - Form submission event
   */
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(0);
  };

  /**
   * Handle load more button click
   * 
   * Increments the pagination page to load more results.
   */
  const handleLoadMore = () => {
    setPage(prev => prev + 1);
  };

  // ============================================================================
  // UTILITY FUNCTIONS
  // Helper functions for data transformation and formatting
  // ============================================================================

  /**
   * Get human-readable label for date filter values
   * 
   * Converts date filter codes to user-friendly labels.
   * 
   * @param value - Date filter value code
   * @returns Human-readable date label
   */
  function getDateLabel(value: string) {
    switch (value) {
      case '24h': return 'Last 24 hours';
      case '3d': return 'Last 3 days';
      case '7d': return 'Last week';
      case '30d': return 'Last month';
      default: return value;
    }
  }

  // ============================================================================
  // COMPONENT RENDERING
  // Sub-components and rendering functions
  // ============================================================================

  /**
   * Filter content component
   * 
   * Renders the filter options UI for both desktop sidebar and mobile sheet.
   */
  const FilterContent = () => (
    <div className="space-y-6">
      <div>
        <label htmlFor="job-type-filter" className="text-sm font-medium mb-2 block">Job Type</label>
        <Select value={selectedJobType} onValueChange={setSelectedJobType}>
          <SelectTrigger id="job-type-filter">
            <SelectValue placeholder="Select job type" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="Full-time">Full-time</SelectItem>
            <SelectItem value="Part-time">Part-time</SelectItem>
            <SelectItem value="Contract">Contract</SelectItem>
            <SelectItem value="Internship">Internship</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div>
        <label htmlFor="experience-filter" className="text-sm font-medium mb-2 block">Experience Level</label>
        <Select value={selectedExperience} onValueChange={setSelectedExperience}>
          <SelectTrigger id="experience-filter">
            <SelectValue placeholder="Select experience" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="Entry Level">Entry Level</SelectItem>
            <SelectItem value="Mid Level">Mid Level</SelectItem>
            <SelectItem value="Senior Level">Senior Level</SelectItem>
            <SelectItem value="Executive">Executive</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div>
        <label htmlFor="salary-filter" className="text-sm font-medium mb-2 block">Salary Range</label>
        <Select value={selectedSalary} onValueChange={setSelectedSalary}>
          <SelectTrigger id="salary-filter">
            <SelectValue placeholder="Select salary range" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="0-50k">$0 - $50k</SelectItem>
            <SelectItem value="50k-100k">$50k - $100k</SelectItem>
            <SelectItem value="100k-150k">$100k - $150k</SelectItem>
            <SelectItem value="150k+">$150k+</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div>
        <label htmlFor="company-filter" className="text-sm font-medium mb-2 block">Company</label>
        <Input
          id="company-filter"
          placeholder="Enter company name"
          value={selectedCompany}
          onChange={(e) => setSelectedCompany(e.target.value)}
        />
      </div>

      <div>
        <label htmlFor="date-filter" className="text-sm font-medium mb-2 block">Date Posted</label>
        <Select value={selectedDatePosted} onValueChange={setSelectedDatePosted}>
          <SelectTrigger id="date-filter">
            <SelectValue placeholder="Select date range" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="24h">Last 24 hours</SelectItem>
            <SelectItem value="3d">Last 3 days</SelectItem>
            <SelectItem value="7d">Last week</SelectItem>
            <SelectItem value="30d">Last month</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {activeFilters.length > 0 && (
        <Button variant="outline" onClick={clearAllFilters} className="w-full">
          Clear All Filters
        </Button>
      )}
    </div>
  );

  // ============================================================================
  // MAIN RENDER
  // Primary component render function
  // ============================================================================

  /**
   * Render the jobs page
   * 
   * Returns the complete jobs page UI with search, filters, results, and modals.
   */
  return (
    <ErrorBoundary>
      <SEOHead
        title="Job Search - Find Your Dream Job"
        description="Search thousands of job opportunities with intelligent filters and real-time results. Find remote work, full-time positions, and more."
        keywords="job search, find jobs, career opportunities, remote work, hiring"
      />
      
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search Section */}
        <section className="mb-8" aria-label="Job search">
          <form onSubmit={handleSearch} className="max-w-4xl mx-auto" role="search">
            <div className="flex flex-col lg:flex-row gap-4 p-2 bg-background rounded-lg shadow-lg border">
              <div className="flex-1 relative">
                <label htmlFor="job-keyword" className="sr-only">Job title, keywords, or company</label>
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-muted-foreground" aria-hidden="true" />
                <Input
                  id="job-keyword"
                  type="text"
                  placeholder="Job title, keywords, or company"
                  value={searchKeyword}
                  onChange={(e) => setSearchKeyword(e.target.value)}
                  className="pl-10 border-0 focus-visible:ring-0 h-12"
                />
              </div>
              <div className="flex-1 relative">
                <label htmlFor="job-location" className="sr-only">City, state, or remote</label>
                <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-muted-foreground" aria-hidden="true" />
                <Input
                  id="job-location"
                  type="text"
                  placeholder="City, state, or remote"
                  value={searchLocation}
                  onChange={(e) => setSearchLocation(e.target.value)}
                  className="pl-10 border-0 focus-visible:ring-0 h-12"
                />
              </div>
              <Button type="submit" size="lg" className="px-8 h-12">
                Search Jobs
              </Button>
            </div>
          </form>
        </section>

        <div className="flex flex-col lg:flex-row gap-8">
          {/* Desktop Filters Sidebar */}
          <aside className="hidden lg:block w-80 shrink-0" aria-label="Job filters">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Filter className="h-5 w-5 mr-2" aria-hidden="true" />
                  Filters
                </CardTitle>
              </CardHeader>
              <CardContent>
                <FilterContent />
              </CardContent>
            </Card>
          </aside>

          {/* Main Content */}
          <div className="flex-1">
            {/* Mobile Filter Button & Active Filters */}
            <div className="lg:hidden mb-6">
              <Sheet open={isFiltersOpen} onOpenChange={setIsFiltersOpen}>
                <SheetTrigger asChild>
                  <Button variant="outline" className="w-full">
                    <Filter className="h-4 w-4 mr-2" />
                    Filters {activeFilters.length > 0 && `(${activeFilters.length})`}
                  </Button>
                </SheetTrigger>
                <SheetContent side="right" className="w-[300px] sm:w-[400px]">
                  <SheetHeader>
                    <SheetTitle>Filters</SheetTitle>
                  </SheetHeader>
                  <div className="mt-6">
                    <FilterContent />
                  </div>
                </SheetContent>
              </Sheet>
            </div>

            {/* Active Filters */}
            {activeFilters.length > 0 && (
              <div className="mb-6" role="region" aria-label="Active filters">
                <div className="flex flex-wrap gap-2">
                  {activeFilters.map((filter, index) => (
                    <Badge key={index} variant="secondary" className="pr-1">
                      {filter.label}
                      <button
                        onClick={() => clearFilter(filter.type)}
                        className="ml-2 hover:bg-muted-foreground/20 rounded-full p-0.5"
                        aria-label={`Remove ${filter.label} filter`}
                      >
                        <X className="h-3 w-3" />
                      </button>
                    </Badge>
                  ))}
                  <Button variant="ghost" size="sm" onClick={clearAllFilters}>
                    Clear all
                  </Button>
                </div>
              </div>
            )}

            {/* Error State */}
            {error && (
              <ErrorMessage
                title="Failed to load jobs"
                message={error.message}
                onRetry={() => refetch()}
                className="mb-6"
              />
            )}

            {/* Loading State */}
            {isLoading && page === 0 && (
              <div className="flex justify-center py-12">
                <LoadingSpinner size="lg" text="Searching jobs..." />
              </div>
            )}

            {/* Results */}
            {data && (
              <>
                {/* Results Header */}
                <div className="mb-6">
                  <h1 className="text-2xl font-bold mb-2">Job Search Results</h1>
                  <p className="text-muted-foreground">
                    Showing {data.jobs.length} of {data.total} jobs
                  </p>
                </div>

                {/* Job Grid */}
                {data.jobs.length > 0 ? (
                  <>
                    <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-6 mb-8">
                      {data.jobs.map((job) => (
                        <div 
                          key={job.id} 
                          onClick={() => setSelectedJob(job)} 
                          className="cursor-pointer"
                          onKeyDown={(e) => {
                            if (e.key === 'Enter' || e.key === ' ') {
                              e.preventDefault();
                              setSelectedJob(job);
                            }
                          }}
                        >
                          <JobCard job={job} />
                        </div>
                      ))}
                    </div>

                    {/* Load More */}
                    {data.hasMore && (
                      <div className="text-center">
                        <Button 
                          onClick={handleLoadMore} 
                          size="lg" 
                          variant="outline"
                          disabled={isLoading}
                        >
                          {isLoading ? <LoadingSpinner size="sm" /> : 'Load More Jobs'}
                        </Button>
                      </div>
                    )}
                  </>
                ) : (
                  <div className="text-center py-12">
                    <h2 className="text-xl font-semibold mb-2">No jobs found</h2>
                    <p className="text-muted-foreground mb-4">
                      Try adjusting your search criteria or filters
                    </p>
                    <Button onClick={clearAllFilters} variant="outline">
                      Clear All Filters
                    </Button>
                  </div>
                )}
              </>
            )}
          </div>
        </div>

        {/* Job Details Modal */}
        {selectedJob && (
          <JobDetailsModal
            job={selectedJob}
            isOpen={!!selectedJob}
            onClose={() => setSelectedJob(null)}
          />
        )}
      </main>
    </ErrorBoundary>
  );
}