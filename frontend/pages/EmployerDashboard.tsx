/**
 * Employer Dashboard Page for MyBrand Job Application Platform
 * 
 * This page provides a comprehensive dashboard for employers to manage
 * job postings, track applicants, and post new job opportunities.
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
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Plus, Users, Briefcase, Eye, MoreVertical, FileText, Download, Mail } from 'lucide-react';
import { ErrorBoundary } from '../components/common/ErrorBoundary';
import SEOHead from '../components/seo/SEOHead';

// ============================================================================
// DATA INTERFACES
// TypeScript interfaces for data structures
// ============================================================================

/**
 * Job posting data interface
 * 
 * Represents a job posting created by an employer
 */
interface JobPosting {
  /** Unique identifier for the job posting */
  id: string;
  
  /** Job title */
  title: string;
  
  /** Current status of the job posting */
  status: string;
  
  /** Number of applicants */
  applicants: number;
  
  /** Number of views */
  views: number;
  
  /** Date when the job was posted */
  posted: string;
  
  /** Date when the job posting expires */
  expires: string;
}

/**
 * Job applicant data interface
 * 
 * Represents a candidate who has applied to a job posting
 */
interface Applicant {
  /** Unique identifier for the applicant */
  id: string;
  
  /** Applicant's name */
  name: string;
  
  /** Position applied for */
  position: string;
  
  /** Date when the application was submitted */
  appliedDate: string;
  
  /** Current status of the application */
  status: string;
  
  /** Years of experience */
  experience: string;
  
  /** Applicant's location */
  location: string;
  
  /** Resume file name */
  resume: string;
}

// ============================================================================
// PAGE COMPONENT
// Main page component implementation
// ============================================================================

/**
 * Employer dashboard page component for job posting management
 * 
 * This component provides a comprehensive dashboard for employers with
 * multiple tabs for overview, job postings, and applicant tracking.
 * It includes tools for posting new jobs and managing existing postings.
 * 
 * @returns JSX element representing the employer dashboard page
 * 
 * @example
 * ```tsx
 * <EmployerDashboard />
 * ```
 */
