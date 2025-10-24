# ✅ Dev Branch Deployment - Implementation Complete!

## 🎉 What We've Built

A complete **development and production deployment workflow** for BleedRate with automatic deployments, CI/CD, and easy promotion between environments.

## 📦 Files Created/Modified

### New Files
1. **`railway.json`** - Railway deployment configuration
2. **`.github/workflows/test.yml`** - GitHub Actions CI/CD pipeline
3. **`docker-compose.dev.yml`** - Local development container setup
4. **`docs/DEPLOYMENT_WORKFLOW.md`** - Comprehensive deployment guide
5. **`QUICKSTART_DEPLOYMENT.md`** - Quick reference guide

### Modified Files
1. **`app/config.py`** - Added environment-specific configuration
2. **`app/main.py`** - Enhanced health check endpoint
3. **`Makefile`** - Added deployment commands
4. **`.env.example`** - Updated with environment variables
5. **`.gitignore`** - Allowed railway.json

## 🚀 How It Works

### Branch Structure
```
main (production)     → https://bleedrate.up.railway.app
 ↑
dev (staging)         → https://bleedrate-dev.up.railway.app
```

### Automatic Deployments
- **Push to `dev`** → Auto-deploys to development
- **Push to `main`** → Auto-deploys to production

### CI/CD Pipeline
- **Tests** run automatically on every push/PR
- **Linting** checks code quality
- **Formatting** validates code style

## 🎯 Quick Commands

```bash
# Development
make switch-to-dev          # Switch to dev branch
make deploy-dev             # Deploy to dev environment
make dev                    # Run locally

# Testing
make test                   # Run test suite
make lint                   # Check code quality
make format                 # Format code

# Production
make promote-to-prod        # Merge dev → main and deploy
make deploy-prod            # Deploy to production
```

## 📋 Next Steps - Railway Setup

### 1. Create Development Service

