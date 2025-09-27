/**
 * Skill Gap Analysis Client for MyBrand Job Application Platform
 * 
 * This module provides a client for interacting with the skill gap analysis API,
 * which compares resumes with job descriptions to identify skill gaps and provide
 * recommendations.
 * 
 * @version 2.0
 * @author MyBrand Team
 */

// ============================================================================
// DATA INTERFACES
// TypeScript interfaces for API data structures
// ============================================================================

/**
 * Skill gap analysis request parameters
 * 
 * Contains resume text and job description for skill gap analysis
 */
export interface SkillGapRequest {
  /** The text content of the user's resume */
  resume_text: string;
  
  /** The text content of the job description */
  job_description: string;
}

/**
 * Skill gap analysis response structure
 * 
 * Contains analysis results including missing skills, matched skills,
 * skill gap score, and recommendations
 */
export interface SkillGapResponse {
  /** List of skills missing from the resume */
  missing_skills: string[];
  
  /** List of skills that match between resume and job description */
  matched_skills: string[];
  
  /** Numerical score representing the skill gap (0-100) */
  skill_gap_score: number;
  
  /** List of recommendations for skill development */
  recommendations: string[];
}

// ============================================================================
// API FUNCTIONS
// Functions for interacting with the skill gap analysis API
// ============================================================================

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
  /**
   * Determine API base URL
   * 
   * Uses the VITE_API_URL environment variable if available,
   * otherwise falls back to localhost:8000
   */
  const apiBaseUrl = typeof process !== 'undefined' && process.env?.VITE_API_URL 
    ? process.env.VITE_API_URL 
    : 'http://localhost:8000';
    
  /**
   * Make API request to skill gap analysis endpoint
   * 
   * Sends the request data as JSON and handles the response
   */
  const response = await fetch(`${apiBaseUrl}/ai/skill-gap/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });
  
  // Handle API errors
  if (!response.ok) {
    throw new Error('Failed to analyze skill gaps');
  }
  
  // Return parsed response data
  return response.json();
};