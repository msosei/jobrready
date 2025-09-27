/**
 * Admin Dashboard Page for MyBrand Job Application Platform
 * 
 * This page provides a comprehensive dashboard for administrators to monitor
 * and manage platform users, companies, and job postings.
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
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { 
  Users, 
  Building2, 
  Briefcase, 
  AlertTriangle, 
  CheckCircle, 
  XCircle, 
  Eye,
  MoreVertical,
  Search,
  Filter
} from 'lucide-react';
import { ErrorBoundary } from '../components/common/ErrorBoundary';
import SEOHead from '../components/seo/SEOHead';

// ============================================================================
// DATA INTERFACES
// TypeScript interfaces for data structures
// ============================================================================

/**
 * User data interface
 * 
 * Represents a platform user (candidate or employer)
 */
interface User {
  /** Unique identifier for the user */
  id: string;
  
  /** User's name */
  name: string;
  
  /** User's email address */
  email: string;
  
  /** Type of user */
  type: 'Candidate' | 'Employer';
  
  /** Current status of the user */
  status: string;
  
  /** Date when the user joined the platform */
  joinDate: string;
  
  /** Date when the user was last active */
  lastActive: string;
}

/**
 * Company data interface
 * 
 * Represents a company registered on the platform
 */
interface Company {
  /** Unique identifier for the company */
  id: string;
  
  /** Company name */
  name: string;
  
  /** Industry the company operates in */
  industry: string;
  
  /** Company size */
  size: string;
  
  /** Current status of the company */
  status: string;
  
  /** Date when the company joined the platform */
  joinDate: string;
  
  /** Number of active job postings */
  activeJobs: number;
}

/**
 * Job posting data interface
 * 
 * Represents a job posting on the platform
 */
interface JobPosting {
  /** Unique identifier for the job posting */
  id: string;
  
  /** Job title */
  title: string;
  
  /** Company that posted the job */
  company: string;
  
  /** Current status of the job posting */
  status: string;
  
  /** Date when the job was posted */
  posted: string;
  
  /** Number of applicants */
  applicants: number;
  
  /** Whether the job has been flagged for review */
  flagged: boolean;
}

// ============================================================================
// PAGE COMPONENT
// Main page component implementation
// ============================================================================

/**
 * Admin dashboard page component for platform management
 * 
 * This component provides a comprehensive dashboard for administrators with
 * multiple tabs for overview, users, companies, and job postings management.
 * It displays key metrics and tools for monitoring platform activity.
 * 
 * @returns JSX element representing the admin dashboard page
 * 
 * @example
 * ```tsx
 * <AdminDashboard />
 * ```
 */
