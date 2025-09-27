# Configuration Files Documentation

## Stripe Plans Configuration (stripe-plans.json)

This configuration file defines the subscription plans available for the JobReady platform.

### Structure

- `plans`: Object containing all available subscription plans
  - Each plan has:
    - `id`: Stripe price ID for the plan
    - `name`: Human-readable plan name
    - `price`: Price in cents (e.g., 2900 = $29.00)
    - `interval`: Billing interval ("month" or "year")
    - `features`: Object defining plan features and limits

### Plans

1. **Free Plan**
   - The basic tier with limited features and usage caps
   - Intended for users to try the platform before upgrading
   - Features:
     - 5 job applications per month
     - 5 cover letters per month
     - 20 AI requests per month
     - Access to application tailoring
     - Access to mock interview feature
     - No access to gap narratives
     - No access to portfolio projects
     - No access to personal website builder
     - No access to bulk application feature

2. **Pro Plan**
   - The mid-tier plan with expanded features and higher usage limits
   - Suitable for active job seekers who need more resources
   - Features:
     - 50 job applications per month
     - 50 cover letters per month
     - 200 AI requests per month
     - Access to application tailoring
     - Access to mock interview feature
     - Access to gap narratives
     - Access to portfolio projects
     - Access to personal website builder
     - No access to bulk application feature

3. **Premium Plan**
   - The highest tier with unlimited usage and all features unlocked
   - Designed for serious job seekers who want maximum platform capabilities
   - Features:
     - Unlimited job applications
     - Unlimited cover letters
     - Unlimited AI requests
     - Access to application tailoring
     - Access to mock interview feature
     - Access to gap narratives
     - Access to portfolio projects
     - Access to personal website builder
     - Access to bulk application feature