/**
 * Home Page for MyBrand Job Application Platform
 * 
 * This is the main landing page of the application that serves as the
 * entry point for users, featuring key sections like hero, featured
 * companies, trending jobs, and AI tools.
 * 
 * @version 2.0
 * @author MyBrand Team
 */

// ============================================================================
// IMPORT STATEMENTS
// Component and utility imports
// ============================================================================

import { ErrorBoundary } from '../components/common/ErrorBoundary';
import SEOHead from '../components/seo/SEOHead';
import HeroSection from '../components/home/HeroSection';
import FeaturedCompanies from '../components/home/FeaturedCompanies';
import TrendingJobs from '../components/home/TrendingJobs';
import JobFeedPreview from '../components/home/JobFeedPreview';
import AIToolsTeaser from '../components/home/AIToolsTeaser';

// ============================================================================
// PAGE COMPONENT
// Main page component implementation
// ============================================================================

/**
 * Home page component for the job application platform
 * 
 * This component serves as the main landing page, orchestrating various
 * sections to provide an overview of the platform's features and content.
 * It includes error boundary protection and SEO optimization.
 * 
 * @returns JSX element representing the home page
 * 
 * @example
 * ```tsx
 * <HomePage />
 * ```
 */
export default function HomePage() {
  /**
   * Render the home page
   * 
   * Returns the main page structure with all home page sections
   * wrapped in an error boundary for robustness.
   */
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