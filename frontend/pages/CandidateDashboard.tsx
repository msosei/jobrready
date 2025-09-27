/**
 * Candidate Dashboard Page for MyBrand Job Application Platform
 * 
 * This page provides a comprehensive dashboard for job candidates to manage
 * their job search, track applications, save jobs, and update their profile.
 * 
 * @version 2.0
 * @author MyBrand Team
 */

// ============================================================================
// IMPORT STATEMENTS
// React component and utility imports
// ============================================================================

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { User, FileText, Bookmark, Clock, CheckCircle, XCircle, Upload } from 'lucide-react';
import JobCard from '../components/jobs/JobCard';
import { ErrorBoundary } from '../components/common/ErrorBoundary';
import SEOHead from '../components/seo/SEOHead';
import type { Job } from '@/src/api/client';

// ============================================================================
// DATA INTERFACES
// TypeScript interfaces for data structures
// ============================================================================

/**
 * Saved job data interface
 * 
 * Represents a job that has been saved by the user
 */
interface SavedJob {
  /** Unique identifier for the job */
  id: string;
  
  /** Job title */
  title: string;
  
  /** Company name */
  company: string;
  
  /** Job location */
  location: string;
  
  /** Salary range */
  salary: string;
  
  /** Employment type */
  type: string;
  
  /** Whether the job offers remote work */
  remote: boolean;
  
  /** Whether the job is marked as urgent */
  urgent: boolean;
  
  /** When the job was posted */
  posted: string;
  
  /** Whether the job is newly posted */
  isNew: boolean;
  
  /** Job description */
  description: string;
}

/**
 * Job application data interface
 * 
 * Represents a job application submitted by the user
 */
interface JobApplication {
  /** Unique identifier for the application */
  id: string;
  
  /** Job title */
  job: string;
  
  /** Company name */
  company: string;
  
  /** Date when the application was submitted */
  appliedDate: string;
  
  /** Current status of the application */
  status: string;
  
  /** Type of status for styling purposes */
  statusType: 'pending' | 'interview' | 'offer' | 'rejected';
}

// ============================================================================
// PAGE COMPONENT
// Main page component implementation
// ============================================================================

/**
 * Candidate dashboard page component for job search management
 * 
 * This component provides a comprehensive dashboard for job candidates with
 * multiple tabs for overview, saved jobs, applications, and profile management.
 * It displays key metrics, recent activity, and tools for managing the job search.
 * 
 * @returns JSX element representing the candidate dashboard page
 * 
 * @example
 * ```tsx
 * <CandidateDashboard />
 * ```
 */