export default function AdminDashboard() {
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

  /** Sample users data */
  const users: User[] = [
    {
      id: '1',
      name: 'John Smith',
      email: 'john@example.com',
      type: 'Candidate',
      status: 'Active',
      joinDate: '2024-01-15',
      lastActive: '2024-01-20',
    },
    {
      id: '2',
      name: 'TechCorp Inc.',
      email: 'hr@techcorp.com',
      type: 'Employer',
      status: 'Active',
      joinDate: '2024-01-10',
      lastActive: '2024-01-19',
    },
    {
      id: '3',
      name: 'Sarah Johnson',
      email: 'sarah@example.com',
      type: 'Candidate',
      status: 'Suspended',
      joinDate: '2024-01-05',
      lastActive: '2024-01-18',
    },
  ];

  /** Sample companies data */
  const companies: Company[] = [
    {
      id: '1',
      name: 'TechCorp Inc.',
      industry: 'Technology',
      size: '1000+',
      status: 'Approved',
      joinDate: '2024-01-10',
      activeJobs: 5,
    },
    {
      id: '2',
      name: 'StartupCo',
      industry: 'Fintech',
      size: '50-100',
      status: 'Pending',
      joinDate: '2024-01-18',
      activeJobs: 0,
    },
    {
      id: '3',
      name: 'DesignStudio',
      industry: 'Design',
      size: '10-50',
      status: 'Rejected',
      joinDate: '2024-01-15',
      activeJobs: 0,
    },
  ];

  /** Sample job postings data */
  const jobPostings: JobPosting[] = [
    {
      id: '1',
      title: 'Senior Software Engineer',
      company: 'TechCorp Inc.',
      status: 'Active',
      posted: '2024-01-15',
      applicants: 45,
      flagged: false,
    },
    {
      id: '2',
      title: 'Suspicious Job Title',
      company: 'ShadyCompany',
      status: 'Flagged',
      posted: '2024-01-19',
      applicants: 2,
      flagged: true,
    },
    {
      id: '3',
      title: 'Product Manager',
      company: 'StartupCo',
      status: 'Under Review',
      posted: '2024-01-18',
      applicants: 12,
      flagged: false,
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
   * @param type - The type of entity (user, company, or job)
   * @returns JSX element representing the status badge
   */
  const getStatusBadge = (status: string, type: 'user' | 'company' | 'job' = 'user') => {
    const variants: { [key: string]: "default" | "secondary" | "destructive" | "outline" } = {
      Active: 'default',
      Approved: 'default',
      Pending: 'outline',
      'Under Review': 'outline',
      Suspended: 'destructive',
      Rejected: 'destructive',
      Flagged: 'destructive',
    };
    return <Badge variant={variants[status] || 'outline'}>{status}</Badge>;
  };

  /**
   * Get appropriate icon for status
   * 
   * Returns an icon component based on the status
   * 
   * @param status - The status text
   * @returns JSX element representing the status icon
   */
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'Active':
      case 'Approved':
        return <CheckCircle className="h-4 w-4 text-green-600" />;
      case 'Suspended':
      case 'Rejected':
      case 'Flagged':
        return <XCircle className="h-4 w-4 text-red-600" />;
      case 'Pending':
      case 'Under Review':
        return <AlertTriangle className="h-4 w-4 text-yellow-600" />;
      default:
        return <Eye className="h-4 w-4 text-gray-600" />;
    }
  };

  // ============================================================================
  // MAIN RENDER
  // Primary component render function
  // ============================================================================

  /**
   * Render the admin dashboard page
   * 
   * Returns the complete dashboard UI with tabs, metrics, and management tools
   */
  return (
    <ErrorBoundary>
      <SEOHead
        title="Admin Dashboard - Platform Management"
        description="Monitor and manage platform users, companies, and job postings from the administrative dashboard."
        keywords="admin dashboard, platform management, user management, company management"
      />
      
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Admin Dashboard</h1>
          <p className="text-muted-foreground">
            Monitor and manage platform users, companies, and job postings
          </p>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-8">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="users">Users</TabsTrigger>
            <TabsTrigger value="companies">Companies</TabsTrigger>
            <TabsTrigger value="jobs">Job Postings</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Users</CardTitle>
                  <Users className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{users.length}</div>
                  <p className="text-xs text-muted-foreground">
                    +12% from last month
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Companies</CardTitle>
                  <Building2 className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{companies.length}</div>
                  <p className="text-xs text-muted-foreground">
                    {companies.filter(c => c.status === 'Pending').length} pending approval
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Job Postings</CardTitle>
                  <Briefcase className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{jobPostings.length}</div>
                  <p className="text-xs text-muted-foreground">
                    {jobPostings.filter(j => j.flagged).length} flagged for review
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Active Applications</CardTitle>
                  <Eye className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    {jobPostings.reduce((sum, job) => sum + job.applicants, 0)}
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
                  <CardTitle>Recent User Activity</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {users.slice(0, 3).map((user) => (
                      <div key={user.id} className="flex items-center justify-between p-3 border rounded-lg">
                        <div>
                          <h4 className="font-medium">{user.name}</h4>
                          <p className="text-sm text-muted-foreground">{user.email}</p>
                        </div>
                        <div className="flex items-center gap-2">
                          {getStatusBadge(user.status)}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Flagged Content</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {jobPostings.filter(j => j.flagged).map((job) => (
                      <div key={job.id} className="flex items-center justify-between p-3 border rounded-lg">
                        <div>
                          <h4 className="font-medium">{job.title}</h4>
                          <p className="text-sm text-muted-foreground">{job.company}</p>
                        </div>
                        <div className="flex items-center gap-2">
                          {getStatusBadge(job.status, 'job')}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="users" className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold">Users</h2>
              <p className="text-muted-foreground">{users.length} total users</p>
            </div>

            <div className="space-y-4">
              {users.map((user) => (
                <Card key={user.id}>
                  <CardContent className="p-6">
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="text-lg font-semibold mb-1">{user.name}</h3>
                        <p className="text-muted-foreground mb-2">{user.email}</p>
                        <div className="flex items-center gap-4 text-sm text-muted-foreground">
                          <span>Type: {user.type}</span>
                          <span>Joined: {new Date(user.joinDate).toLocaleDateString()}</span>
                          <span>Last active: {new Date(user.lastActive).toLocaleDateString()}</span>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        {getStatusBadge(user.status)}
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

          <TabsContent value="companies" className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold">Companies</h2>
              <p className="text-muted-foreground">{companies.length} total companies</p>
            </div>

            <div className="space-y-4">
              {companies.map((company) => (
                <Card key={company.id}>
                  <CardContent className="p-6">
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="text-lg font-semibold mb-1">{company.name}</h3>
                        <p className="text-muted-foreground mb-2">
                          {company.industry} • {company.size} employees
                        </p>
                        <div className="flex items-center gap-4 text-sm text-muted-foreground">
                          <span>Joined: {new Date(company.joinDate).toLocaleDateString()}</span>
                          <span>{company.activeJobs} active jobs</span>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        {getStatusBadge(company.status, 'company')}
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

          <TabsContent value="jobs" className="space-y-6">
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
                        <p className="text-muted-foreground mb-2">{job.company}</p>
                        <div className="flex items-center gap-4 text-sm text-muted-foreground">
                          <span>Posted: {new Date(job.posted).toLocaleDateString()}</span>
                          <span>{job.applicants} applicants</span>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        {getStatusBadge(job.status, 'job')}
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
        </Tabs>
      </main>
    </ErrorBoundary>
  );
}