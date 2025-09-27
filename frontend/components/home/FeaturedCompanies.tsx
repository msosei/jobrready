/**
 * Featured Companies Component for MyBrand Job Application Platform
 * 
 * This component displays a grid of featured companies that are actively
 * hiring, encouraging users to explore opportunities at top organizations.
 * 
 * @version 2.0
 * @author MyBrand Team
 */

// ============================================================================
// IMPORT STATEMENTS
// React component and utility imports
// ============================================================================

import { Card } from '@/components/ui/card';

// ============================================================================
// DATA INTERFACES
// TypeScript interfaces for data structures
// ============================================================================

/**
 * Featured company data interface
 * 
 * Represents a company featured on the home page
 */
interface FeaturedCompany {
  /** Company name */
  name: string;
  
  /** Company logo URL */
  logo: string;
  
  /** Number of open job positions */
  openJobs: number;
}

// ============================================================================
// COMPONENT PROPS INTERFACE
// TypeScript interface for component properties
// ============================================================================

/**
 * Featured companies component props interface
 * 
 * Defines the properties for the featured companies component
 */
interface FeaturedCompaniesProps {}

// ============================================================================
// COMPONENT IMPLEMENTATION
// Main component function with comprehensive documentation
// ============================================================================

/**
 * Featured companies component for the home page
 * 
 * This component displays a grid of featured companies that are actively
 * hiring, encouraging users to explore opportunities at top organizations.
 * Each company card shows the company logo, name, and number of open positions.
 * 
 * @param props - Component properties
 * @returns JSX element representing the featured companies section
 * 
 * @example
 * ```tsx
 * <FeaturedCompanies />
 * ```
 */
export default function FeaturedCompanies() {
  // ============================================================================
  // MOCK DATA
  // Sample data for demonstration purposes
  // ============================================================================

  /** Sample featured companies data */
  const companies: FeaturedCompany[] = [
    { name: 'Google', logo: '/api/placeholder/120/60', openJobs: 45 },
    { name: 'Microsoft', logo: '/api/placeholder/120/60', openJobs: 32 },
    { name: 'Apple', logo: '/api/placeholder/120/60', openJobs: 28 },
    { name: 'Amazon', logo: '/api/placeholder/120/60', openJobs: 67 },
    { name: 'Meta', logo: '/api/placeholder/120/60', openJobs: 23 },
    { name: 'Netflix', logo: '/api/placeholder/120/60', openJobs: 15 },
    { name: 'Tesla', logo: '/api/placeholder/120/60', openJobs: 38 },
    { name: 'Spotify', logo: '/api/placeholder/120/60', openJobs: 19 },
  ];

  // ============================================================================
  // MAIN RENDER
  // Primary component render function
  // ============================================================================

  /**
   * Render the featured companies component
   * 
   * Returns the complete featured companies section UI with company cards
   */
  return (
    <section className="container mx-auto px-4 sm:px-6 lg:px-8">
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold mb-4">Featured Companies</h2>
        <p className="text-lg text-muted-foreground">
          Discover opportunities at top companies actively hiring
        </p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
        {companies.map((company) => (
          <Card
            key={company.name}
            className="p-6 text-center hover:shadow-lg transition-shadow cursor-pointer group"
          >
            <img
              src={company.logo}
              alt={company.name}
              className="w-16 h-8 mx-auto mb-3 object-contain opacity-60 group-hover:opacity-100 transition-opacity"
            />
            <h3 className="font-semibold text-sm mb-1">{company.name}</h3>
            <p className="text-xs text-muted-foreground">
              {company.openJobs} open positions
            </p>
          </Card>
        ))}
      </div>
    </section>
  );
}