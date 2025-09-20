import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { TrendingUp, MapPin, DollarSign } from 'lucide-react';

export default function TrendingJobs() {
  const categories = [
    { name: 'Software Engineering', growth: '+15%', jobs: 1234 },
    { name: 'Data Science', growth: '+22%', jobs: 856 },
    { name: 'Product Management', growth: '+18%', jobs: 432 },
    { name: 'UX/UI Design', growth: '+12%', jobs: 678 },
    { name: 'DevOps', growth: '+25%', jobs: 345 },
    { name: 'Marketing', growth: '+8%', jobs: 567 },
  ];

  const trendingJobs = [
    {
      title: 'Senior Full Stack Developer',
      company: 'TechCorp',
      location: 'San Francisco, CA',
      salary: '$120k - $160k',
      type: 'Full-time',
      remote: true,
      urgent: false,
    },
    {
      title: 'Machine Learning Engineer',
      company: 'AI Innovations',
      location: 'Remote',
      salary: '$140k - $180k',
      type: 'Full-time',
      remote: true,
      urgent: true,
    },
    {
      title: 'Product Designer',
      company: 'Design Studio',
      location: 'New York, NY',
      salary: '$90k - $120k',
      type: 'Full-time',
      remote: false,
      urgent: false,
    },
  ];

  return (
    <section className="container mx-auto px-4 sm:px-6 lg:px-8">
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold mb-4">Trending Jobs & Categories</h2>
        <p className="text-lg text-muted-foreground">
          Hot job categories and latest opportunities in the market
        </p>
      </div>

      <div className="grid lg:grid-cols-2 gap-12">
        {/* Popular Categories */}
        <div>
          <h3 className="text-xl font-semibold mb-6 flex items-center">
            <TrendingUp className="h-5 w-5 mr-2 text-primary" />
            Popular Categories
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {categories.map((category) => (
              <Card key={category.name} className="hover:shadow-md transition-shadow cursor-pointer">
                <CardContent className="p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-semibold">{category.name}</h4>
                    <Badge variant="secondary" className="text-green-600">
                      {category.growth}
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    {category.jobs.toLocaleString()} jobs available
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Trending Jobs */}
        <div>
          <h3 className="text-xl font-semibold mb-6">Latest Opportunities</h3>
          <div className="space-y-4">
            {trendingJobs.map((job, index) => (
              <Card key={index} className="hover:shadow-md transition-shadow cursor-pointer">
                <CardContent className="p-4">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h4 className="font-semibold">{job.title}</h4>
                      <p className="text-sm text-muted-foreground">{job.company}</p>
                    </div>
                    <div className="flex gap-2">
                      {job.remote && <Badge variant="outline">Remote</Badge>}
                      {job.urgent && <Badge variant="destructive">Urgent</Badge>}
                    </div>
                  </div>
                  <div className="flex items-center gap-4 text-sm text-muted-foreground">
                    <div className="flex items-center">
                      <MapPin className="h-4 w-4 mr-1" />
                      {job.location}
                    </div>
                    <div className="flex items-center">
                      <DollarSign className="h-4 w-4 mr-1" />
                      {job.salary}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
