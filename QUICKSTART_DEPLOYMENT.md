# 🚀 Quick Start - Dev Branch Deployment

## ⚡ Quick Commands

```bash
# Development workflow
make switch-to-dev          # Switch to dev branch
make dev                    # Run local server
make test                   # Run tests
make deploy-dev             # Deploy to Railway dev

# Production workflow  
make promote-to-prod        # Merge dev to main and deploy
make deploy-prod            # Deploy main to production

# Utilities
make format                 # Format code
make lint                   # Check code quality
```

## 📋 Setup Checklist

### 1. Local Setup
- [x] Dev branch created and pushed
- [ ] Copy `.env.example` to `.env`
- [ ] Install dependencies: `make install`
- [ ] Run tests: `make test`
- [ ] Start server: `make dev`

### 2. Railway Setup

#### Create Development Service
1. Go to Railway dashboard
2. Click "New" → "Service from GitHub"
3. Select BleedRate repository
4. Name: `bleedrate-development`
5. Settings:
   - Branch: `dev`
   - Build: Dockerfile
   - Healthcheck: `/health`

6. Add environment variables:
```
ENVIRONMENT=development
DEBUG=true
ADMIN_ENABLED=true
ENABLE_ADS=false
SECRET_KEY=<generate-new-secret>
```

#### Create Production Service
1. Create another service
2. Name: `bleedrate-production`
3. Settings:
   - Branch: `main`
   - Build: Dockerfile
   - Healthcheck: `/health`

4. Add environment variables:
```
ENVIRONMENT=production
DEBUG=false
ENABLE_ADS=true
ENABLE_SUBMISSION_LOGGING=true
SECRET_KEY=<generate-different-secret>
SUPABASE_URL=<your-url>
SUPABASE_KEY=<your-key>
GOOGLE_ADSENSE_CLIENT_ID=<your-id>
```

### 3. Test Deployments

```bash
# Test dev deployment
curl https://bleedrate-dev.up.railway.app/health

# Should return:
# {"status":"healthy","version":"1.0.0","environment":"development","debug":true}

# Test prod deployment
curl https://bleedrate.up.railway.app/health

# Should return:
# {"status":"healthy","version":"1.0.0","environment":"production","debug":false}
```

## 🔄 Daily Workflow

### Working on a Feature

```bash
# 1. Start on dev
make switch-to-dev

# 2. Make changes
# ... edit files ...

# 3. Test locally
make test
make dev

# 4. Commit and deploy
git add .
git commit -m "feat: your feature description"
make deploy-dev

# 5. Test on dev server
# Visit: https://bleedrate-dev.up.railway.app

# 6. When ready, promote to production
make promote-to-prod
```

### Quick Deploy Cycle

```bash
# Edit → Test → Deploy
vim app/some_file.py
make test && make deploy-dev
```

## 🎯 URLs

| Environment | URL | Branch | Database |
|-------------|-----|--------|----------|
| **Local** | http://localhost:8000 | any | local SQLite |
| **Dev** | https://bleedrate-dev.up.railway.app | `dev` | dev SQLite |
| **Prod** | https://bleedrate.up.railway.app | `main` | prod SQLite |

## 🔍 Health Checks

All environments expose a health check:

```bash
# Local
curl http://localhost:8000/health

# Dev
curl https://bleedrate-dev.up.railway.app/health

# Prod
curl https://bleedrate.up.railway.app/health
```

## 🐳 Docker Testing

Test in a production-like environment locally:

```bash
# Start dev container
docker-compose -f docker-compose.dev.yml up

# Access:
# - App: http://localhost:8001
# - DB Viewer: http://localhost:8002 (with --profile tools)
```

## ✅ Pre-Production Checklist

Before running `make promote-to-prod`:

- [ ] All tests pass (`make test`)
- [ ] Code is formatted (`make format`)
- [ ] No lint errors (`make lint`)
- [ ] Tested in dev environment
- [ ] Reviewed changes (`git log`)
- [ ] Database migrations applied (if any)
- [ ] Environment variables updated in Railway prod

## 🆘 Troubleshooting

### Deployment Not Working
```bash
# Check Railway logs in dashboard
# Redeploy: Railway → Service → Settings → Redeploy

# Test health endpoint
curl https://your-service.up.railway.app/health
```

### Tests Failing
```bash
# Run with verbose output
pytest tests/ -v

# Check specific test
pytest tests/test_specific.py -v
```

### Can't Switch Branches
```bash
# Stash changes
git stash

# Switch branch
make switch-to-dev

# Apply changes
git stash pop
```

## 📚 More Info

For detailed documentation, see:
- [DEPLOYMENT_WORKFLOW.md](./DEPLOYMENT_WORKFLOW.md) - Complete deployment guide
- [RAILWAY_DEPLOYMENT.md](./RAILWAY_DEPLOYMENT.md) - Railway-specific setup

---

**You're all set!** 🎉

Start with: `make switch-to-dev` → make changes → `make deploy-dev`
