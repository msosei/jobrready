import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { FileText, Lightbulb, BarChart3, Brain, ArrowRight } from 'lucide-react';

export default function AIToolsTeaser() {
  const featuredTools = [
    {
      icon: FileText,
      title: 'Resume Parser',
      description: 'AI-powered resume analysis and optimization suggestions',
      color: 'text-blue-600',
    },
    {
      icon: Lightbulb,
      title: 'Cover Letter Generator',
      description: 'Create personalized cover letters tailored to each job',
      color: 'text-green-600',
    },
    {
      icon: BarChart3,
      title: 'ATS Resume Score',
      description: 'Check how well your resume performs with ATS systems',
      color: 'text-purple-600',
    },
    {
      icon: Brain,
      title: 'Interview Q&A Generator',
      description: 'Practice with AI-generated interview questions',
      color: 'text-orange-600',
    },
  ];

  return (
    <section className="bg-muted/30 py-16">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4">AI-Powered Career Tools</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Accelerate your career with cutting-edge AI tools designed to help you 
            stand out in today's competitive job market
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {featuredTools.map((tool) => {
            const Icon = tool.icon;
            return (
              <Card key={tool.title} className="hover:shadow-lg transition-shadow">
                <CardHeader className="text-center">
                  <Icon className={`h-12 w-12 mx-auto mb-4 ${tool.color}`} />
                  <CardTitle className="text-lg">{tool.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground text-center">
                    {tool.description}
                  </p>
                </CardContent>
              </Card>
            );
          })}
        </div>

        <div className="text-center">
          <Button asChild size="lg" className="group">
            <Link to="/ai-career-tools">
              Explore All AI Tools
              <ArrowRight className="h-4 w-4 ml-2 group-hover:translate-x-1 transition-transform" />
            </Link>
          </Button>
        </div>
      </div>
    </section>
  );
}
