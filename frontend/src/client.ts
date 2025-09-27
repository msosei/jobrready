/*
 * Custom API Client for the MyBrand Job Application Platform
 * 
 * This file provides a simplified interface for interacting with the backend API.
 * It includes functions for job search, notifications, skill gap analysis, and real-time communication.
 * 
 * The client is designed to work with the FastAPI backend and provides:
 * 1. Type-safe API calls with proper error handling
 * 2. Environment-based configuration for different deployment contexts
 * 3. WebSocket support for real-time notifications
 * 4. Consistent error handling and response parsing
 */

/**
 * API Base URL Configuration
 * 
 * The API base URL is determined in the following order:
 * 1. VITE_API_URL environment variable (for development)
 * 2. Default to localhost:8000
 */
const API_BASE_URL = import.meta.env?.VITE_API_URL || 'http://localhost:8000';

// Validate that we have a proper API base URL
if (!API_BASE_URL || API_BASE_URL === 'undefined') {
  console.warn('API_BASE_URL is not properly configured. Using default URL.');
}

/*
 * Type definitions for API responses and requests
 * 
 * These interfaces define the structure of data exchanged with the backend API.
 * They provide type safety and documentation for the expected data formats.
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

export interface JobSearchRequest {
  keyword?: string;
  location?: string;
  jobType?: string;
  company?: string;
  remote?: boolean;
  limit?: number;
  offset?: number;
}

export interface JobSearchResponse {
  jobs: Job[];
  total: number;
  hasMore: boolean;
}

export interface SkillGapRequest {
  resume_text: string;
  job_description: string;
}

export interface SkillGapResponse {
  missing_skills: string[];
  matched_skills: string[];
  skill_gap_score: number;
  recommendations: string[];
}

/*
 * Job Search API Functions
 * 
 * These functions provide a clean interface for searching jobs through the backend API.
 * They handle parameter serialization, API calls, and response parsing.
 */

/**
 * Search for jobs based on provided criteria
 * 
 * @param params - Search parameters including keyword, location, job type, etc.
 * @returns Promise resolving to job search results
 * @throws Error if the API request fails
 */
export const searchJobs = async (params: JobSearchRequest): Promise<JobSearchResponse> => {
  const queryParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      queryParams.append(key, value.toString());
    }
  });

  const response = await fetch(`${API_BASE_URL}/jobs/search?${queryParams}`);
  if (!response.ok) {
    throw new Error('Failed to search jobs');
  }
  return response.json();
};

/*
 * Notification API Functions
 * 
 * These functions handle sending notifications through the backend API.
 * They provide a simple interface for triggering notifications for testing purposes.
 */

/**
 * Send a notification to a user
 * 
 * @param userId - ID of the user to send notification to
 * @param type - Type of notification
 * @param title - Notification title
 * @param message - Notification message content
 * @returns Promise resolving to API response
 * @throws Error if the API request fails
 */
export const sendNotification = async (
  userId: string,
  type: string,
  title: string,
  message: string
) => {
  const response = await fetch(`${API_BASE_URL}/notifications/send`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id: userId, notification_type: type, title, message }),
  });
  if (!response.ok) {
    throw new Error('Failed to send notification');
  }
  return response.json();
};

/*
 * Skill Gap Analysis API Functions
 * 
 * These functions provide interfaces for analyzing skill gaps between resumes and job descriptions.
 * They handle the communication with the AI-powered skill gap analysis service.
 */

/**
 * Analyze skill gaps between a resume and job description
 * 
 * @param request - Object containing resume text and job description
 * @returns Promise resolving to skill gap analysis results
 * @throws Error if the API request fails
 */
export const analyzeSkillGaps = async (request: SkillGapRequest): Promise<SkillGapResponse> => {
  const response = await fetch(`${API_BASE_URL}/ai/skill-gap/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });
  
  if (!response.ok) {
    throw new Error('Failed to analyze skill gaps');
  }
  
  return response.json();
};

/*
 * WebSocket Functions for Real-time Communication
 * 
 * These functions establish WebSocket connections for real-time notifications.
 * They handle the protocol conversion from HTTP to WebSocket URLs.
 */

/**
 * Create a WebSocket connection for real-time notifications
 * 
 * @param userId - ID of the user to receive notifications for (defaults to 'anonymous')
 * @returns WebSocket connection instance
 */
export const createNotificationWebSocket = (userId: string = 'anonymous') => {
  return new WebSocket(`${API_BASE_URL.replace('http', 'ws')}/ws/notifications?user_id=${userId}`);
};