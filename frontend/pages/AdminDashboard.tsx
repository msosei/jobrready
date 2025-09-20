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

export default function AdminDashboard() {
  const [activeTab, setActiveTab] = useState('overview');

  const users = [
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

  const companies = [
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

  const jobPostings = [
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

  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
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
                <CardTitle className="text-sm font-medium">Pending Actions</CardTitle>
                <AlertTriangle className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {companies.filter(c => c.status === 'Pending').length + 
                   jobPostings.filter(j => j.flagged).length}
                </div>
                <p className="text-xs text-muted-foreground">
                  Require immediate attention
                </p>
              </CardContent>
            </Card>
          </div>

          <div className="grid lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Recent Activity</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-3 border rounded-lg">
                    <div>
                      <h4 className="font-medium">New company registration</h4>
                      <p className="text-sm text-muted-foreground">StartupCo requested approval</p>
                    </div>
                    <Badge variant="outline">Pending</Badge>
                  </div>
                  <div className="flex items-center justify-between p-3 border rounded-lg">
                    <div>
                      <h4 className="font-medium">Job posting flagged</h4>
                      <p className="text-sm text-muted-foreground">Suspicious content detected</p>
                    </div>
                    <Badge variant="destructive">Flagged</Badge>
                  </div>
                  <div className="flex items-center justify-between p-3 border rounded-lg">
                    <div>
                      <h4 className="font-medium">User account suspended</h4>
                      <p className="text-sm text-muted-foreground">Policy violation reported</p>
                    </div>
                    <Badge variant="destructive">Action Taken</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Platform Statistics</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Active Job Seekers</span>
                    <span className="text-2xl font-bold">
                      {users.filter(u => u.type === 'Candidate' && u.status === 'Active').length}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Active Employers</span>
                    <span className="text-2xl font-bold">
                      {users.filter(u => u.type === 'Employer' && u.status === 'Active').length}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Approved Companies</span>
                    <span className="text-2xl font-bold">
                      {companies.filter(c => c.status === 'Approved').length}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Active Job Postings</span>
                    <span className="text-2xl font-bold">
                      {jobPostings.filter(j => j.status === 'Active').length}
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="users" className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold">User Management</h2>
            <div className="flex gap-2">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input placeholder="Search users..." className="pl-10 w-[250px]" />
              </div>
              <Select>
                <SelectTrigger className="w-[150px]">
                  <SelectValue placeholder="Filter by type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Types</SelectItem>
                  <SelectItem value="candidate">Candidates</SelectItem>
                  <SelectItem value="employer">Employers</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-4">
            {users.map((user) => (
              <Card key={user.id}>
                <CardContent className="p-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-lg font-semibold">{user.name}</h3>
                        {getStatusBadge(user.status)}
                        <Badge variant="outline">{user.type}</Badge>
                      </div>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-muted-foreground">
                        <div>
                          <span className="font-medium">Email:</span> {user.email}
                        </div>
                        <div>
                          <span className="font-medium">Joined:</span> {new Date(user.joinDate).toLocaleDateString()}
                        </div>
                        <div>
                          <span className="font-medium">Last Active:</span> {new Date(user.lastActive).toLocaleDateString()}
                        </div>
                        <div>
                          <span className="font-medium">Status:</span> {user.status}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button variant="outline" size="sm">
                        View Profile
                      </Button>
                      <Select>
                        <SelectTrigger className="w-[140px]">
                          <SelectValue placeholder="Actions" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="activate">Activate</SelectItem>
                          <SelectItem value="suspend">Suspend</SelectItem>
                          <SelectItem value="delete">Delete</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="companies" className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold">Company Management</h2>
            <div className="flex gap-2">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input placeholder="Search companies..." className="pl-10 w-[250px]" />
              </div>
              <Select>
                <SelectTrigger className="w-[150px]">
                  <SelectValue placeholder="Filter by status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Statuses</SelectItem>
                  <SelectItem value="approved">Approved</SelectItem>
                  <SelectItem value="pending">Pending</SelectItem>
                  <SelectItem value="rejected">Rejected</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-4">
            {companies.map((company) => (
              <Card key={company.id}>
                <CardContent className="p-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-lg font-semibold">{company.name}</h3>
                        {getStatusBadge(company.status, 'company')}
                      </div>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-muted-foreground">
                        <div>
                          <span className="font-medium">Industry:</span> {company.industry}
                        </div>
                        <div>
                          <span className="font-medium">Size:</span> {company.size}
                        </div>
                        <div>
                          <span className="font-medium">Joined:</span> {new Date(company.joinDate).toLocaleDateString()}
                        </div>
                        <div>
                          <span className="font-medium">Active Jobs:</span> {company.activeJobs}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button variant="outline" size="sm">
                        View Details
                      </Button>
                      {company.status === 'Pending' && (
                        <>
                          <Button size="sm">
                            Approve
                          </Button>
                          <Button variant="destructive" size="sm">
                            Reject
                          </Button>
                        </>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="jobs" className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold">Job Posting Management</h2>
            <div className="flex gap-2">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input placeholder="Search jobs..." className="pl-10 w-[250px]" />
              </div>
              <Select>
                <SelectTrigger className="w-[150px]">
                  <SelectValue placeholder="Filter by status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Statuses</SelectItem>
                  <SelectItem value="active">Active</SelectItem>
                  <SelectItem value="flagged">Flagged</SelectItem>
                  <SelectItem value="under-review">Under Review</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-4">
            {jobPostings.map((job) => (
              <Card key={job.id}>
                <CardContent className="p-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-lg font-semibold">{job.title}</h3>
                        {getStatusBadge(job.status, 'job')}
                        {job.flagged && <Badge variant="destructive">Flagged</Badge>}
                      </div>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-muted-foreground">
                        <div>
                          <span className="font-medium">Company:</span> {job.company}
                        </div>
                        <div>
                          <span className="font-medium">Posted:</span> {new Date(job.posted).toLocaleDateString()}
                        </div>
                        <div>
                          <span className="font-medium">Applicants:</span> {job.applicants}
                        </div>
                        <div>
                          <span className="font-medium">Status:</span> {job.status}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button variant="outline" size="sm">
                        View Job
                      </Button>
                      {job.flagged && (
                        <>
                          <Button size="sm">
                            Approve
                          </Button>
                          <Button variant="destructive" size="sm">
                            Remove
                          </Button>
                        </>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
