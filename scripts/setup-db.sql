-- Complete database setup script for MyBrand Job Application Platform
-- Run this in your Supabase SQL editor or local PostgreSQL instance

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create tables (from schema.sql)
\i ../config/schema.sql

-- Enable RLS and create policies (from rls.sql)
\i ../config/rls.sql

-- Insert sample data for development
INSERT INTO users (id, name, email, role) VALUES 
  ('550e8400-e29b-41d4-a716-446655440000', 'John Doe', 'john@example.com', 'user'),
  ('550e8400-e29b-41d4-a716-446655440001', 'Jane Smith', 'jane@example.com', 'user')
ON CONFLICT (id) DO NOTHING;

-- Insert sample subscription plans
INSERT INTO subscriptions (user_id, plan_type, start_date, end_date, quota_limits) VALUES 
  ('550e8400-e29b-41d4-a716-446655440000', 'pro', CURRENT_DATE, CURRENT_DATE + INTERVAL '1 month', 
   '{"applications": 50, "cover_letters": 50, "ai_requests": 200}'::jsonb),
  ('550e8400-e29b-41d4-a716-446655440001', 'free', CURRENT_DATE, CURRENT_DATE + INTERVAL '1 month',
   '{"applications": 5, "cover_letters": 5, "ai_requests": 20}'::jsonb)
ON CONFLICT DO NOTHING;

-- Insert sample jobs
INSERT INTO jobs_index (title, description, company, source, date_posted) VALUES 
  ('Senior Software Engineer', 'Build scalable web applications with React and Node.js', 'Tech Corp', 'internal', NOW()),
  ('Full Stack Developer', 'Work on exciting projects using modern technologies', 'Startup Inc', 'external', NOW()),
  ('Frontend Engineer', 'Create beautiful user interfaces with React and TypeScript', 'Design Co', 'internal', NOW())
ON CONFLICT DO NOTHING;

-- Insert sample usage counters
INSERT INTO usage_counters (user_id, applications_sent, cover_letters_generated, ai_requests) VALUES 
  ('550e8400-e29b-41d4-a716-446655440000', 12, 8, 45),
  ('550e8400-e29b-41d4-a716-446655440001', 3, 2, 8)
ON CONFLICT (user_id) DO NOTHING;

-- Verify setup
SELECT 'Database setup completed successfully!' as status;
