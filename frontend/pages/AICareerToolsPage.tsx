import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  FileText,
  Lightbulb,
  BarChart3,
  Brain,
  MessageSquare,
  Camera,
  DollarSign,
  Folder,
  Globe,
  Zap,
  Upload,
  Sparkles,
  Target,
} from 'lucide-react';
import { ErrorBoundary } from '../components/common/ErrorBoundary';
import SEOHead from '../components/seo/SEOHead';
import LoadingSpinner from '../components/common/LoadingSpinner';

export default function AICareerToolsPage() {
  const [isResumeParserOpen, setIsResumeParserOpen] = useState(false);
  const [isCoverLetterOpen, setIsCoverLetterOpen] = useState(false);
  const [isInterviewQAOpen, setIsInterviewQAOpen] = useState(false);
  const [isMockInterviewOpen, setIsMockInterviewOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const tools = [
    {
      id: 'resume-parser',
      icon: FileText,
      title: 'Resume Parser',
      description: 'AI-powered resume analysis and optimization suggestions',
      color: 'text-blue-600',
      bgColor: 'bg-blue-50 dark:bg-blue-950/20',
      features: ['ATS Compatibility Check', 'Skills Gap Analysis', 'Format Optimization', 'Keyword Enhancement'],
      available: true,
    },
    {
      id: 'cover-letter',
      icon: Lightbulb,
      title: 'Cover Letter Generator',
      description: 'Create personalized cover letters tailored to each job',
      color: 'text-green-600',
      bgColor: 'bg-green-50 dark:bg-green-950/20',
      features: ['Job-Specific Content', 'Company Research', 'Tone Customization', 'Multiple Templates'],
      available: true,
    },
    {
      id: 'ats-score',
      icon: BarChart3,
      title: 'ATS Resume Score',
      description: 'Check how well your resume performs with ATS systems',
      color: 'text-purple-600',
      bgColor: 'bg-purple-50 dark:bg-purple-950/20',
      features: ['ATS Compatibility Score', 'Improvement Suggestions', 'Keyword Optimization', 'Format Analysis'],
      available: true,
    },
    {
      id: 'recommendations',
      icon: Target,
      title: 'Job Recommendations',
      description: 'AI-powered job matching based on your profile and preferences',
      color: 'text-orange-600',
      bgColor: 'bg-orange-50 dark:bg-orange-950/20',
      features: ['Smart Matching', 'Skill-Based Filtering', 'Career Path Analysis', 'Salary Insights'],
      available: true,
    },
    {
      id: 'interview-qa',
      icon: Brain,
      title: 'Interview Q&A Generator',
      description: 'Practice with AI-generated interview questions',
      color: 'text-red-600',
      bgColor: 'bg-red-50 dark:bg-red-950/20',
      features: ['Role-Specific Questions', 'STAR Method Guidance', 'Answer Evaluation', 'Practice Tracking'],
      available: true,
    },
    {
      id: 'mock-interview',
      icon: Camera,
      title: 'Mock Interview Simulator',
      description: 'Full mock interview experience with AI feedback',
      color: 'text-indigo-600',
      bgColor: 'bg-indigo-50 dark:bg-indigo-950/20',
      features: ['Video Practice', 'Real-time Feedback', 'Body Language Analysis', 'Confidence Building'],
      available: true,
    },
    {
      id: 'salary-insights',
      icon: DollarSign,
      title: 'Salary Insights',
      description: 'Market salary data and negotiation guidance',
      color: 'text-emerald-600',
      bgColor: 'bg-emerald-50 dark:bg-emerald-950/20',
      features: ['Market Analysis', 'Negotiation Tips', 'Benefits Calculator', 'Location Comparison'],
      available: true,
    },
    {
      id: 'portfolio',
      icon: Folder,
      title: 'Portfolio Project Generator',
      description: 'AI-suggested portfolio projects for your career goals',
      color: 'text-pink-600',
      bgColor: 'bg-pink-50 dark:bg-pink-950/20',
      features: ['Project Ideas', 'Skill Building', 'Technology Recommendations', 'Career Alignment'],
      available: true,
    },
    {
      id: 'website-builder',
      icon: Globe,
      title: 'Personal Website Builder',
      description: 'Create a professional website to showcase your skills',
      color: 'text-cyan-600',
      bgColor: 'bg-cyan-50 dark:bg-cyan-950/20',
      features: ['Template Selection', 'Content Generation', 'SEO Optimization', 'Portfolio Integration'],
      available: false,
    },
    {
      id: 'bulk-apply',
      icon: Zap,
      title: 'Bulk Apply Orchestrator',
      description: 'Efficiently apply to multiple jobs with AI assistance',
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-50 dark:bg-yellow-950/20',
      features: ['Application Automation', 'Custom Cover Letters', 'Application Tracking', 'Follow-up Reminders'],
      available: false,
    },
  ];

  const jobRecommendations = [
    {
      title: 'Senior Frontend Developer',
      company: 'TechCorp',
      match: 95,
      salary: '$120k - $160k',
      location: 'San Francisco, CA',
    },
    {
      title: 'React Developer',
      company: 'StartupCo',
      match: 88,
      salary: '$100k - $130k',
      location: 'Remote',
    },
    {
      title: 'Full Stack Engineer',
      company: 'WebSolutions',
      match: 82,
      salary: '$110k - $140k',
      location: 'New York, NY',
    },
  ];

  const handleToolClick = (toolId: string) => {
    if (isLoading) return;

    switch (toolId) {
      case 'resume-parser':
        setIsResumeParserOpen(true);
        break;
      case 'cover-letter':
        setIsCoverLetterOpen(true);
        break;
      case 'interview-qa':
        setIsInterviewQAOpen(true);
        break;
      case 'mock-interview':
        setIsMockInterviewOpen(true);
        break;
      default:
        console.log(`${toolId} clicked`);
    }
  };

  const handleFileUpload = async () => {
    setIsLoading(true);
    // Simulate file processing
    await new Promise(resolve => setTimeout(resolve, 2000));
    setIsLoading(false);
  };

  return (
    <ErrorBoundary>
      <SEOHead
        title="AI Career Tools - Accelerate Your Career"
        description="Transform your job search with AI-powered tools including resume optimization, cover letter generation, interview practice, and more."
        keywords="AI career tools, resume optimizer, cover letter generator, interview practice, job search AI"
      />
      
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <header className="text-center mb-12">
          <div className="flex items-center justify-center mb-6">
            <Sparkles className="h-8 w-8 text-primary mr-2" aria-hidden="true" />
            <span className="text-sm font-medium text-primary uppercase tracking-wide">
              AI-Powered Career Tools
            </span>
          </div>
          <h1 className="text-4xl font-bold mb-4">
            Accelerate Your Career with AI
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Transform your job search and career development with our comprehensive suite of 
            AI-powered tools designed to help you stand out in today's competitive market.
          </p>
        </header>

        {/* Tools Grid */}
        <section className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-16" aria-label="AI Career Tools">
          {tools.map((tool) => {
            const Icon = tool.icon;
            return (
              <Card 
                key={tool.id} 
                className={`hover:shadow-lg transition-all duration-200 cursor-pointer ${
                  !tool.available ? 'opacity-60' : ''
                }`}
                onClick={() => tool.available && handleToolClick(tool.id)}
                onKeyDown={(e) => {
                  if ((e.key === 'Enter' || e.key === ' ') && tool.available) {
                    e.preventDefault();
                    handleToolClick(tool.id);
                  }
                }}
                tabIndex={tool.available ? 0 : -1}
                role="button"
                aria-label={`Open ${tool.title} tool`}
              >
                <CardHeader className="text-center pb-3">
                  <div className={`mx-auto p-3 rounded-lg ${tool.bgColor} w-fit mb-4`}>
                    <Icon className={`h-8 w-8 ${tool.color}`} aria-hidden="true" />
                  </div>
                  <CardTitle className="text-lg mb-2">{tool.title}</CardTitle>
                  {!tool.available && (
                    <Badge variant="secondary" className="mx-auto">
                      Coming Soon
                    </Badge>
                  )}
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground text-center mb-4">
                    {tool.description}
                  </p>
                  <div className="space-y-1">
                    {tool.features.slice(0, 3).map((feature, index) => (
                      <div key={index} className="flex items-center text-xs text-muted-foreground">
                        <span className="w-1 h-1 bg-muted-foreground rounded-full mr-2" aria-hidden="true" />
                        {feature}
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </section>

        {/* Featured Sections */}
        <section className="grid lg:grid-cols-2 gap-8 mb-16" aria-label="Featured tools preview">
          {/* ATS Score Demo */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <BarChart3 className="h-5 w-5 mr-2 text-purple-600" aria-hidden="true" />
                ATS Resume Score
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium">Overall Score</span>
                    <span className="text-2xl font-bold text-purple-600">85%</span>
                  </div>
                  <Progress value={85} className="h-2" aria-label="Overall ATS score: 85%" />
                </div>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="font-medium">Keywords:</span>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Match</span>
                      <span className="text-green-600">92%</span>
                    </div>
                  </div>
                  <div>
                    <span className="font-medium">Format:</span>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Score</span>
                      <span className="text-yellow-600">78%</span>
                    </div>
                  </div>
                </div>
                <Button className="w-full" size="sm" onClick={() => setIsResumeParserOpen(true)}>
                  Analyze Your Resume
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Job Recommendations */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Target className="h-5 w-5 mr-2 text-orange-600" aria-hidden="true" />
                AI Job Recommendations
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {jobRecommendations.map((job, index) => (
                  <div key={index} className="p-3 border rounded-lg">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h4 className="font-medium text-sm">{job.title}</h4>
                        <p className="text-xs text-muted-foreground">{job.company}</p>
                      </div>
                      <Badge variant="secondary" className="text-xs">
                        {job.match}% match
                      </Badge>
                    </div>
                    <div className="flex justify-between text-xs text-muted-foreground">
                      <span>{job.salary}</span>
                      <span>{job.location}</span>
                    </div>
                  </div>
                ))}
                <Button className="w-full" size="sm">
                  View All Recommendations
                </Button>
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Modals */}
        <Dialog open={isResumeParserOpen} onOpenChange={setIsResumeParserOpen}>
          <DialogContent className="max-w-2xl" aria-describedby="resume-parser-description">
            <DialogHeader>
              <DialogTitle className="flex items-center">
                <FileText className="h-5 w-5 mr-2 text-blue-600" aria-hidden="true" />
                Resume Parser & Optimizer
              </DialogTitle>
            </DialogHeader>
            <div id="resume-parser-description" className="space-y-6">
              <div className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-8 text-center">
                <Upload className="h-12 w-12 mx-auto mb-4 text-muted-foreground" aria-hidden="true" />
                <h3 className="text-lg font-medium mb-2">Upload Your Resume</h3>
                <p className="text-sm text-muted-foreground mb-4">
                  PDF, DOC, or DOCX files up to 5MB
                </p>
                <Button onClick={handleFileUpload} disabled={isLoading}>
                  {isLoading ? <LoadingSpinner size="sm" /> : 'Choose File'}
                </Button>
              </div>
              <div className="text-sm text-muted-foreground">
                <h4 className="font-medium mb-2">What we'll analyze:</h4>
                <ul className="space-y-1">
                  <li>• ATS compatibility and formatting</li>
                  <li>• Keyword optimization for your target roles</li>
                  <li>• Skills gap analysis and recommendations</li>
                  <li>• Content structure and impact statements</li>
                </ul>
              </div>
            </div>
          </DialogContent>
        </Dialog>

        <Dialog open={isCoverLetterOpen} onOpenChange={setIsCoverLetterOpen}>
          <DialogContent className="max-w-2xl" aria-describedby="cover-letter-description">
            <DialogHeader>
              <DialogTitle className="flex items-center">
                <Lightbulb className="h-5 w-5 mr-2 text-green-600" aria-hidden="true" />
                AI Cover Letter Generator
              </DialogTitle>
            </DialogHeader>
            <div id="cover-letter-description" className="space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label htmlFor="job-title" className="text-sm font-medium mb-2 block">Job Title</label>
                  <Input id="job-title" placeholder="e.g., Senior Software Engineer" />
                </div>
                <div>
                  <label htmlFor="company-name" className="text-sm font-medium mb-2 block">Company Name</label>
                  <Input id="company-name" placeholder="e.g., TechCorp Inc." />
                </div>
              </div>
              <div>
                <label htmlFor="job-description" className="text-sm font-medium mb-2 block">Job Description (paste here)</label>
                <Textarea 
                  id="job-description"
                  placeholder="Paste the job description to generate a tailored cover letter..."
                  rows={4}
                />
              </div>
              <div>
                <label htmlFor="background" className="text-sm font-medium mb-2 block">Your Background (optional)</label>
                <Textarea 
                  id="background"
                  placeholder="Brief description of your relevant experience..."
                  rows={3}
                />
              </div>
              <Button className="w-full" disabled={isLoading}>
                {isLoading ? <LoadingSpinner size="sm" /> : 'Generate Cover Letter'}
              </Button>
            </div>
          </DialogContent>
        </Dialog>

        <Dialog open={isInterviewQAOpen} onOpenChange={setIsInterviewQAOpen}>
          <DialogContent className="max-w-2xl" aria-describedby="interview-qa-description">
            <DialogHeader>
              <DialogTitle className="flex items-center">
                <Brain className="h-5 w-5 mr-2 text-red-600" aria-hidden="true" />
                Interview Q&A Generator
              </DialogTitle>
            </DialogHeader>
            <div id="interview-qa-description">
              <Tabs defaultValue="generate" className="space-y-6">
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="generate">Generate Questions</TabsTrigger>
                  <TabsTrigger value="practice">Practice Session</TabsTrigger>
                </TabsList>
                <TabsContent value="generate" className="space-y-4">
                  <div>
                    <label htmlFor="job-role" className="text-sm font-medium mb-2 block">Job Role</label>
                    <Input id="job-role" placeholder="e.g., Software Engineer, Product Manager" />
                  </div>
                  <div>
                    <label htmlFor="experience-level" className="text-sm font-medium mb-2 block">Experience Level</label>
                    <Input id="experience-level" placeholder="e.g., Entry, Mid, Senior" />
                  </div>
                  <div>
                    <label htmlFor="company-industry" className="text-sm font-medium mb-2 block">Company/Industry</label>
                    <Input id="company-industry" placeholder="e.g., Tech Startup, Financial Services" />
                  </div>
                  <Button className="w-full" disabled={isLoading}>
                    {isLoading ? <LoadingSpinner size="sm" /> : 'Generate Interview Questions'}
                  </Button>
                </TabsContent>
                <TabsContent value="practice" className="space-y-4">
                  <div className="p-4 bg-muted/50 rounded-lg">
                    <h4 className="font-medium mb-2">Sample Question:</h4>
                    <p className="text-sm text-muted-foreground mb-4">
                      "Tell me about a challenging project you worked on and how you overcame the obstacles."
                    </p>
                    <label htmlFor="answer" className="sr-only">Your answer</label>
                    <Textarea 
                      id="answer"
                      placeholder="Type your answer here..."
                      rows={4}
                    />
                  </div>
                  <div className="flex gap-2">
                    <Button className="flex-1" disabled={isLoading}>
                      {isLoading ? <LoadingSpinner size="sm" /> : 'Submit Answer'}
                    </Button>
                    <Button variant="outline">
                      Next Question
                    </Button>
                  </div>
                </TabsContent>
              </Tabs>
            </div>
          </DialogContent>
        </Dialog>

        <Dialog open={isMockInterviewOpen} onOpenChange={setIsMockInterviewOpen}>
          <DialogContent className="max-w-2xl" aria-describedby="mock-interview-description">
            <DialogHeader>
              <DialogTitle className="flex items-center">
                <Camera className="h-5 w-5 mr-2 text-indigo-600" aria-hidden="true" />
                Mock Interview Simulator
              </DialogTitle>
            </DialogHeader>
            <div id="mock-interview-description" className="space-y-6">
              <div className="aspect-video bg-muted rounded-lg flex items-center justify-center">
                <div className="text-center">
                  <Camera className="h-12 w-12 mx-auto mb-4 text-muted-foreground" aria-hidden="true" />
                  <p className="text-sm text-muted-foreground">
                    Camera will activate when you start the interview
                  </p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label htmlFor="interview-type" className="text-sm font-medium mb-2 block">Interview Type</label>
                  <Input id="interview-type" placeholder="e.g., Technical, Behavioral" />
                </div>
                <div>
                  <label htmlFor="duration" className="text-sm font-medium mb-2 block">Duration</label>
                  <Input id="duration" placeholder="e.g., 30 minutes" />
                </div>
              </div>
              <div className="p-4 bg-blue-50 dark:bg-blue-950/20 rounded-lg">
                <h4 className="font-medium text-blue-900 dark:text-blue-100 mb-2">
                  What to expect:
                </h4>
                <ul className="text-sm text-blue-700 dark:text-blue-300 space-y-1">
                  <li>• Real-time interview questions</li>
                  <li>• AI feedback on your responses</li>
                  <li>• Body language and speech analysis</li>
                  <li>• Detailed performance report</li>
                </ul>
              </div>
              <Button className="w-full" size="lg" disabled={isLoading}>
                {isLoading ? <LoadingSpinner size="sm" /> : 'Start Mock Interview'}
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </main>
    </ErrorBoundary>
  );
}
