/*
 * Header Component for MyBrand Job Application Platform
 * 
 * This component provides the main navigation header for the application,
 * including responsive design for mobile and desktop views, navigation links,
 * dashboard access, and notification center integration.
 * 
 * The header features:
 * 1. Responsive design with mobile menu toggle
 * 2. Navigation links for main application sections
 * 3. Dashboard access links for different user roles
 * 4. Notification center integration
 * 5. Active route highlighting
 * 6. Accessibility features including ARIA labels and keyboard navigation
 */

// Import required React hooks and components
import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { Menu, BrainCircuit, User, Building2, Shield, Bot, FileText, Users, MessageCircle, TrendingUp, Mic, Globe, BookOpen, DollarSign } from 'lucide-react';
import NotificationCenter from '../common/NotificationCenter';

export default function Header() {
  // State for controlling mobile menu open/close
  const [isOpen, setIsOpen] = useState(false);
  
  // Get current location for active route detection
  const location = useLocation();

  // Request notification permission when component mounts
  // This ensures users can receive real-time notifications
  useEffect(() => {
    if ('Notification' in window && Notification.permission === 'default') {
      Notification.requestPermission();
    }
  }, []);

  // Main navigation links for the application
  const navigation = [
    { name: 'Home', href: '/' },
    { name: 'Jobs', href: '/jobs' },
    { name: 'AI Career Tools', href: '/ai-career-tools' },
  ];

  // AI Microservices navigation links
  const aiServices = [
    { name: 'Skill Gap Analyzer', href: '/ai/skill-gap', icon: TrendingUp },
    { name: 'Resume Builder', href: '/ai/resume-builder', icon: FileText },
    { name: 'Resume Enhancer', href: '/ai/resume-enhancer', icon: FileText },
    { name: 'Interview Coach', href: '/ai/interview-coach', icon: MessageCircle },
    { name: 'Mock Interviewer', href: '/ai/mock-interviewer', icon: Mic },
    { name: 'Job Matcher', href: '/ai/job-matcher', icon: Users },
    { name: 'Job Recommender', href: '/ai/job-recommender', icon: TrendingUp },
    { name: 'Document Summarizer', href: '/ai/document-summarizer', icon: FileText },
    { name: 'Course Recommender', href: '/ai/course-recommender', icon: BookOpen },
    { name: 'Salary Predictor', href: '/ai/salary-predictor', icon: DollarSign },
    { name: 'Diversity Insights', href: '/ai/diversity-insights', icon: Users },
    { name: 'Multi-Language', href: '/ai/multi-language', icon: Globe },
    { name: 'Voice Agent', href: '/ai/voice-agent', icon: Mic },
    { name: 'Career Chatbot', href: '/ai/career-chatbot', icon: Bot },
  ];

  // Dashboard links for different user roles
  const dashboardLinks = [
    { name: 'Candidate Dashboard', href: '/candidate/dashboard', icon: User },
    { name: 'Employer Dashboard', href: '/employer/dashboard', icon: Building2 },
    { name: 'Admin Dashboard', href: '/admin/dashboard', icon: Shield },
  ];

  // Helper function to determine if a navigation link is active
  const isActive = (href: string) => location.pathname === href;

  return (
    <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Brand/logo section */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <BrainCircuit className="h-8 w-8 text-primary" />
              <span className="text-xl font-bold">JobBoard Pro</span>
            </Link>
          </div>

          {/* Desktop Navigation - hidden on mobile */}
          <nav className="hidden md:flex items-center space-x-8" role="navigation" aria-label="Main navigation">
            {navigation.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className={`text-sm font-medium transition-colors hover:text-primary focus:text-primary focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 rounded-sm ${
                  isActive(item.href) ? 'text-primary' : 'text-muted-foreground'
                }`}
                aria-current={isActive(item.href) ? 'page' : undefined}
              >
                {item.name}
              </Link>
            ))}
            
            {/* AI Services Dropdown */}
            <div className="relative group">
              <button className="text-sm font-medium text-muted-foreground hover:text-primary focus:text-primary focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 rounded-sm">
                AI Services
              </button>
              <div className="absolute left-0 mt-2 w-64 rounded-md shadow-lg bg-background border border-border opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 z-50">
                <div className="py-1">
                  {aiServices.map((service) => {
                    const Icon = service.icon;
                    return (
                      <Link
                        key={service.name}
                        to={service.href}
                        className="flex items-center px-4 py-2 text-sm hover:bg-accent hover:text-accent-foreground"
                        onClick={() => setIsOpen(false)}
                      >
                        <Icon className="h-4 w-4 mr-2" />
                        {service.name}
                      </Link>
                    );
                  })}
                </div>
              </div>
            </div>
          </nav>

          {/* Desktop Dashboard Links & Notifications - hidden on mobile */}
          <div className="hidden md:flex items-center space-x-4">
            <NotificationCenter userId="demo-user" />
            {dashboardLinks.map((item) => {
              const Icon = item.icon;
              return (
                <Button
                  key={item.name}
                  variant={isActive(item.href) ? 'default' : 'ghost'}
                  size="sm"
                  asChild
                >
                  <Link 
                    to={item.href} 
                    className="flex items-center space-x-2"
                    aria-current={isActive(item.href) ? 'page' : undefined}
                  >
                    <Icon className="h-4 w-4" aria-hidden="true" />
                    <span className="hidden lg:inline">{item.name.split(' ')[0]}</span>
                  </Link>
                </Button>
              );
            })}
          </div>

          {/* Mobile Menu - shown only on mobile */}
          <div className="md:hidden flex items-center space-x-2">
            <NotificationCenter userId="demo-user" />
            <Sheet open={isOpen} onOpenChange={setIsOpen}>
              <SheetTrigger asChild>
                <Button variant="ghost" size="icon" aria-label="Open menu">
                  <Menu className="h-5 w-5" />
                </Button>
              </SheetTrigger>
              <SheetContent side="right" className="w-[300px] sm:w-[400px]">
                <nav className="flex flex-col space-y-4" role="navigation" aria-label="Mobile navigation">
                  {navigation.map((item) => (
                    <Link
                      key={item.name}
                      to={item.href}
                      className={`text-lg font-medium transition-colors hover:text-primary focus:text-primary focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 rounded-sm ${
                        isActive(item.href) ? 'text-primary' : 'text-muted-foreground'
                      }`}
                      onClick={() => setIsOpen(false)}
                      aria-current={isActive(item.href) ? 'page' : undefined}
                    >
                      {item.name}
                    </Link>
                  ))}
                  
                  {/* AI Services Section */}
                  <div className="border-t pt-4">
                    <h3 className="text-md font-semibold mb-2">AI Career Tools</h3>
                    {aiServices.map((service) => {
                      const Icon = service.icon;
                      return (
                        <Link
                          key={service.name}
                          to={service.href}
                          className="flex items-center space-x-2 py-2 text-sm font-medium transition-colors hover:text-primary focus:text-primary focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 rounded-sm"
                          onClick={() => setIsOpen(false)}
                        >
                          <Icon className="h-4 w-4" aria-hidden="true" />
                          <span>{service.name}</span>
                        </Link>
                      );
                    })}
                  </div>
                  
                  <div className="border-t pt-4">
                    {dashboardLinks.map((item) => {
                      const Icon = item.icon;
                      return (
                        <Link
                          key={item.name}
                          to={item.href}
                          className="flex items-center space-x-2 py-2 text-lg font-medium transition-colors hover:text-primary focus:text-primary focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 rounded-sm"
                          onClick={() => setIsOpen(false)}
                          aria-current={isActive(item.href) ? 'page' : undefined}
                        >
                          <Icon className="h-5 w-5" aria-hidden="true" />
                          <span>{item.name}</span>
                        </Link>
                      );
                    })}
                  </div>
                </nav>
              </SheetContent>
            </Sheet>
          </div>
        </div>
      </div>
    </header>
  );
}