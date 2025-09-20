import { useParams } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Building2, MapPin, Users, Globe, Star } from 'lucide-react';
import JobCard from '../components/jobs/JobCard';

export default function CompanyProfilePage() {
  const { id } = useParams();

  // Mock company data
  const company = {
    id: id,
    name: 'TechCorp Inc.',
    logo: '/api/placeholder/120/120',
    banner: '/api/placeholder/1200/300',
    industry: 'Technology',
    size: '1,001-5,000 employees',
    location: 'San Francisco, CA',
    website: 'https://techcorp.com',
    rating: 4.5,
    reviewCount: 1250,
    founded: 2010,
    description: 'TechCorp Inc. is a leading technology company that specializes in developing innovative software solutions for businesses worldwide. We are committed to creating cutting-edge products that transform the way companies operate and grow.',
    mission: 'To empower businesses through innovative technology solutions that drive growth, efficiency, and success in the digital age.',
    values: ['Innovation', 'Integrity', 'Collaboration', 'Excellence', 'Customer Focus'],
    benefits: [
      'Competitive salary and equity',
      'Comprehensive health insurance',
      'Flexible work arrangements',
      'Professional development budget',
      'Unlimited PTO',
      'Modern office spaces',
      'Team building events',
      'Wellness programs'
    ],
    openJobs: [
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
        company: 'TechCorp Inc.',
        location: 'San Francisco, CA',
        salary: '$130k - $170k',
        type: 'Full-time',
        remote: false,
        urgent: true,
        posted: '1 week ago',
        isNew: false,
        description: 'Lead product strategy and development...',
      },
      {
        id: '3',
        title: 'UX Designer',
        company: 'TechCorp Inc.',
        location: 'Remote',
        salary: '$90k - $120k',
        type: 'Full-time',
        remote: true,
        urgent: false,
        posted: '3 days ago',
        isNew: false,
        description: 'Create beautiful and intuitive user experiences...',
      },
    ]
  };

  return (
    <div className="min-h-screen">
      {/* Banner Section */}
      <div className="relative h-64 bg-gradient-to-r from-primary/20 to-secondary/20">
        <img
          src={company.banner}
          alt={`${company.name} banner`}
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black/20" />
      </div>

      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        {/* Company Header */}
        <div className="relative -mt-20 mb-8">
          <div className="bg-background rounded-lg shadow-lg p-6">
            <div className="flex flex-col md:flex-row items-start md:items-center gap-6">
              <img
                src={company.logo}
                alt={`${company.name} logo`}
                className="w-24 h-24 rounded-lg border bg-white"
              />
              <div className="flex-1">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div>
                    <h1 className="text-3xl font-bold mb-2">{company.name}</h1>
                    <div className="flex flex-wrap items-center gap-4 text-muted-foreground">
                      <div className="flex items-center">
                        <Building2 className="h-4 w-4 mr-1" />
                        {company.industry}
                      </div>
                      <div className="flex items-center">
                        <Users className="h-4 w-4 mr-1" />
                        {company.size}
                      </div>
                      <div className="flex items-center">
                        <MapPin className="h-4 w-4 mr-1" />
                        {company.location}
                      </div>
                      <div className="flex items-center">
                        <Star className="h-4 w-4 mr-1 text-yellow-500" />
                        {company.rating} ({company.reviewCount} reviews)
                      </div>
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <Button variant="outline" asChild>
                      <a href={company.website} target="_blank" rel="noopener noreferrer">
                        <Globe className="h-4 w-4 mr-2" />
                        Website
                      </a>
                    </Button>
                    <Button>Follow Company</Button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Company Content */}
        <Tabs defaultValue="overview" className="space-y-8">
          <TabsList className="grid w-full grid-cols-3 lg:w-[400px]">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="jobs">Jobs ({company.openJobs.length})</TabsTrigger>
            <TabsTrigger value="culture">Culture</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-8">
            <div className="grid lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2 space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>About {company.name}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-muted-foreground leading-relaxed">
                      {company.description}
                    </p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Our Mission</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-muted-foreground leading-relaxed">
                      {company.mission}
                    </p>
                  </CardContent>
                </Card>
              </div>

              <div className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Company Info</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div>
                      <span className="font-medium">Founded:</span>
                      <span className="ml-2 text-muted-foreground">{company.founded}</span>
                    </div>
                    <div>
                      <span className="font-medium">Industry:</span>
                      <span className="ml-2 text-muted-foreground">{company.industry}</span>
                    </div>
                    <div>
                      <span className="font-medium">Company Size:</span>
                      <span className="ml-2 text-muted-foreground">{company.size}</span>
                    </div>
                    <div>
                      <span className="font-medium">Headquarters:</span>
                      <span className="ml-2 text-muted-foreground">{company.location}</span>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Our Values</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="flex flex-wrap gap-2">
                      {company.values.map((value) => (
                        <Badge key={value} variant="secondary">
                          {value}
                        </Badge>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="jobs" className="space-y-6">
            <div>
              <h2 className="text-2xl font-bold mb-4">Open Positions</h2>
              <p className="text-muted-foreground mb-6">
                Explore career opportunities and join our growing team
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {company.openJobs.map((job) => (
                <JobCard key={job.id} job={job} />
              ))}
            </div>
          </TabsContent>

          <TabsContent value="culture" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Benefits & Perks</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-2 gap-4">
                  {company.benefits.map((benefit, index) => (
                    <div key={index} className="flex items-center">
                      <span className="text-green-600 mr-3">✓</span>
                      <span>{benefit}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Work Environment</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground leading-relaxed">
                  At TechCorp, we believe in fostering a collaborative and inclusive work environment 
                  where every team member can thrive. Our modern offices are designed to promote 
                  creativity and productivity, while our flexible work policies ensure a healthy 
                  work-life balance.
                </p>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
