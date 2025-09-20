import { useState } from 'react';
import { Button } from '@/components/ui/button';
import JobCard from '../jobs/JobCard';

export default function JobFeedPreview() {
  const [displayCount, setDisplayCount] = useState(6);

  const sampleJobs = [
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
      title: 'Data Scientist',
      company: 'DataFlow Analytics',
      location: 'Remote',
      salary: '$110k - $140k',
      type: 'Full-time',
      remote: true,
      urgent: true,
      posted: '1 day ago',
      isNew: true,
      description: 'Work with machine learning models and big data...',
    },
    {
      id: '3',
      title: 'UX Designer',
      company: 'Design Studio',
      location: 'New York, NY',
      salary: '$80k - $110k',
      type: 'Full-time',
      remote: false,
      urgent: false,
      posted: '3 days ago',
      isNew: false,
      description: 'Create beautiful and intuitive user experiences...',
    },
    {
      id: '4',
      title: 'DevOps Engineer',
      company: 'CloudTech',
      location: 'Austin, TX',
      salary: '$100k - $130k',
      type: 'Full-time',
      remote: true,
      urgent: false,
      posted: '1 week ago',
      isNew: false,
      description: 'Manage cloud infrastructure and deployment pipelines...',
    },
    {
      id: '5',
      title: 'Product Manager',
      company: 'InnovateCo',
      location: 'Seattle, WA',
      salary: '$130k - $170k',
      type: 'Full-time',
      remote: false,
      urgent: true,
      posted: '4 days ago',
      isNew: false,
      description: 'Lead product strategy and development initiatives...',
    },
    {
      id: '6',
      title: 'Frontend Developer',
      company: 'WebSolutions',
      location: 'Remote',
      salary: '$70k - $95k',
      type: 'Contract',
      remote: true,
      urgent: false,
      posted: '5 days ago',
      isNew: false,
      description: 'Build responsive web applications with React...',
    },
    {
      id: '7',
      title: 'Marketing Manager',
      company: 'GrowthHackers',
      location: 'Los Angeles, CA',
      salary: '$85k - $115k',
      type: 'Full-time',
      remote: false,
      urgent: false,
      posted: '6 days ago',
      isNew: false,
      description: 'Drive marketing campaigns and brand awareness...',
    },
    {
      id: '8',
      title: 'Security Engineer',
      company: 'SecureNet',
      location: 'Washington, DC',
      salary: '$115k - $145k',
      type: 'Full-time',
      remote: true,
      urgent: true,
      posted: '3 days ago',
      isNew: false,
      description: 'Implement security measures and protocols...',
    },
  ];

  const handleLoadMore = () => {
    setDisplayCount(prev => Math.min(prev + 3, sampleJobs.length));
  };

  return (
    <section className="container mx-auto px-4 sm:px-6 lg:px-8">
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold mb-4">Latest Job Opportunities</h2>
        <p className="text-lg text-muted-foreground">
          Discover thousands of job openings from top companies
        </p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {sampleJobs.slice(0, displayCount).map((job) => (
          <JobCard key={job.id} job={job} />
        ))}
      </div>

      <div className="text-center">
        {displayCount < sampleJobs.length && (
          <Button onClick={handleLoadMore} size="lg" variant="outline">
            Load More Jobs
          </Button>
        )}
        <div className="mt-4">
          <Button asChild size="lg">
            <a href="/jobs">View All Jobs</a>
          </Button>
        </div>
      </div>
    </section>
  );
}