export default function EmployerDashboard() {
  // ============================================================================
  // STATE MANAGEMENT
  // Component state for active tab and UI state
  // ============================================================================

  /** Currently active tab in the dashboard */
  const [activeTab, setActiveTab] = useState('overview');
  
  /** Whether the post job dialog is open */
  const [isPostJobOpen, setIsPostJobOpen] = useState(false);

  // ============================================================================
  // MOCK DATA
  // Sample data for demonstration purposes
  // ============================================================================

  /** Sample job postings data */
  const jobPostings: JobPosting[] = [
    {
      id: '1',
      title: 'Senior Software Engineer',
      status: 'Active',
      applicants: 45,
      views: 1250,
      posted: '2024-01-15',
      expires: '2024-02-15',
    },
    {
      id: '2',
      title: 'Product Manager',
      status: 'Active',
      applicants: 32,
      views: 890,
      posted: '2024-01-10',
      expires: '2024-02-10',
    },
    {
      id: '3',
      title: 'UX Designer',
      status: 'Closed',
      applicants: 67,
      views: 1540,
      posted: '2023-12-20',
      expires: '2024-01-20',
    },
  ];

  /** Sample applicants data */
  const applicants: Applicant[] = [
    {
      id: '1',
      name: 'John Smith',
      position: 'Senior Software Engineer',
      appliedDate: '2024-01-18',
      status: 'Under Review',
      experience: '5+ years',
      location: 'San Francisco, CA',
      resume: 'john_smith_resume.pdf',
    },
    {
      id: '2',
      name: 'Sarah Johnson',
      position: 'Senior Software Engineer',
      appliedDate: '2024-01-17',
      status: 'Interview Scheduled',
      experience: '7+ years',
      location: 'Remote',
      resume: 'sarah_johnson_resume.pdf',
    },
    {
      id: '3',
      name: 'Mike Chen',
      position: 'Product Manager',
      appliedDate: '2024-01-16',
      status: 'Shortlisted',
      experience: '4+ years',
      location: 'New York, NY',
      resume: 'mike_chen_resume.pdf',
    },
  ];

  // ============================================================================
  // UTILITY FUNCTIONS
  // Helper functions for data transformation and formatting
  // ============================================================================

  /**
   * Get appropriate badge for status
   * 
   * Returns a badge component with appropriate styling based on the status
   * 
   * @param status - The status text to display
   * @returns JSX element representing the status badge
   */
  const getStatusBadge = (status: string) => {
    const variants: { [key: string]: "default" | "secondary" | "destructive" | "outline" } = {
      Active: 'default',
      Closed: 'secondary',
      'Under Review': 'outline',
      'Interview Scheduled': 'default',
      Shortlisted: 'secondary',
    };
    return <Badge variant={variants[status] || 'outline'}>{status}</Badge>;
  };

  // ============================================================================
  // MAIN RENDER
  // Primary component render function
  // ============================================================================

  /**
   * Render the employer dashboard page
   * 
   * Returns the complete dashboard UI with tabs, metrics, and management tools
   */
  return (
    <ErrorBoundary>
      <SEOHead
        title="Employer Dashboard - Manage Job Postings"
        description="Post new jobs, track applicants, and manage your company's job listings from your personalized dashboard."
        keywords="employer dashboard, job postings, applicant tracking, hire candidates"
      />
      
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold mb-2">Employer Dashboard</h1>
            <p className="text-muted-foreground">
              Manage your job postings and track applicants
            </p>
          </div>
          <Dialog open={isPostJobOpen} onOpenChange={setIsPostJobOpen}>
            <DialogTrigger asChild>
              <Button className="flex items-center">
                <Plus className="h-4 w-4 mr-2" />
                Post New Job
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle>Post a New Job</DialogTitle>
              </DialogHeader>
              <div className="space-y-6 mt-6">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium mb-2 block">Job Title</label>
                    <Input placeholder="e.g., Senior Software Engineer" />
                  </div>
                  <div>
                    <label className="text-sm font-medium mb-2 block">Department</label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Select department" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="engineering">Engineering</SelectItem>
                        <SelectItem value="product">Product</SelectItem>
                        <SelectItem value="design">Design</SelectItem>
                        <SelectItem value="marketing">Marketing</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium mb-2 block">Job Type</label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Select job type" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="full-time">Full-time</SelectItem>
                        <SelectItem value="part-time">Part-time</SelectItem>
                        <SelectItem value="contract">Contract</SelectItem>
                        <SelectItem value="internship">Internship</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <label className="text-sm font-medium mb-2 block">Experience Level</label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Select experience level" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="entry">Entry Level</SelectItem>
                        <SelectItem value="mid">Mid Level</SelectItem>
                        <SelectItem value="senior">Senior Level</SelectItem>
                        <SelectItem value="executive">Executive</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium mb-2 block">Location</label>
                    <Input placeholder="e.g., San Francisco, CA or Remote" />
                  </div>
                  <div>
                    <label className="text-sm font-medium mb-2 block">Salary Range</label>
                    <Input placeholder="e.g., $120k - $160k" />
                  </div>
                </div>

                <div>
                  <label className="text-sm font-medium mb-2 block">Job Description</label>
                  <Textarea
                    placeholder="Describe the role, responsibilities, and what you're looking for..."
                    rows={6}
                  />
                </div>

                <div>
                  <label className="text-sm font-medium mb-2 block">Requirements</label>
                  <Textarea
                    placeholder="List the required skills, experience, and qualifications..."
                    rows={4}
                  />
                </div>

                <div className="flex justify-end gap-3">
                  <Button variant="outline" onClick={() => setIsPostJobOpen(false)}>
                    Cancel
                  </Button>
                  <Button onClick={() => setIsPostJobOpen(false)}>
                    Post Job
                  </Button>
                </div>
              </div>
            </DialogContent>
          </Dialog>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-8">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="postings">Job Postings</TabsTrigger>
            <TabsTrigger value="applicants">Applicants</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Postings</CardTitle>
                  <Briefcase className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{jobPostings.length}</div>
                  <p className="text-xs text-muted-foreground">
                    2 active this month
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Applicants</CardTitle>
                  <Users className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    {applicants.length}
                  </div>
                  <p className="text-xs text-muted-foreground">
                    +12 from last week
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Avg. Applications</CardTitle>
                  <FileText className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    {Math.round(jobPostings.reduce((sum, job) => sum + job.applicants, 0) / jobPostings.length)}
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Per job posting
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Views</CardTitle>
                  <Eye className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    {jobPostings.reduce((sum, job) => sum + job.views, 0).toLocaleString()}
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Across all postings
                  </p>
                </CardContent>
              </Card>
            </div>

            <div className="grid lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Recent Job Postings</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {jobPostings.slice(0, 3).map((job) => (
                      <div key={job.id} className="flex items-center justify-between p-3 border rounded-lg">
                        <div>
                          <h4 className="font-medium">{job.title}</h4>
                          <p className="text-sm text-muted-foreground">
                            {job.applicants} applicants • {job.views} views
                          </p>
                        </div>
                        <div className="flex items-center gap-2">
                          {getStatusBadge(job.status)}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Recent Applicants</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {applicants.slice(0, 3).map((applicant) => (
                      <div key={applicant.id} className="flex items-center justify-between p-3 border rounded-lg">
                        <div>
                          <h4 className="font-medium">{applicant.name}</h4>
                          <p className="text-sm text-muted-foreground">
                            {applicant.position}
                          </p>
                        </div>
                        <div className="flex items-center gap-2">
                          {getStatusBadge(applicant.status)}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="postings" className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold">Job Postings</h2>
              <p className="text-muted-foreground">{jobPostings.length} total postings</p>
            </div>

            <div className="space-y-4">
              {jobPostings.map((job) => (
                <Card key={job.id}>
                  <CardContent className="p-6">
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="text-lg font-semibold mb-1">{job.title}</h3>
                        <div className="flex items-center gap-4 text-sm text-muted-foreground mb-2">
                          <span>Posted: {new Date(job.posted).toLocaleDateString()}</span>
                          <span>Expires: {new Date(job.expires).toLocaleDateString()}</span>
                        </div>
                        <div className="flex items-center gap-4">
                          <div className="flex items-center gap-1">
                            <Users className="h-4 w-4" />
                            <span>{job.applicants} applicants</span>
                          </div>
                          <div className="flex items-center gap-1">
                            <Eye className="h-4 w-4" />
                            <span>{job.views} views</span>
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        {getStatusBadge(job.status)}
                        <Button variant="ghost" size="icon">
                          <MoreVertical className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="applicants" className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold">Applicants</h2>
              <p className="text-muted-foreground">{applicants.length} total applicants</p>
            </div>

            <div className="space-y-4">
              {applicants.map((applicant) => (
                <Card key={applicant.id}>
                  <CardContent className="p-6">
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="text-lg font-semibold mb-1">{applicant.name}</h3>
                        <p className="text-muted-foreground mb-2">{applicant.position}</p>
                        <div className="flex items-center gap-4 text-sm text-muted-foreground">
                          <span>Applied: {new Date(applicant.appliedDate).toLocaleDateString()}</span>
                          <span>{applicant.experience}</span>
                          <span>{applicant.location}</span>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        {getStatusBadge(applicant.status)}
                        <Button variant="ghost" size="icon">
                          <Mail className="h-4 w-4" />
                        </Button>
                        <Button variant="ghost" size="icon">
                          <Download className="h-4 w-4" />
                        </Button>
                        <Button variant="ghost" size="icon">
                          <MoreVertical className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                    <div className="mt-4">
                      <Button variant="outline" size="sm">
                        <FileText className="h-4 w-4 mr-2" />
                        View Resume
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </main>
    </ErrorBoundary>
  );
}