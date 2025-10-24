# 🚀 Development & Deployment Workflow

Complete guide for managing development and production deployments of BleedRate.

## 📋 Branch Strategy

We use a **two-branch strategy**:

- **`main`** - Production environment (live site)
- **`dev`** - Development/staging environment (for testing)

## 🏗️ Architecture Overview

### Environments

| Environment | Branch | URL | Auto-Deploy | Database |
|-------------|--------|-----|-------------|----------|
| **Production** | `main` | https://bleedrate.up.railway.app | ✅ Yes | `sa-tax-production.db` |
| **Development** | `dev` | https://bleedrate-dev.up.railway.app | ✅ Yes | `sa-tax-development.db` |

## 🛠️ Setup Instructions

### 1. Initial Railway Setup

#### Create Two Services in Railway

1. **Production Service**
   - Go to Railway dashboard
   - Create new service from GitHub repo
   - Name: `bleedrate-production`
   - Branch: `main`
   - Set environment variables:
     ```bash
     ENVIRONMENT=production
     DEBUG=false
     ENABLE_ADS=true
     SECRET_KEY=<your-production-secret>
     # ... other production vars
     ```

2. **Development Service**
   - Create another service in the same project
   - Name: `bleedrate-development`
   - Branch: `dev`
   - Set environment variables:
     ```bash
     ENVIRONMENT=development
     DEBUG=true
     ENABLE_ADS=false
     ADMIN_ENABLED=true
     SECRET_KEY=<your-dev-secret>
     # ... other development vars
     ```

### 2. Environment Variables

Create `.env` files for each environment:

**.env.production**
```bash
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=<production-database-url>
SECRET_KEY=<strong-secret-key>
ENABLE_ADS=true
ENABLE_SUBMISSION_LOGGING=true
SUPABASE_URL=<your-supabase-url>
SUPABASE_KEY=<your-supabase-key>
GOOGLE_ADSENSE_CLIENT_ID=<your-adsense-id>
```

**.env.development**
```bash
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=sqlite:///./db/sa-tax-development.db
SECRET_KEY=dev-secret-key
ENABLE_ADS=false
ENABLE_SUBMISSION_LOGGING=false
ADMIN_ENABLED=true
```

## 📦 Development Workflow

### Working on Features

```bash
# 1. Switch to dev branch
make switch-to-dev
# or: git checkout dev

# 2. Create a feature branch (optional but recommended)
git checkout -b feature/my-new-feature

# 3. Make your changes
# ... edit files ...

# 4. Test locally
make dev
# Visit http://localhost:8000

# 5. Run tests
make test

# 6. Commit changes
git add .
git commit -m "feat: add new feature"

# 7. Merge to dev
git checkout dev
git merge feature/my-new-feature

# 8. Deploy to development
make deploy-dev
```

### Testing Changes

```bash
# Run local development server
make dev

# Run in Docker (simulates production)
docker-compose -f docker-compose.dev.yml up

# Run tests
make test

# Check formatting
make lint
```

## 🚀 Deployment Commands

### Deploy to Development

```bash
make deploy-dev
```

This will:
1. Switch to `dev` branch
2. Push to GitHub
3. Trigger Railway deployment
4. Available at: https://bleedrate-dev.up.railway.app

### Deploy to Production

```bash
make deploy-prod
```

This will:
1. Switch to `main` branch
2. Push to GitHub
3. Trigger Railway deployment
4. Available at: https://bleedrate.up.railway.app

### Promote Dev to Production

When you're satisfied with dev, promote it:

```bash
make promote-to-prod
```

This will:
1. Ask for confirmation
2. Merge `dev` into `main`
3. Push to GitHub
4. Auto-deploy to production

## 🔍 Monitoring & Health Checks

### Health Check Endpoints

Both environments have health check endpoints:

**Production:**
```bash
curl https://bleedrate.up.railway.app/health
```

**Development:**
```bash
curl https://bleedrate-dev.up.railway.app/health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development",
  "debug": true
}
```

### Railway Dashboard

