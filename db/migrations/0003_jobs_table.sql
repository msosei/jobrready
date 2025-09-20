-- Create jobs table
CREATE TABLE IF NOT EXISTS jobs (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  company TEXT NOT NULL,
  location TEXT NOT NULL,
  salary TEXT,
  type TEXT NOT NULL,
  remote BOOLEAN NOT NULL DEFAULT FALSE,
  urgent BOOLEAN NOT NULL DEFAULT FALSE,
  description TEXT NOT NULL,
  requirements TEXT[],
  benefits TEXT[],
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_jobs_title ON jobs(title);
CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company);
CREATE INDEX IF NOT EXISTS idx_jobs_location ON jobs(location);
CREATE INDEX IF NOT EXISTS idx_jobs_type ON jobs(type);
CREATE INDEX IF NOT EXISTS idx_jobs_created_at ON jobs(created_at);

-- Insert sample data
INSERT INTO jobs (title, company, location, salary, type, remote, urgent, description, requirements, benefits, expires_at) VALUES
('Senior Software Engineer', 'TechCorp Inc.', 'San Francisco, CA', '$120k - $160k', 'Full-time', true, false, 'Join our team to build scalable web applications using React, Node.js, and cloud technologies. You will work on exciting projects that impact millions of users.', '{"5+ years of software development experience", "Proficiency in React and Node.js", "Experience with cloud platforms", "Strong problem-solving skills"}', '{"Health insurance", "Stock options", "Remote work", "Unlimited PTO"}', CURRENT_TIMESTAMP + INTERVAL '30 days'),
('Data Scientist', 'DataFlow Analytics', 'Remote', '$110k - $140k', 'Full-time', true, true, 'Work with machine learning models and big data to derive actionable insights for our clients. You will be responsible for building predictive models and data pipelines.', '{"PhD or Masters in Data Science/Statistics", "Experience with Python and R", "Machine learning expertise", "SQL proficiency"}', '{"Flexible hours", "Learning budget", "Health benefits", "Work from anywhere"}', CURRENT_TIMESTAMP + INTERVAL '45 days'),
('UX Designer', 'Design Studio', 'New York, NY', '$80k - $110k', 'Full-time', false, false, 'Create beautiful and intuitive user experiences for our digital products. You will work closely with product managers and developers to bring designs to life.', '{"3+ years of UX design experience", "Proficiency in Figma and Sketch", "User research skills", "Portfolio of design work"}', '{"Creative environment", "Design tools budget", "Health insurance", "Professional development"}', CURRENT_TIMESTAMP + INTERVAL '60 days'),
('DevOps Engineer', 'CloudTech', 'Austin, TX', '$100k - $130k', 'Full-time', true, false, 'Manage cloud infrastructure and deployment pipelines using modern DevOps practices. You will help scale our systems to support millions of users.', '{"Experience with AWS/Azure/GCP", "Kubernetes and Docker expertise", "CI/CD pipeline experience", "Infrastructure as Code"}', '{"Cloud training", "Certification reimbursement", "Flexible work", "Health benefits"}', CURRENT_TIMESTAMP + INTERVAL '25 days'),
('Product Manager', 'InnovateCo', 'Seattle, WA', '$130k - $170k', 'Full-time', false, true, 'Lead product strategy and development initiatives for our cutting-edge SaaS platform. You will work with cross-functional teams to deliver exceptional user experiences.', '{"5+ years of product management experience", "Technical background preferred", "Experience with Agile methodologies", "Strong analytical skills"}', '{"Equity package", "Health insurance", "Learning stipend", "Team retreats"}', CURRENT_TIMESTAMP + INTERVAL '20 days'),
('Frontend Developer', 'WebSolutions', 'Remote', '$70k - $95k', 'Contract', true, false, 'Build responsive web applications with React and modern JavaScript. You will work on client projects ranging from startups to enterprise applications.', '{"3+ years of frontend development", "React and TypeScript expertise", "Responsive design skills", "Git workflow experience"}', '{"Project bonuses", "Flexible schedule", "Remote work", "Skill development"}', CURRENT_TIMESTAMP + INTERVAL '40 days'),
('Marketing Manager', 'GrowthHackers', 'Los Angeles, CA', '$85k - $115k', 'Full-time', false, false, 'Drive marketing campaigns and brand awareness for our fast-growing startup. You will lead digital marketing initiatives and analyze campaign performance.', '{"Marketing degree or equivalent experience", "Digital marketing expertise", "Analytics and data-driven approach", "Creative thinking"}', '{"Marketing budget", "Conference attendance", "Health benefits", "Growth opportunities"}', CURRENT_TIMESTAMP + INTERVAL '35 days'),
('Security Engineer', 'SecureNet', 'Washington, DC', '$115k - $145k', 'Full-time', true, true, 'Implement security measures and protocols to protect our systems and data. You will conduct security assessments and respond to incidents.', '{"Cybersecurity certifications", "Penetration testing experience", "Security frameworks knowledge", "Incident response skills"}', '{"Security training", "Certification support", "Health insurance", "Bonus structure"}', CURRENT_TIMESTAMP + INTERVAL '15 days'),
('Machine Learning Engineer', 'AI Innovations', 'Remote', '$140k - $180k', 'Full-time', true, true, 'Build and deploy machine learning models at scale. You will work on cutting-edge AI projects that push the boundaries of what is possible.', '{"PhD in Computer Science or related field", "Deep learning expertise", "MLOps experience", "Python and TensorFlow/PyTorch"}', '{"Research time", "Conference speaking", "Stock options", "Top-tier health benefits"}', CURRENT_TIMESTAMP + INTERVAL '50 days'),
('Product Designer', 'Design Studio', 'New York, NY', '$90k - $120k', 'Full-time', false, false, 'Design end-to-end product experiences that delight our users. You will work on both web and mobile applications across various industries.', '{"4+ years of product design experience", "Design systems expertise", "User research skills", "Prototyping abilities"}', '{"Design tools", "Creative workspace", "Health benefits", "Design conferences"}', CURRENT_TIMESTAMP + INTERVAL '28 days'),
('Junior Developer', 'TechStartup', 'Remote', '$50k - $70k', 'Full-time', true, false, 'Start your career in software development with mentorship from senior engineers. You will work on real projects while learning industry best practices.', '{"Computer Science degree or bootcamp", "Basic programming knowledge", "Eagerness to learn", "Problem-solving skills"}', '{"Mentorship program", "Learning resources", "Health insurance", "Flexible hours"}', CURRENT_TIMESTAMP + INTERVAL '60 days'),
('Sales Manager', 'SalesForce Pro', 'Chicago, IL', '$95k - $125k', 'Full-time', false, false, 'Lead our sales team to achieve revenue targets and expand our customer base. You will develop sales strategies and coach team members.', '{"Sales management experience", "CRM software proficiency", "Team leadership skills", "Revenue growth track record"}', '{"Commission structure", "Sales bonuses", "Health benefits", "Team incentives"}', CURRENT_TIMESTAMP + INTERVAL '45 days');