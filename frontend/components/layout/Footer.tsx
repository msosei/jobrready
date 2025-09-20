import { Link } from 'react-router-dom';
import { BrainCircuit } from 'lucide-react';

export default function Footer() {
  const quickLinks = [
    { name: 'Home', href: '/' },
    { name: 'Jobs', href: '/jobs' },
    { name: 'Companies', href: '/companies' },
    { name: 'About', href: '/about' },
    { name: 'Contact', href: '/contact' },
  ];

  const jobSeekerLinks = [
    { name: 'Dashboard', href: '/candidate/dashboard' },
    { name: 'Saved Jobs', href: '/candidate/dashboard?tab=saved' },
    { name: 'Applications', href: '/candidate/dashboard?tab=applications' },
  ];

  const employerLinks = [
    { name: 'Post Jobs', href: '/employer/dashboard?tab=post' },
    { name: 'Manage Applicants', href: '/employer/dashboard?tab=applicants' },
  ];

  const aiToolsLinks = [
    { name: 'Resume Parser', href: '/ai-career-tools?tool=resume-parser' },
    { name: 'Cover Letter Generator', href: '/ai-career-tools?tool=cover-letter' },
    { name: 'ATS Resume Score', href: '/ai-career-tools?tool=ats-score' },
    { name: 'Job Recommendations', href: '/ai-career-tools?tool=recommendations' },
    { name: 'Interview Q&A', href: '/ai-career-tools?tool=interview-qa' },
    { name: 'Mock Interview', href: '/ai-career-tools?tool=mock-interview' },
    { name: 'Salary Insights', href: '/ai-career-tools?tool=salary-insights' },
    { name: 'Portfolio Generator', href: '/ai-career-tools?tool=portfolio' },
    { name: 'Website Builder', href: '/ai-career-tools?tool=website-builder' },
    { name: 'Bulk Apply', href: '/ai-career-tools?tool=bulk-apply' },
  ];

  return (
    <footer className="bg-muted/30 border-t">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8">
          {/* Brand */}
          <div className="lg:col-span-1">
            <Link to="/" className="flex items-center space-x-2 mb-4">
              <BrainCircuit className="h-8 w-8 text-primary" />
              <span className="text-xl font-bold">JobBoard Pro</span>
            </Link>
            <p className="text-sm text-muted-foreground">
              AI-powered job discovery and career tools for the modern workforce.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              {quickLinks.map((link) => (
                <li key={link.name}>
                  <Link
                    to={link.href}
                    className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Job Seekers */}
          <div>
            <h3 className="font-semibold mb-4">Job Seekers</h3>
            <ul className="space-y-2">
              {jobSeekerLinks.map((link) => (
                <li key={link.name}>
                  <Link
                    to={link.href}
                    className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Employers */}
          <div>
            <h3 className="font-semibold mb-4">Employers</h3>
            <ul className="space-y-2">
              {employerLinks.map((link) => (
                <li key={link.name}>
                  <Link
                    to={link.href}
                    className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* AI Career Tools */}
          <div>
            <h3 className="font-semibold mb-4">AI Career Tools</h3>
            <ul className="space-y-2 max-h-48 overflow-y-auto">
              {aiToolsLinks.map((link) => (
                <li key={link.name}>
                  <Link
                    to={link.href}
                    className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="border-t mt-8 pt-8 text-center">
          <p className="text-sm text-muted-foreground">
            © 2024 JobBoard Pro. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
