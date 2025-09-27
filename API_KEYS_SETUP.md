# API Keys Setup Guide

This document explains how to properly configure API keys for the MyBrand Job Application Platform.

## Environment Files

The project uses several environment files for configuration:

1. `.env` - Main environment file in the project root
2. `.env.local` - Local environment file (gitignored, for actual values)
3. `config/.env` - Configuration environment file
4. `frontend/.env.development` - Frontend development environment

## Required API Keys

### 1. Supabase
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_ANON_KEY`: Anonymous key for client-side operations
- `SUPABASE_SERVICE_ROLE`: Service role key for server-side operations
- `VITE_SUPABASE_URL`: Same as SUPABASE_URL (for frontend)
- `VITE_SUPABASE_ANON_KEY`: Same as SUPABASE_ANON_KEY (for frontend)

### 2. Stripe
- `STRIPE_SECRET_KEY`: Your Stripe secret key
- `STRIPE_WEBHOOK_SECRET`: Webhook secret for verifying events

### 3. OpenAI
- `OPENAI_API_KEY`: Your OpenAI API key for AI microservices

### 4. Application URLs
- `APP_URL`: Frontend URL (default: http://localhost:3000)
- `API_URL`: Backend API URL (default: http://localhost:8000)

### 5. Security
- `JWT_SECRET`: Secret key for JWT token signing

## Setup Instructions

### 1. Create your .env.local file
Copy the .env.local file and replace placeholder values with your actual API keys:

```bash
cp .env.local .env.local.actual
# Edit .env.local.actual with your real API keys
```

### 2. Supabase Setup
1. Create a Supabase project at https://supabase.com/
2. Get your project URL and keys from the Supabase dashboard
3. Update the following variables:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE`
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`

### 3. Stripe Setup
1. Create a Stripe account at https://stripe.com/
2. Get your API keys from the Stripe dashboard
3. Update the following variables:
   - `STRIPE_SECRET_KEY`
   - `STRIPE_WEBHOOK_SECRET`

### 4. OpenAI Setup
1. Create an OpenAI account at https://platform.openai.com/
2. Generate an API key
3. Update the following variable:
   - `OPENAI_API_KEY`

### 5. Docker Compose Configuration
The docker-compose.yml file is already configured to use environment variables:

```yaml
backend:
  environment:
    - SUPABASE_URL=${SUPABASE_URL}
    - SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
    - SUPABASE_SERVICE_ROLE=${SUPABASE_SERVICE_ROLE}
    - STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
    - OPENAI_API_KEY=${OPENAI_API_KEY}
```

## Testing Your Configuration

After setting up your API keys, you can test the configuration:

1. Start the services:
```bash
docker compose up -d
```

2. Check that services are running:
```bash
docker compose ps
```

3. Test API endpoints that require authentication or external services.

## Security Best Practices

1. Never commit actual API keys to version control
2. Use .env.local for local development (it's in .gitignore)
3. Use different keys for development and production
4. Rotate API keys regularly
5. Restrict API key permissions to only what's needed

## Troubleshooting

### Common Issues

1. **Services not starting**: Check that all required environment variables are set
2. **API calls failing**: Verify API keys are correct and have proper permissions
3. **Frontend not connecting**: Ensure VITE_* variables are correctly set

### Checking Environment Variables

You can verify environment variables are loaded correctly:

```bash
# Check Docker environment
docker compose exec backend env

# Check frontend environment
cd frontend && cat .env.development
```

## Additional Notes

- The frontend uses VITE_* prefixed variables which are exposed to the client
- Backend variables without VITE_* prefix are server-side only
- Make sure to restart services after updating environment variables