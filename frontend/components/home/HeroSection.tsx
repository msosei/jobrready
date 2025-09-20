import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Search, MapPin, Sparkles } from 'lucide-react';

export default function HeroSection() {
  const [keyword, setKeyword] = useState('');
  const [location, setLocation] = useState('');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle search logic here
    console.log('Searching for:', { keyword, location });
  };

  return (
    <section className="relative bg-gradient-to-br from-primary/10 via-background to-secondary/10 py-20 lg:py-32">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-6">
            <Sparkles className="h-8 w-8 text-primary mr-2" />
            <span className="text-sm font-medium text-primary uppercase tracking-wide">
              AI-Powered Career Platform
            </span>
          </div>
          <h1 className="text-4xl lg:text-6xl font-bold mb-6">
            AI-powered job discovery
            <br />
            <span className="text-primary">and career tools</span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-8">
            Find your dream job with intelligent matching, get personalized career insights,
            and accelerate your professional journey with cutting-edge AI tools.
          </p>
        </div>

        <form onSubmit={handleSearch} className="max-w-4xl mx-auto">
          <div className="flex flex-col lg:flex-row gap-4 p-2 bg-background rounded-lg shadow-lg border">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-muted-foreground" />
              <Input
                type="text"
                placeholder="Job title, keywords, or company"
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
                className="pl-10 border-0 focus-visible:ring-0 text-lg h-12"
              />
            </div>
            <div className="flex-1 relative">
              <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-muted-foreground" />
              <Input
                type="text"
                placeholder="City, state, or remote"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                className="pl-10 border-0 focus-visible:ring-0 text-lg h-12"
              />
            </div>
            <Button type="submit" size="lg" className="px-8 h-12">
              Search Jobs
            </Button>
          </div>
        </form>

        <div className="flex justify-center mt-8">
          <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
            <span>Popular searches:</span>
            {['Software Engineer', 'Data Scientist', 'Product Manager', 'UX Designer'].map((term) => (
              <button
                key={term}
                className="px-3 py-1 bg-muted rounded-full hover:bg-muted/80 transition-colors"
              >
                {term}
              </button>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