Go to [Railway Dashboard](https://railway.app/dashboard):

1. Click "New Project" or select existing project
2. Click "New" → "Service from GitHub repo"
3. Select **BleedRate** repository
4. Configure:
   - **Name:** `bleedrate-development`
   - **Branch:** `dev`
   - **Root Directory:** `/`
   - **Build:** Dockerfile
   
5. Add Environment Variables:
```bash
ENVIRONMENT=development
DEBUG=true
ADMIN_ENABLED=true
ENABLE_ADS=false
ENABLE_SUBMISSION_LOGGING=false
SECRET_KEY=<generate-random-key>
```

6. Go to Settings → Deploy:
   - **Healthcheck Path:** `/health`
   - **Healthcheck Timeout:** 100
   - **Restart Policy:** On Failure

### 2. Create Production Service

Repeat the above but with:
- **Name:** `bleedrate-production`
- **Branch:** `main`
- Environment Variables:
```bash
ENVIRONMENT=production
DEBUG=false
ENABLE_ADS=true
ENABLE_SUBMISSION_LOGGING=true
SECRET_KEY=<different-random-key>
SUPABASE_URL=<your-url>
SUPABASE_KEY=<your-key>
GOOGLE_ADSENSE_CLIENT_ID=<your-id>
```

### 3. Test Deployments

```bash
# Test dev
curl https://bleedrate-dev.up.railway.app/health

# Test prod
curl https://bleedrate.up.railway.app/health
```

## 🔄 Typical Workflow

### Day-to-Day Development

```bash
# 1. Work on dev branch
make switch-to-dev

# 2. Make changes
vim app/some_file.py

# 3. Test locally
make test
make dev

# 4. Commit and deploy to dev
git add .
git commit -m "feat: new feature"
make deploy-dev

# 5. Test on dev server
# Visit: https://bleedrate-dev.up.railway.app

# 6. When satisfied, promote to production
make promote-to-prod
```

### Quick Deploy Cycle

```bash
# Edit → Test → Deploy (one-liner)
vim app/file.py && make test && make deploy-dev
```

## 🛠️ Features Included

### ✅ Multi-Environment Setup
- Separate dev and production databases
- Environment-specific configuration
- Different debug/logging settings

### ✅ Automatic Deployments
- Push to `dev` = auto-deploy to staging
- Push to `main` = auto-deploy to production
- No manual deployment needed

### ✅ CI/CD Pipeline
- Automated testing on every push
- Code quality checks (Black, Ruff)
- Prevents broken code from deploying

### ✅ Health Monitoring
- `/health` endpoint on all environments
- Railway automatic health checks
- Easy monitoring and debugging

### ✅ Docker Development
- Local dev environment with hot reload
- Database viewer included
- Production-like testing locally

### ✅ Easy Promotion
- One command to promote dev → prod
- Confirmation prompt to prevent accidents
- Automatic merge and deployment

## 📊 What Happens Now

### On Every Push to Dev:
1. ✅ GitHub Actions runs tests
2. ✅ Code quality checks run
3. ✅ If passing, Railway deploys to dev environment
4. ✅ Health check confirms deployment
5. ✅ Dev site updates automatically

### When You Promote to Production:
1. ✅ Confirmation prompt shown
2. ✅ `dev` merges into `main`
3. ✅ GitHub Actions runs tests on `main`
4. ✅ If passing, Railway deploys to production
5. ✅ Production site updates

## 🎓 Learning Resources

- **Full Guide:** `docs/DEPLOYMENT_WORKFLOW.md`
- **Quick Reference:** `QUICKSTART_DEPLOYMENT.md`
- **Railway Docs:** [railway.app/docs](https://docs.railway.app/)
- **GitHub Actions:** Already configured in `.github/workflows/test.yml`

## 🔍 Monitoring

### Check Deployment Status

**Railway Dashboard:**
- View build logs
- Monitor runtime logs
- Check metrics (CPU, memory, network)
- View deployment history

**Health Checks:**
```bash
# Development
curl https://bleedrate-dev.up.railway.app/health

# Production
curl https://bleedrate.up.railway.app/health
```

**GitHub Actions:**
- Go to GitHub → Actions tab
- View test results for each push
- See CI/CD pipeline status

## 🐛 Troubleshooting

### Deployment Not Showing Up
```bash
# Check Railway logs in dashboard
# Railway → Service → Deployments → Click deployment → View logs
```

### Tests Failing
```bash
# Run locally with verbose output
pytest tests/ -vv

# Check which test failed
make test
```

### Can't Switch Branches
```bash
# Save your work first
git stash
make switch-to-dev
git stash pop
```

## 🎁 Bonus Features

### Docker Development Environment
```bash
# Start dev container with hot reload
docker-compose -f docker-compose.dev.yml up

# Access: http://localhost:8001
```

### Database Viewer
```bash
# Start with database viewer
docker-compose -f docker-compose.dev.yml --profile tools up

# Viewer: http://localhost:8002
```

### Makefile Commands
```bash
make install           # Install dependencies
make dev              # Run local server
make test             # Run tests
make lint             # Check code quality
make format           # Format code
make clean            # Clean cache files
make deploy-dev       # Deploy to dev
make deploy-prod      # Deploy to prod
make promote-to-prod  # Promote dev to prod
make switch-to-dev    # Switch to dev branch
make switch-to-main   # Switch to main branch
```

## 📈 What's Next?

Now that the infrastructure is set up:

1. ✅ **Configure Railway services** (see Next Steps above)
2. ✅ **Test the dev deployment** workflow
3. ✅ **Make a test change** and deploy to dev
4. ✅ **Promote to production** when ready
5. ✅ **Monitor and iterate**

## 🎊 You're All Set!

Everything is configured and ready to go. Just:

1. Set up the Railway services (see "Next Steps" above)
2. Start developing: `make switch-to-dev`
3. Deploy: `make deploy-dev`
4. Promote when ready: `make promote-to-prod`

**Happy deploying!** 🚀

---

**Implementation Date:** October 24, 2025  
**Status:** ✅ Complete and Ready  
**Branch:** `dev` (with all changes pushed)
