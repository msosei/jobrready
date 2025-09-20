import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { HelmetProvider } from 'react-helmet-async';
import { Toaster } from '@/components/ui/toaster';
import { ErrorBoundary } from './components/common/ErrorBoundary';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import HomePage from './pages/HomePage';
import JobsPage from './pages/JobsPage';
import CompanyProfilePage from './pages/CompanyProfilePage';
import CandidateDashboard from './pages/CandidateDashboard';
import EmployerDashboard from './pages/EmployerDashboard';
import AdminDashboard from './pages/AdminDashboard';
import AICareerToolsPage from './pages/AICareerToolsPage';

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

export default function App() {
  return (
    <HelmetProvider>
      <QueryClientProvider client={queryClient}>
        <Router>
          <ErrorBoundary>
            <div className="min-h-screen bg-background text-foreground flex flex-col">
              <Header />
              <main className="flex-1" role="main">
                <Routes>
                  <Route path="/" element={<HomePage />} />
                  <Route path="/jobs" element={<JobsPage />} />
                  <Route path="/company/:id" element={<CompanyProfilePage />} />
                  <Route path="/candidate/dashboard" element={<CandidateDashboard />} />
                  <Route path="/employer/dashboard" element={<EmployerDashboard />} />
                  <Route path="/admin/dashboard" element={<AdminDashboard />} />
                  <Route path="/ai-career-tools" element={<AICareerToolsPage />} />
                </Routes>
              </main>
              <Footer />
              <Toaster />
            </div>
          </ErrorBoundary>
        </Router>
      </QueryClientProvider>
    </HelmetProvider>
  );
}
