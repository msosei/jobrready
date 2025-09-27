/**
 * Main Application Component
 * Version: 1.0
 * Purpose: Entry point for the JobReady application with routing and providers
 * 
 * This component serves as the root of the application and provides:
 * 1. Routing configuration for all application pages
 * 2. Query client provider for data fetching and caching
 * 3. Error boundary for handling application errors
 * 4. Helmet provider for managing document head elements
 * 5. Layout components (Header, Footer) that persist across routes
 */

// ============================================================================
// IMPORT STATEMENTS
// React, routing, and third-party library imports
// ============================================================================

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { HelmetProvider } from 'react-helmet-async';
import { Toaster } from '@/components/ui/toaster';

// ============================================================================
// COMPONENT IMPORTS
// Custom components and page components
// ============================================================================

// ----------------------------------------------------------------------------
// UTILITY COMPONENTS
// Shared utility and layout components
// ----------------------------------------------------------------------------

import { ErrorBoundary } from './components/common/ErrorBoundary';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import PageTransition from './components/common/PageTransition';

// ----------------------------------------------------------------------------
// PAGE COMPONENTS
// All application page components
// ----------------------------------------------------------------------------

import HomePage from './pages/HomePage';
import JobsPage from './pages/JobsPage';
import CompanyProfilePage from './pages/CompanyProfilePage';
import CandidateDashboard from './pages/CandidateDashboard';
import EmployerDashboard from './pages/EmployerDashboard';
import AdminDashboard from './pages/AdminDashboard';
import AICareerToolsPage from './pages/AICareerToolsPage';

// ============================================================================
// AI MICROSERVICE PAGES
// Dedicated pages for each AI microservice
// ============================================================================

import AISkillGapPage from './pages/AISkillGapPage';

// Placeholder components for other AI microservice pages
const AIResumeBuilderPage = () => <div className="container mx-auto py-8">Resume Builder Page</div>;
const AIResumeEnhancerPage = () => <div className="container mx-auto py-8">Resume Enhancer Page</div>;
const AIInterviewCoachPage = () => <div className="container mx-auto py-8">Interview Coach Page</div>;
const AIMockInterviewerPage = () => <div className="container mx-auto py-8">Mock Interviewer Page</div>;
const AIJobMatcherPage = () => <div className="container mx-auto py-8">Job Matcher Page</div>;
const AIJobRecommenderPage = () => <div className="container mx-auto py-8">Job Recommender Page</div>;
const AIDocumentSummarizerPage = () => <div className="container mx-auto py-8">Document Summarizer Page</div>;
const AICourseRecommenderPage = () => <div className="container mx-auto py-8">Course Recommender Page</div>;
const AISalaryPredictorPage = () => <div className="container mx-auto py-8">Salary Predictor Page</div>;
const AIDiversityInsightsPage = () => <div className="container mx-auto py-8">Diversity Insights Page</div>;
const AIMultiLanguagePage = () => <div className="container mx-auto py-8">Multi-Language Page</div>;
const AIVoiceAgentPage = () => <div className="container mx-auto py-8">Voice Agent Page</div>;
const AICareerChatbotPage = () => <div className="container mx-auto py-8">Career Chatbot Page</div>;

// ============================================================================
// QUERY CLIENT CONFIGURATION
// Configure React Query client with default options
// ============================================================================

/**
 * Query client configuration with custom default options
 * - retry: Retry failed queries up to 3 times with exponential backoff
 * - staleTime: Cache data for 5 minutes before considering it stale
 * - gcTime: Keep unused data in cache for 10 minutes
 */
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 3,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
      staleTime: 5 * 60 * 1000, // 5 minutes
      gcTime: 10 * 60 * 1000, // 10 minutes (formerly cacheTime)
    },
  },
});

// ============================================================================
// MAIN APPLICATION COMPONENT
// Root component that wraps the entire application
// ============================================================================

/**
 * Main App component that serves as the root of the application
 * 
 * @returns {JSX.Element} The complete application with routing and providers
 */
export default function App() {
  // ----------------------------------------------------------------------------
  // APPLICATION STRUCTURE
  // Main application layout with providers, routing, and layout components
  // ----------------------------------------------------------------------------
  
  return (
    // Helmet provider for managing document head elements
    <HelmetProvider>
      {/* Query client provider for data fetching and caching */}
      <QueryClientProvider client={queryClient}>
        {/* Router for application navigation */}
        <Router>
          {/* Error boundary to catch and handle application errors */}
          <ErrorBoundary>
            {/* Main application container with flex layout */}
            <div className="min-h-screen bg-background text-foreground flex flex-col">
              {/* Header that persists across all routes */}
              <Header />
              
              {/* Main content area where routed components are rendered */}
              <main className="flex-1" role="main">
                {/* Route definitions for all application pages with smooth transitions */}
                <Routes>
                  <Route path="/" element={<PageTransition><HomePage /></PageTransition>} />
                  <Route path="/jobs" element={<PageTransition><JobsPage /></PageTransition>} />
                  <Route path="/company/:id" element={<PageTransition><CompanyProfilePage /></PageTransition>} />
                  <Route path="/candidate/dashboard" element={<PageTransition><CandidateDashboard /></PageTransition>} />
                  <Route path="/employer/dashboard" element={<PageTransition><EmployerDashboard /></PageTransition>} />
                  <Route path="/admin/dashboard" element={<PageTransition><AdminDashboard /></PageTransition>} />
                  <Route path="/ai-career-tools" element={<PageTransition><AICareerToolsPage /></PageTransition>} />
                  
                  {/* AI Microservice Routes */}
                  <Route path="/ai/skill-gap" element={<PageTransition><AISkillGapPage /></PageTransition>} />
                  <Route path="/ai/resume-builder" element={<PageTransition><AIResumeBuilderPage /></PageTransition>} />
                  <Route path="/ai/resume-enhancer" element={<PageTransition><AIResumeEnhancerPage /></PageTransition>} />
                  <Route path="/ai/interview-coach" element={<PageTransition><AIInterviewCoachPage /></PageTransition>} />
                  <Route path="/ai/mock-interviewer" element={<PageTransition><AIMockInterviewerPage /></PageTransition>} />
                  <Route path="/ai/job-matcher" element={<PageTransition><AIJobMatcherPage /></PageTransition>} />
                  <Route path="/ai/job-recommender" element={<PageTransition><AIJobRecommenderPage /></PageTransition>} />
                  <Route path="/ai/document-summarizer" element={<PageTransition><AIDocumentSummarizerPage /></PageTransition>} />
                  <Route path="/ai/course-recommender" element={<PageTransition><AICourseRecommenderPage /></PageTransition>} />
                  <Route path="/ai/salary-predictor" element={<PageTransition><AISalaryPredictorPage /></PageTransition>} />
                  <Route path="/ai/diversity-insights" element={<PageTransition><AIDiversityInsightsPage /></PageTransition>} />
                  <Route path="/ai/multi-language" element={<PageTransition><AIMultiLanguagePage /></PageTransition>} />
                  <Route path="/ai/voice-agent" element={<PageTransition><AIVoiceAgentPage /></PageTransition>} />
                  <Route path="/ai/career-chatbot" element={<PageTransition><AICareerChatbotPage /></PageTransition>} />
                </Routes>
              </main>
              
              {/* Footer that persists across all routes */}
              <Footer />
              
              {/* Toast notification component for user feedback */}
              <Toaster />
            </div>
          </ErrorBoundary>
        </Router>
      </QueryClientProvider>
    </HelmetProvider>
  );
}