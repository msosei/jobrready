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

export default function EmployerDashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const [isPostJobOpen, setIsPostJobOpen] = useState(false);

  const jobPostings = [
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

  const applicants = [
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

  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
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
          <TabsTrigger value="jobs">Job Postings</TabsTrigger>
          <TabsTrigger value="applicants">Applicants</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Active Jobs</CardTitle>
                <Briefcase className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {jobPostings.filter(job => job.status === 'Active').length}
                </div>
                <p className="text-xs text-muted-foreground">
                  Currently accepting applications
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
                  Across all positions
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Job Views</CardTitle>
                <Eye className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">3,680</div>
                <p className="text-xs text-muted-foreground">
                  Total views this month
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Pending Reviews</CardTitle>
                <FileText className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">8</div>
                <p className="text-xs text-muted-foreground">
                  Applications to review
                </p>
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
                  {applicants.slice(0, 3).map((applicant) => (
                    <div key={applicant.id} className="flex items-center justify-between p-3 border rounded-lg">
                      <div>
                        <h4 className="font-medium">{applicant.name}</h4>
                        <p className="text-sm text-muted-foreground">{applicant.position}</p>
                      </div>
                      {getStatusBadge(applicant.status)}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Top Performing Jobs</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {jobPostings
                    .sort((a, b) => b.applicants - a.applicants)
                    .slice(0, 3)
                    .map((job) => (
                      <div key={job.id} className="flex items-center justify-between p-3 border rounded-lg">
                        <div>
                          <h4 className="font-medium">{job.title}</h4>
                          <p className="text-sm text-muted-foreground">
                            {job.applicants} applicants • {job.views} views
                          </p>
                        </div>
                        {getStatusBadge(job.status)}
                      </div>
                    ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="jobs" className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold">Job Postings</h2>
            <Button onClick={() => setIsPostJobOpen(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Post New Job
            </Button>
          </div>

          <div className="space-y-4">
            {jobPostings.map((job) => (
              <Card key={job.id}>
                <CardContent className="p-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-lg font-semibold">{job.title}</h3>
                        {getStatusBadge(job.status)}
                      </div>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-muted-foreground">
                        <div>
                          <span className="font-medium">Applicants:</span> {job.applicants}
                        </div>
                        <div>
                          <span className="font-medium">Views:</span> {job.views}
                        </div>
                        <div>
                          <span className="font-medium">Posted:</span> {new Date(job.posted).toLocaleDateString()}
                        </div>
                        <div>
                          <span className="font-medium">Expires:</span> {new Date(job.expires).toLocaleDateString()}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button variant="outline" size="sm">
                        Edit
                      </Button>
                      <Button variant="outline" size="sm">
                        View
                      </Button>
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
            <div className="flex gap-2">
              <Select>
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="Filter by position" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Positions</SelectItem>
                  <SelectItem value="senior-engineer">Senior Software Engineer</SelectItem>
                  <SelectItem value="product-manager">Product Manager</SelectItem>
                  <SelectItem value="ux-designer">UX Designer</SelectItem>
                </SelectContent>
              </Select>
              <Select>
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="Filter by status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Statuses</SelectItem>
                  <SelectItem value="under-review">Under Review</SelectItem>
                  <SelectItem value="interview">Interview Scheduled</SelectItem>
                  <SelectItem value="shortlisted">Shortlisted</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-4">
            {applicants.map((applicant) => (
              <Card key={applicant.id}>
                <CardContent className="p-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-3">
                        <h3 className="text-lg font-semibold">{applicant.name}</h3>
                        {getStatusBadge(applicant.status)}
                      </div>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-muted-foreground mb-4">
                        <div>
                          <span className="font-medium">Position:</span> {applicant.position}
                        </div>
                        <div>
                          <span className="font-medium">Experience:</span> {applicant.experience}
                        </div>
                        <div>
                          <span className="font-medium">Location:</span> {applicant.location}
                        </div>
                        <div>
                          <span className="font-medium">Applied:</span> {new Date(applicant.appliedDate).toLocaleDateString()}
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 pt-4 border-t">
                    <Button size="sm">
                      <FileText className="h-4 w-4 mr-2" />
                      View Resume
                    </Button>
                    <Button variant="outline" size="sm">
                      <Download className="h-4 w-4 mr-2" />
                      Download
                    </Button>
                    <Button variant="outline" size="sm">
                      <Mail className="h-4 w-4 mr-2" />
                      Contact
                    </Button>
                    <Select>
                      <SelectTrigger className="w-[180px]">
                        <SelectValue placeholder="Update status" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="under-review">Under Review</SelectItem>
                        <SelectItem value="interview">Schedule Interview</SelectItem>
                        <SelectItem value="shortlisted">Shortlist</SelectItem>
                        <SelectItem value="rejected">Reject</SelectItem>
                      </SelectContent>
                    </Select>
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
