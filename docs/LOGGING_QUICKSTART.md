# Supabase Logging - Quick Start

## ✅ What's Been Implemented

Your BleedRate calculator now logs every form submission to Supabase!

### Features Added:
1. **Submission Logger** (`app/services/logger.py`)
   - Logs all form inputs + calculated results
   - Non-blocking (won't slow down responses)
   - Includes user agent and hashed IP
   - Graceful error handling (never breaks main app)

2. **Privacy-First**:
   - No PII stored (names, emails, etc.)
   - IP addresses hashed with SHA-256
   - Only form inputs and calculation results
   - POPIA compliant

3. **Database Schema** (`scripts/supabase_setup.sql`)
   - `submissions` table with indexes
   - Helper views for statistics
   - Row Level Security enabled
   - Ready for 100k+ submissions

4. **Configuration**:
   - Environment variables in `.env.example`
   - Config added to `app/config.py`
   - Easy to enable/disable via `ENABLE_SUBMISSION_LOGGING`

5. **Documentation**:
   - Full setup guide: `docs/SUPABASE_SETUP.md`
   - Railway deployment: `docs/RAILWAY_DEPLOYMENT.md`

## 🚀 Quick Setup (5 minutes)

### 1. Create Supabase Project
- Go to https://supabase.com → New Project
- Note your URL and anon key

### 2. Run SQL Setup
- Supabase Dashboard → SQL Editor
- Paste contents of `scripts/supabase_setup.sql`
- Click Run

### 3. Configure Locally
Edit `.env`:
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
ENABLE_SUBMISSION_LOGGING=true
```

### 4. Install Package
```bash
pip install supabase
# or
pip install -r requirements.txt
```

### 5. Test It!
```bash
uvicorn app.main:app --reload
```
- Submit form
- Check Supabase → Table Editor → `submissions`
- See your data! 🎉

## 📊 Viewing Your Data

### Supabase Dashboard
**Table Editor** → `submissions`:
- View all submissions
- Sort/filter by salary, rate, date
- Export to CSV

### Useful SQL Queries

**Recent submissions:**
```sql
SELECT timestamp, annual_salary, total_to_govt, effective_rate
FROM submissions
ORDER BY timestamp DESC
LIMIT 20;
```

**Average by salary band:**
```sql
SELECT * FROM salary_band_stats;
```

**Daily stats:**
```sql
SELECT 
    DATE(timestamp) as date,
    COUNT(*) as count,
    AVG(effective_rate) as avg_rate
FROM submissions
GROUP BY DATE(timestamp)
ORDER BY date DESC;
```

## 🚂 Deploy to Railway

### Add Environment Variables:
Railway Dashboard → Your Service → Variables:
```
SUPABASE_URL = https://your-project.supabase.co
SUPABASE_KEY = your-anon-key-here
ENABLE_SUBMISSION_LOGGING = true
```

Railway auto-deploys on git push!

## 💰 Costs

**Supabase Free Tier:**
- 500MB database (~100k submissions)
- 2GB bandwidth/month
- Unlimited API requests
- **Cost: FREE**

**Railway Free Tier:**
- $5 credit/month
- 500 hours runtime
- 100GB bandwidth
- **Cost: FREE** for small projects

## 📈 What Gets Logged

Each submission records:
- ✅ All form inputs (salary, age, consumption, etc.)
- ✅ Calculated results (total, percentage, breakdown)
- ✅ Timestamp
- ✅ User agent (browser info)
- ✅ Hashed IP (for abuse prevention)
- ❌ NO personal identifiers (POPIA compliant)

## 🔒 Security

- **Row Level Security (RLS)** enabled
- **Anonymous inserts** allowed (for form submissions)
- **Authenticated reads only** (for your admin access)
- **No service role key** in client code
- **IP hashing** for privacy

## 🛠️ Troubleshooting

**Logging not working?**
```bash
# Check environment variables
echo $SUPABASE_URL
echo $ENABLE_SUBMISSION_LOGGING

# Check logs
tail -f logs/app.log  # or railway logs
```

**Database errors?**
- Verify SQL setup ran successfully
- Check Supabase → Logs → Postgres Logs

**See "Logging disabled" message?**
- Set `ENABLE_SUBMISSION_LOGGING=true` in .env
- Restart server

## 📚 Full Documentation

- **Supabase Setup**: `docs/SUPABASE_SETUP.md`
- **Railway Deployment**: `docs/RAILWAY_DEPLOYMENT.md`
- **Supabase Docs**: https://supabase.com/docs
- **Railway Docs**: https://docs.railway.app

## 🎯 Next Steps

1. **Test locally** with `.env` configured
2. **Create Supabase project** and run SQL setup
3. **Deploy to Railway** with environment variables
4. **Monitor submissions** in Supabase dashboard
5. **Build analytics** using the data!

---

**You're ready to track your BleedRate submissions!** 🚀

Every form submission now logs to Supabase for analysis, with full privacy protection and POPIA compliance.
