import { ErrorBoundary } from '../components/common/ErrorBoundary';
import SEOHead from '../components/seo/SEOHead';
import HeroSection from '../components/home/HeroSection';
import FeaturedCompanies from '../components/home/FeaturedCompanies';
import TrendingJobs from '../components/home/TrendingJobs';
import JobFeedPreview from '../components/home/JobFeedPreview';
import AIToolsTeaser from '../components/home/AIToolsTeaser';

export default function HomePage() {
  return (
    <ErrorBoundary>
      <SEOHead />
      <main className="space-y-16 pb-16">
        <HeroSection />
        <FeaturedCompanies />
        <TrendingJobs />
        <JobFeedPreview />
        <AIToolsTeaser />
      </main>
    </ErrorBoundary>
  );
}
