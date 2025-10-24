# Supabase Setup Instructions for BleedRate

This guide will help you set up Supabase logging for BleedRate submissions.

## Prerequisites
- A Supabase account (free tier: https://supabase.com)
- Railway.app account for deployment

## Step 1: Create Supabase Project

1. Go to https://supabase.com and sign up/login
2. Click "New Project"
3. Fill in:
   - **Name**: bleedrate-logger (or your preferred name)
   - **Database Password**: Generate a strong password (save it!)
   - **Region**: Choose closest to South Africa (e.g., AWS eu-west-1)
   - **Plan**: Free (500MB database, 2GB bandwidth, unlimited API requests)
4. Click "Create new project" (takes ~2 minutes)

## Step 2: Set Up Database

1. In your Supabase dashboard, go to **SQL Editor** (left sidebar)
2. Click "New Query"
3. Copy and paste the entire contents of `scripts/supabase_setup.sql`
4. Click "Run" or press Ctrl+Enter
5. You should see "Success. No rows returned" - this is correct!

### What this creates:
- `submissions` table to store all form submissions
- Indexes for fast queries on salary, rate, timestamp
- Helper views for statistics and salary band analysis
- Row Level Security (RLS) policies for secure access

## Step 3: Get Your API Credentials

1. In Supabase dashboard, go to **Settings** → **API** (left sidebar)
2. You'll need two values:

   **Project URL** (looks like):
   ```
   https://abcdefghijklmnop.supabase.co
   ```

   **anon/public key** (looks like):
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYzMDUwMDAwMCwiZXhwIjoxOTQ2MDc2MDAwfQ.EXAMPLE_SIGNATURE
   ```

3. Copy both values - you'll need them next

## Step 4: Configure Locally (Development)

1. In your project root, create/edit `.env` file:
```bash
# Copy from .env.example if you don't have one
cp .env.example .env
```

2. Edit `.env` and add your Supabase credentials:
```bash
# Supabase (for logging submissions)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
ENABLE_SUBMISSION_LOGGING=true
```

3. Save the file

4. Restart your development server:
```bash
uvicorn app.main:app --reload
```

5. Test by submitting the form - check Supabase dashboard → **Table Editor** → `submissions` to see the data!

## Step 5: Deploy to Railway.app

### Method 1: Railway Dashboard (Recommended)

1. Go to your Railway project dashboard
2. Click on your service (bleedrate)
3. Go to **Variables** tab
4. Add three new variables:
   - **Variable**: `SUPABASE_URL`
     **Value**: `https://your-project.supabase.co`
   
   - **Variable**: `SUPABASE_KEY`
     **Value**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (your anon key)
   
   - **Variable**: `ENABLE_SUBMISSION_LOGGING`
     **Value**: `true`

5. Railway will automatically redeploy with the new environment variables

### Method 2: Railway CLI

```bash
# Install Railway CLI if you haven't
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Add environment variables
railway variables set SUPABASE_URL=https://your-project.supabase.co
railway variables set SUPABASE_KEY=your-anon-key-here
railway variables set ENABLE_SUBMISSION_LOGGING=true

# Deploy
railway up
```

## Step 6: Verify It's Working

1. Visit your deployed BleedRate app on Railway
2. Fill out the form and click "EXPOSE MY BLEED RATE"
3. Go to Supabase dashboard → **Table Editor** → `submissions`
4. You should see a new row with:
   - Timestamp
   - Salary amount
   - Total to government
   - Effective rate
   - Full form data (in `form_data` column)
   - Full results (in `results` column)

## Querying Your Data

### View in Supabase Dashboard

**Table Editor**: Browse submissions visually
- Go to **Table Editor** → `submissions`
- Sort by any column
- Filter by date range, salary, etc.
- Export to CSV

### SQL Queries

Go to **SQL Editor** and run queries:

**Most recent 10 submissions:**
```sql
SELECT 
    timestamp,
    annual_salary,
    total_to_govt,
    effective_rate
FROM submissions
ORDER BY timestamp DESC
LIMIT 10;
```

**Average effective rate by salary band:**
```sql
SELECT * FROM salary_band_stats;
```

**Daily submission count:**
```sql
SELECT 
    DATE(timestamp) as date,
    COUNT(*) as submissions,
    ROUND(AVG(effective_rate), 2) as avg_rate
FROM submissions
GROUP BY DATE(timestamp)
ORDER BY date DESC;
```

**Top tax categories people pay:**
```sql
SELECT 
    jsonb_object_keys(results->'breakdown') as tax_category,
    COUNT(*) as times_appeared,
    ROUND(AVG((results->'breakdown'->>jsonb_object_keys(results->'breakdown'))::numeric), 2) as avg_amount
FROM submissions
WHERE results->'breakdown' IS NOT NULL
GROUP BY tax_category
ORDER BY avg_amount DESC;
```

## Privacy & Compliance

### What Gets Logged:
✅ All form inputs (salary, age, consumption data)
✅ Calculated results (total, rate, breakdown)
✅ Timestamp
✅ User agent (browser info)
✅ Hashed IP address (SHA-256, not reversible)

### What Does NOT Get Logged:
❌ Names, emails, or any PII
❌ Actual IP addresses (only hashed)
❌ Payment information
❌ Contact details

### POPIA Compliance:
- No personal identifiers stored
- IP addresses are hashed (one-way encryption)
- Data used for aggregate statistics only
- Users can request data deletion (contact you)

## Cost Estimates

### Supabase Free Tier:
- **Database**: 500MB (enough for ~100,000-200,000 submissions)
- **Bandwidth**: 2GB/month
- **API Requests**: Unlimited
- **Rows**: No limit

**When do you need to upgrade?**
- If you hit 500MB database (check dashboard)
- If you need more than 2GB bandwidth/month
- Free tier is usually sufficient for 10,000+ users/month

### Railway.app:
- Supabase adds no extra cost to Railway
- All API calls go directly to Supabase (not through Railway)
- No database on Railway needed

## Troubleshooting

### "Logging disabled (missing Supabase config)"
- Check `.env` file has correct SUPABASE_URL and SUPABASE_KEY
- Ensure ENABLE_SUBMISSION_LOGGING=true
- Restart your server

### "Failed to log submission: 401 Unauthorized"
- Check your SUPABASE_KEY is the **anon/public** key (not the service_role key)
- Verify RLS policies are set up correctly (run supabase_setup.sql again)

### "Failed to log submission: 404 Not Found"
- Check your SUPABASE_URL is correct (should end with .supabase.co)
- Verify the `submissions` table exists in Supabase (check Table Editor)

### No data appearing in Supabase
1. Check server logs for errors: `railway logs` or check Railway dashboard
2. Test locally first (with `.env` configured)
3. Verify ENABLE_SUBMISSION_LOGGING=true in Railway variables
4. Check Supabase logs: Dashboard → **Logs** → **Postgres Logs**

## Next Steps

### Build an Admin Dashboard
- Create a simple page to view statistics
- Use the `submission_stats` and `salary_band_stats` views
- Add authentication to protect admin routes

### Export Data
- Download CSV from Table Editor for Excel analysis
- Use Supabase API to programmatically export
- Set up scheduled backups

### Analytics
- Track trends over time (effective rates increasing/decreasing)
- Identify most common salary bands
- See which tax categories shock people most

## Support

- **Supabase Docs**: https://supabase.com/docs
- **Railway Docs**: https://docs.railway.app
- **BleedRate Issues**: [Your GitHub repo]

---

**You're all set!** Your BleedRate calculator is now logging every submission to Supabase for analysis. 🎉
