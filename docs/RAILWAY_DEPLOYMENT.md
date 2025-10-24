
# Railway.app Deployment Configuration for BleedRate

## Quick Deploy to Railway

### Option 1: Deploy from GitHub (Recommended)

1. **Push your code to GitHub**:
```bash
git add .
git commit -m "Add Supabase logging"
git push origin main
```

2. **Connect to Railway**:
- Go to https://railway.app
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose your BleedRate repository
- Railway auto-detects FastAPI and configures everything

3. **Add Environment Variables**:
- In Railway dashboard → Variables tab, add:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
ENABLE_SUBMISSION_LOGGING=true
```

4. **Deploy**: Railway automatically builds and deploys!

### Option 2: Deploy from CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Link to new/existing project
railway link

# Add environment variables
railway variables set SUPABASE_URL=https://your-project.supabase.co
railway variables set SUPABASE_KEY=your-anon-key-here
railway variables set ENABLE_SUBMISSION_LOGGING=true

# Deploy
railway up
```

## Railway Configuration Files

Railway auto-detects Python/FastAPI projects, but you can customize with these files:

### railway.toml (optional, for custom config)
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/"
healthcheckTimeout = 100
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

### Procfile (alternative method)
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Environment Variables Needed

| Variable | Value | Description |
|----------|-------|-------------|
| `SUPABASE_URL` | `https://xxx.supabase.co` | Your Supabase project URL |
| `SUPABASE_KEY` | `eyJhbGci...` | Your Supabase anon/public key |
| `ENABLE_SUBMISSION_LOGGING` | `true` | Enable logging to Supabase |
| `SECRET_KEY` | (auto-generated) | FastAPI secret key |
| `ENV` | `production` | Environment |
| `DEBUG` | `false` | Disable debug mode |

## Custom Domain (Optional)

1. In Railway dashboard → Settings → Domains
2. Click "Generate Domain" for free Railway domain: `bleedrate.up.railway.app`
3. Or add custom domain: `bleedrate.co.za`
   - Add CNAME record in your DNS: `CNAME -> bleedrate.up.railway.app`
   - Railway auto-provisions SSL certificate

## Deployment Checklist

Before deploying, ensure:

- [ ] `requirements.txt` includes `supabase`
- [ ] `.env.example` has Supabase variables documented
- [ ] `scripts/supabase_setup.sql` has been run in Supabase
- [ ] Supabase project is created and table exists
- [ ] All environment variables added to Railway
- [ ] Code pushed to GitHub (if using GitHub deploy)
- [ ] Tested locally with `.env` configured

## Monitoring

### Railway Dashboard
- **Logs**: View real-time application logs
- **Metrics**: CPU, memory, network usage
- **Deployments**: History of all deployments

### Supabase Dashboard
- **Table Editor**: View submissions in real-time
- **Logs**: Database query logs
- **API Analytics**: Request volume and performance

## Troubleshooting

### Deployment fails
```bash
# Check logs
railway logs

# Common issues:
# - Missing dependencies in requirements.txt
# - Python version mismatch
# - Port not bound correctly (must use $PORT env var)
```

### App starts but crashes
```bash
# Check if all environment variables are set
railway variables

# View error logs
railway logs --follow
```

### Logging not working
```bash
# Verify Supabase config
railway variables | grep SUPABASE

# Check logs for error messages
railway logs | grep -i "supabase\|logging"
```

## Costs

### Railway Free Tier
- **$5 free** per month
- **500 hours** of usage
- **100GB** bandwidth
- Enough for hobby projects with moderate traffic

### Railway Pro Plan ($20/month)
- **More resources** for higher traffic
- **Priority support**
- **Team collaboration**

### Supabase Free Tier
- **500MB** database
- **2GB** bandwidth/month
- **Unlimited** API requests
- Enough for ~100k+ submissions

## Scaling Considerations

### When to upgrade Railway:
- App receives >10k requests/day
- Need more than 500 hours/month uptime
- Require guaranteed uptime SLA

### When to upgrade Supabase:
- Database exceeds 500MB (~100k submissions)
- Need >2GB bandwidth/month
- Want daily backups and point-in-time recovery

## Support

- **Railway Discord**: https://discord.gg/railway
- **Railway Docs**: https://docs.railway.app
- **Supabase Discord**: https://discord.supabase.com
- **Supabase Docs**: https://supabase.com/docs
