/**
 * API Client for MyBrand Job Application Platform
 * 
 * This module provides a centralized API client for communicating with
 * the backend services. It includes functions for job search, notifications,
 * skill gap analysis, and real-time communication via WebSocket.
 * 
 * @version 2.0
 * @author MyBrand Team
 */

// ============================================================================
// API CONFIGURATION
// Base URL and configuration settings for API communication
// ============================================================================

/**
 * API Base URL Configuration
 * 
 * The API base URL is determined in the following order:
 * 1. VITE_API_URL environment variable (for development)
 * 2. Default to localhost:8000
 */
const API_BASE_URL = process.env.VITE_API_URL || 'http://localhost:8000';

// ============================================================================
// SECURITY UTILITIES
// Helper functions for input sanitization and security
// ============================================================================

/**
 * Basic XSS sanitization function
 * 
 * Removes potentially dangerous HTML characters to prevent cross-site scripting attacks.
 * This is a basic implementation and should be supplemented with more robust
 * server-side validation.
 * 
 * @param str - The string to sanitize
 * @returns The sanitized string with HTML characters escaped
 */
function sanitizeHTML(str: string): string {
  return str.replace(/[<>]/g, function(match) {
    switch (match) {
      case '<': return '&lt;';
      case '>': return '&gt;';
      default: return match;
    }
  });
}

// ============================================================================
// DATA INTERFACES
// TypeScript interfaces for API data structures
// ============================================================================

/**
 * Job interface representing a job posting
 * 
 * Contains all relevant information about a job opportunity including
 * title, company, location, salary, and description.
 */
export interface Job {
  id: number;
  title: string;
  company: string;
  location: string;
  salary?: string;
  type: string;
  remote: boolean;
  urgent: boolean;
  description: string;
  requirements?: string[];
  benefits?: string[];
  posted: string;
  isNew: boolean;
}

/**
 * Job search request parameters
 * 
 * Optional parameters for filtering job search results
 */
export interface JobSearchRequest {
  keyword?: string;
  location?: string;
  jobType?: string;
  company?: string;
  remote?: boolean;
  limit?: number;
  offset?: number;
}

/**
 * Job search response structure
 * 
 * Contains job search results along with pagination information
 */
export interface JobSearchResponse {
  jobs: Job[];
  total: number;
  hasMore: boolean;
}

/**
 * Skill gap analysis request parameters
 * 
 * Contains resume text and job description for skill gap analysis
 */
export interface SkillGapRequest {
  resume_text: string;
  job_description: string;
}

/**
 * Skill gap analysis response structure
 * 
 * Contains analysis results including missing skills, matched skills,
 * skill gap score, and recommendations
 */
export interface SkillGapResponse {
  missing_skills: string[];
  matched_skills: string[];
  skill_gap_score: number;
  recommendations: string[];
}

/**
 * Notification request parameters
 * 
 * Contains information for sending a notification to a user
 */
export interface NotificationRequest {
  user_id: string;
  notification_type: string;
  title: string;
  message: string;
}

// ============================================================================
// API FUNCTIONS
// Functions for interacting with backend API endpoints
// ============================================================================

/**
 * Search for jobs with optional filtering parameters
 * 
 * This function queries the job search API endpoint with the provided
 * search parameters and returns matching job postings.
 * 
 * @param params - Job search parameters for filtering results
 * @returns Promise resolving to job search results
 * @throws Error if the API request fails
 * 
 * @example
 * ```typescript
 * const results = await searchJobs({
 *   keyword: 'software engineer',
 *   location: 'San Francisco',
 *   remote: true
 * });
 * console.log(`Found ${results.total} jobs`);
 * ```
 */
export const searchJobs = async (params: JobSearchRequest): Promise<JobSearchResponse> => {
  // Build query parameters from search request
  const queryParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      // Sanitize parameters to prevent XSS
      queryParams.append(key, sanitizeHTML(value.toString()));
    }
  });

  // Make API request to job search endpoint
  const response = await fetch(`${API_BASE_URL}/jobs/search?${queryParams}`);
  if (!response.ok) {
    throw new Error('Failed to search jobs');
  }
  return response.json();
};