export default function CandidateDashboard() {
  // ============================================================================
  // STATE MANAGEMENT
  // Component state for active tab and UI state
  // ============================================================================

  /** Currently active tab in the dashboard */
  const [activeTab, setActiveTab] = useState('overview');

  // ============================================================================
  // MOCK DATA
  // Sample data for demonstration purposes
  // ============================================================================

  /** Sample saved jobs data */
  const savedJobs: SavedJob[] = [
    {
      id: '1',
      title: 'Senior Software Engineer',
      company: 'TechCorp Inc.',
      location: 'San Francisco, CA',
      salary: '$120k - $160k',
      type: 'Full-time',
      remote: true,
      urgent: false,
      posted: '2 days ago',
      isNew: true,
      description: 'Join our team to build scalable web applications...',
    },
    {
      id: '2',
      title: 'Product Manager',
      company: 'InnovateCo',
      location: 'Remote',
      salary: '$130k - $170k',
      type: 'Full-time',
      remote: true,
      urgent: true,
      posted: '5 days ago',
      isNew: false,
      description: 'Lead product strategy and development...',
    },
  ];

  /** Sample job applications data */
  const applications: JobApplication[] = [
    {
      id: '1',
      job: 'Senior Frontend Developer',
      company: 'WebTech Solutions',
      appliedDate: '2024-01-15',
      status: 'Under Review',
      statusType: 'pending',
    },
    {
      id: '2',
      job: 'React Developer',
      company: 'StartupCo',
      appliedDate: '2024-01-10',
      status: 'Interview Scheduled',
      statusType: 'interview',
    },
    {
      id: '3',
      job: 'Full Stack Engineer',
      company: 'TechGiant',
      appliedDate: '2024-01-05',
      status: 'Rejected',
      statusType: 'rejected',
    },
    {
      id: '4',
      job: 'Software Engineer',
      company: 'CloudCorp',
      appliedDate: '2023-12-28',
      status: 'Offer Extended',
      statusType: 'offer',
    },
  ];

  // ============================================================================
  // UTILITY FUNCTIONS
  // Helper functions for data transformation and formatting
  // ============================================================================

  /**
   * Convert saved job to API job format
   * 
   * Converts a saved job with string ID to the API job format with number ID
   * 
   * @param savedJob - The saved job to convert
   * @returns The converted API job
   */
  const convertToApiJob = (savedJob: SavedJob): Job => {
    return {
      ...savedJob,
      id: parseInt(savedJob.id, 10) || 0
    };
  };

  /**
   * Get appropriate icon for application status
   * 
   * Returns an icon component based on the application status type
   * 
   * @param statusType - The type of application status
   * @returns JSX element representing the status icon
   */
  const getStatusIcon = (statusType: string) => {
    switch (statusType) {
      case 'pending':
        return <Clock className="h-4 w-4 text-yellow-600" />;
      case 'interview':
        return <User className="h-4 w-4 text-blue-600" />;
      case 'offer':
        return <CheckCircle className="h-4 w-4 text-green-600" />;
      case 'rejected':
        return <XCircle className="h-4 w-4 text-red-600" />;
      default:
        return <Clock className="h-4 w-4 text-gray-600" />;
    }
  };

  /**
   * Get appropriate badge for application status
   * 
   * Returns a badge component with appropriate styling based on the application status type
   * 
   * @param statusType - The type of application status
   * @param status - The status text to display
   * @returns JSX element representing the status badge
   */
  const getStatusBadge = (statusType: string, status: string) => {
    const variants: { [key: string]: "default" | "secondary" | "destructive" | "outline" } = {
      pending: 'outline',
      interview: 'default',
      offer: 'secondary',
      rejected: 'destructive',
    };
    return <Badge variant={variants[statusType] || 'outline'}>{status}</Badge>;
  };

  // ============================================================================
  // MAIN RENDER
  // Primary component render function
  // ============================================================================

  /**
   * Render the candidate dashboard page
   * 
   * Returns the complete dashboard UI with tabs, metrics, and management tools
   */
  return (
    <ErrorBoundary>
      <SEOHead
        title="Candidate Dashboard - Manage Your Job Search"
        description="Track your job applications, save jobs, and manage your profile from your personalized dashboard."
        keywords="candidate dashboard, job applications, saved jobs, profile management"
      />
      
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Candidate Dashboard</h1>
          <p className="text-muted-foreground">
            Manage your job search, track applications, and update your profile
          </p>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-8">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="saved">Saved Jobs</TabsTrigger>
            <TabsTrigger value="applications">Applications</TabsTrigger>
            <TabsTrigger value="profile">Profile</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Applications</CardTitle>
                  <FileText className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{applications.length}</div>
                  <p className="text-xs text-muted-foreground">
                    +2 from last month
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Saved Jobs</CardTitle>
                  <Bookmark className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{savedJobs.length}</div>
                  <p className="text-xs text-muted-foreground">
                    Jobs you're interested in
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Interview Rate</CardTitle>
                  <User className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">25%</div>
                  <p className="text-xs text-muted-foreground">
                    Above average
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Profile Strength</CardTitle>
                  <CheckCircle className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">85%</div>
                  <Progress value={85} className="mt-2" />
                </CardContent>
              </Card>
            </div>

            <div className="grid lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Recent Applications</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {applications.slice(0, 3).map((app) => (
                      <div key={app.id} className="flex items-center justify-between p-3 border rounded-lg">
                        <div>
                          <h4 className="font-medium">{app.job}</h4>
                          <p className="text-sm text-muted-foreground">{app.company}</p>
                        </div>
                        <div className="flex items-center gap-2">
                          {getStatusIcon(app.statusType)}
                          {getStatusBadge(app.statusType, app.status)}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Recommended Actions</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="p-3 bg-blue-50 dark:bg-blue-950/20 rounded-lg">
                      <h4 className="font-medium text-blue-900 dark:text-blue-100">
                        Update Your Resume
                      </h4>
                      <p className="text-sm text-blue-700 dark:text-blue-300">
                        Your resume hasn't been updated in 2 months
                      </p>
                    </div>
                    <div className="p-3 bg-green-50 dark:bg-green-950/20 rounded-lg">
                      <h4 className="font-medium text-green-900 dark:text-green-100">
                        Complete Skills Assessment
                      </h4>
                      <p className="text-sm text-green-700 dark:text-green-300">
                        Boost your profile visibility
                      </p>
                    </div>
                    <div className="p-3 bg-orange-50 dark:bg-orange-950/20 rounded-lg">
                      <h4 className="font-medium text-orange-900 dark:text-orange-100">
                        Follow Up on Applications
                      </h4>
                      <p className="text-sm text-orange-700 dark:text-orange-300">
                        2 applications pending follow-up
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="saved" className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold">Saved Jobs</h2>
              <p className="text-muted-foreground">{savedJobs.length} jobs saved</p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {savedJobs.map((job) => (
                <JobCard key={job.id} job={convertToApiJob(job)} />
              ))}
            </div>
          </TabsContent>

          <TabsContent value="applications" className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold">Application History</h2>
              <p className="text-muted-foreground">{applications.length} applications</p>
            </div>

            <div className="space-y-4">
              {applications.map((app) => (
                <Card key={app.id}>
                  <CardContent className="p-6">
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="text-lg font-semibold mb-1">{app.job}</h3>
                        <p className="text-muted-foreground mb-2">{app.company}</p>
                        <p className="text-sm text-muted-foreground">
                          Applied on {new Date(app.appliedDate).toLocaleDateString()}
                        </p>
                      </div>
                      <div className="flex items-center gap-2">
                        {getStatusIcon(app.statusType)}
                        {getStatusBadge(app.statusType, app.status)}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="profile" className="space-y-6">
            <div className="grid lg:grid-cols-2 gap-8">
              <Card>
                <CardHeader>
                  <CardTitle>Personal Information</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-sm font-medium mb-2 block">First Name</label>
                      <Input defaultValue="John" />
                    </div>
                    <div>
                      <label className="text-sm font-medium mb-2 block">Last Name</label>
                      <Input defaultValue="Doe" />
                    </div>
                  </div>
                  <div>
                    <label className="text-sm font-medium mb-2 block">Email</label>
                    <Input type="email" defaultValue="john.doe@example.com" />
                  </div>
                  <div>
                    <label className="text-sm font-medium mb-2 block">Phone</label>
                    <Input type="tel" defaultValue="+1 (555) 123-4567" />
                  </div>
                  <div>
                    <label className="text-sm font-medium mb-2 block">Location</label>
                    <Input defaultValue="San Francisco, CA" />
                  </div>
                  <Button>Update Profile</Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Resume & Documents</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-6 text-center">
                    <Upload className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                    <h3 className="text-lg font-medium mb-2">Upload Resume</h3>
                    <p className="text-sm text-muted-foreground mb-4">
                      PDF, DOC, or DOCX up to 5MB
                    </p>
                    <Button>Choose File</Button>
                  </div>

                  <div>
                    <label className="text-sm font-medium mb-2 block">Professional Summary</label>
                    <Textarea
                      placeholder="Write a brief summary of your professional experience..."
                      rows={4}
                      defaultValue="Experienced software engineer with 5+ years in full-stack development..."
                    />
                  </div>

                  <div>
                    <label className="text-sm font-medium mb-2 block">Skills</label>
                    <Input
                      placeholder="e.g., JavaScript, React, Node.js, Python..."
                      defaultValue="JavaScript, React, Node.js, Python, AWS, Docker"
                    />
                  </div>

                  <Button>Save Changes</Button>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </main>
    </ErrorBoundary>
  );
}