Monitor deployments in Railway:
- Build logs
- Runtime logs
- Metrics (CPU, Memory, Network)
- Health checks

## 🧪 CI/CD Pipeline

GitHub Actions automatically runs on every push:

### Tests Workflow

Triggers on: `push` or `pull_request` to `main` or `dev`

Runs:
1. ✅ Unit tests with coverage
2. ✅ Code formatting check (Black)
3. ✅ Linting (Ruff)

View results: GitHub → Actions tab

## 🐳 Docker Development

### Run Development Container

```bash
docker-compose -f docker-compose.dev.yml up
```

Includes:
- Hot reload on code changes
- Port 8001 (to avoid conflicts)
- Development database
- SQLite database viewer on port 8002

### With Database Viewer

```bash
docker-compose -f docker-compose.dev.yml --profile tools up
```

Access:
- App: http://localhost:8001
- DB Viewer: http://localhost:8002

## 🔄 Git Workflow

### Branching Model

```
main (production)
 ↑
 └── dev (staging)
      ↑
      └── feature/xyz (feature branches)
```

### Best Practices

1. **Never commit directly to `main`**
   - Always work in `dev` or feature branches
   - Use `make promote-to-prod` to deploy to production

2. **Test in dev first**
   - All changes should be tested in dev environment
   - Get approval before promoting to production

3. **Use meaningful commit messages**
   ```bash
   feat: add new calculator
   fix: correct VAT calculation
   docs: update deployment guide
   chore: update dependencies
   ```

4. **Keep branches synchronized**
   ```bash
   # Update dev with latest from main
   git checkout dev
   git merge main
   git push origin dev
   ```

## 🐛 Troubleshooting

### Deployment Failed

```bash
# Check Railway logs
# Railway Dashboard → Service → Deployments → View logs

# Test locally with production settings
ENVIRONMENT=production DEBUG=false make dev
```

### Database Issues

```bash
# Reset development database
rm db/sa-tax-development.db
make dev
```

### Health Check Failing

```bash
# Test locally
curl http://localhost:8000/health

# Check Railway environment variables
# Ensure ENVIRONMENT is set correctly
```

### Code Not Updating

```bash
# Force Railway rebuild
# Railway Dashboard → Service → Settings → Redeploy

# Or commit an empty change
git commit --allow-empty -m "trigger rebuild"
git push origin dev
```

## 📊 Monitoring Checklist

Before promoting to production:

- [ ] All tests pass (`make test`)
- [ ] Code is formatted (`make format`)
- [ ] No linting errors (`make lint`)
- [ ] Tested in dev environment
- [ ] Health check responds correctly
- [ ] Database migrations applied (if any)
- [ ] Environment variables updated in Railway
- [ ] Reviewed recent changes
- [ ] Backup of production database (if significant changes)

## 🔐 Security Notes

1. **Never commit sensitive data**
   - Use environment variables
   - Keep `.env` files in `.gitignore`

2. **Use different secrets per environment**
   - Production and dev should have different SECRET_KEYs
   - Different database credentials

3. **Limit production access**
   - Only deploy to production from `main` branch
   - Require code review before merging to `main`

## 📞 Support

If you encounter issues:

1. Check Railway logs
2. Review GitHub Actions results
3. Test locally with Docker
4. Check this documentation

## 🎉 Quick Reference

```bash
# Development
make switch-to-dev          # Switch to dev branch
make dev                    # Run local server
make test                   # Run tests
make deploy-dev             # Deploy to dev environment

# Production
make switch-to-main         # Switch to main branch
make promote-to-prod        # Merge dev → main and deploy
make deploy-prod            # Deploy to production

# Utilities
make lint                   # Check code quality
make format                 # Format code
make clean                  # Clean cache files
```

## 🌟 Tips

1. **Use dev liberally** - Test everything in dev first
2. **Commit often** - Small, focused commits are better
3. **Write tests** - They catch bugs before production
4. **Monitor logs** - Railway provides excellent logging
5. **Document changes** - Update docs when you add features

---

**Last Updated:** October 2025  
**Maintainer:** BleedRate Team