/**
 * Send a notification to a user
 * 
 * This function sends a notification request to the notifications API
 * endpoint to deliver a message to a specific user.
 * 
 * @param request - Notification request parameters
 * @returns Promise resolving to API response
 * @throws Error if the API request fails
 * 
 * @example
 * ```typescript
 * await sendNotification({
 *   user_id: 'user123',
 *   notification_type: 'job_match',
 *   title: 'New Job Match',
 *   message: 'We found a job that matches your profile!'
 * });
 * ```
 */
export const sendNotification = async (request: NotificationRequest) => {
  // Sanitize request data to prevent XSS
  const sanitizedRequest = {
    ...request,
    title: sanitizeHTML(request.title),
    message: sanitizeHTML(request.message)
  };

  // Make API request to notifications endpoint
  const response = await fetch(`${API_BASE_URL}/notifications/send`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(sanitizedRequest),
  });
  if (!response.ok) {
    throw new Error('Failed to send notification');
  }
  return response.json();
};

/**
 * Analyze skill gaps between a resume and job description
 * 
 * This function sends a skill gap analysis request to the AI service
 * to compare a resume with a job description and identify gaps.
 * 
 * @param request - Skill gap analysis request parameters
 * @returns Promise resolving to skill gap analysis results
 * @throws Error if the API request fails
 * 
 * @example
 * ```typescript
 * const analysis = await analyzeSkillGaps({
 *   resume_text: 'Experienced developer with Python and React skills...',
 *   job_description: 'Looking for a senior developer with AWS experience...'
 * });
 * console.log(`Skill gap score: ${analysis.skill_gap_score}`);
 * ```
 */
export const analyzeSkillGaps = async (request: SkillGapRequest): Promise<SkillGapResponse> => {
  // Sanitize request data to prevent XSS
  const sanitizedRequest = {
    ...request,
    resume_text: sanitizeHTML(request.resume_text),
    job_description: sanitizeHTML(request.job_description)
  };

  // Make API request to skill gap analysis endpoint
  const response = await fetch(`${API_BASE_URL}/ai/skill-gap/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(sanitizedRequest),
  });
  
  if (!response.ok) {
    throw new Error('Failed to analyze skill gaps');
  }
  
  return response.json();
};

// ============================================================================
// WEBSOCKET FUNCTIONS
// Functions for real-time communication
// ============================================================================

/**
 * Create a WebSocket connection for real-time notifications
 * 
 * This function establishes a WebSocket connection to the notifications
 * service for receiving real-time updates and messages.
 * 
 * @param userId - User ID for the connection (defaults to 'anonymous')
 * @returns WebSocket connection instance
 * 
 * @example
 * ```typescript
 * const ws = createNotificationWebSocket('user123');
 * ws.onmessage = (event) => {
 *   console.log('Received notification:', event.data);
 * };
 * ```
 */
export const createNotificationWebSocket = (userId: string = 'anonymous') => {
  // Determine WebSocket protocol based on API URL protocol
  const wsProtocol = API_BASE_URL.startsWith('https') ? 'wss' : 'ws';
  const wsUrl = API_BASE_URL.replace(/^http(s?):/, `${wsProtocol}:`);
  
  // Create and return WebSocket connection
  return new WebSocket(`${wsUrl}/ws/notifications?user_id=${encodeURIComponent(userId)}`);
};

// ============================================================================
// DEFAULT EXPORT
// Export all functions as a default object for convenience
// ============================================================================

/**
 * Default export containing all API client functions
 * 
 * Provides a convenient way to import all API functions at once.
 */
export default {
  searchJobs,
  sendNotification,
  analyzeSkillGaps,
  createNotificationWebSocket,
  API_BASE_URL
};