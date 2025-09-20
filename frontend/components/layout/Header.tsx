import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { Menu, BrainCircuit, User, Building2, Shield } from 'lucide-react';
import NotificationCenter from '../common/NotificationCenter';

export default function Header() {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  // Request notification permission on mount
  useEffect(() => {
    if ('Notification' in window && Notification.permission === 'default') {
      Notification.requestPermission();
    }
  }, []);

  const navigation = [
    { name: 'Home', href: '/' },
    { name: 'Jobs', href: '/jobs' },
    { name: 'AI Career Tools', href: '/ai-career-tools' },
  ];

  const dashboardLinks = [
    { name: 'Candidate Dashboard', href: '/candidate/dashboard', icon: User },
    { name: 'Employer Dashboard', href: '/employer/dashboard', icon: Building2 },
    { name: 'Admin Dashboard', href: '/admin/dashboard', icon: Shield },
  ];

  const isActive = (href: string) => location.pathname === href;

  return (
    <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <BrainCircuit className="h-8 w-8 text-primary" />
              <span className="text-xl font-bold">JobBoard Pro</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
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
          </nav>

          {/* Desktop Dashboard Links & Notifications */}
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

          {/* Mobile Menu */}
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
