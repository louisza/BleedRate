# Google AdSense Integration Guide

## Overview

BleedRate includes Google AdSense integration for monetization. Ads are strategically placed to maximize revenue without disrupting user experience.

## Ad Placements

1. **Top Banner** (Desktop only) - After header, before calculator form
2. **After Results** - Below the results section 
3. **Premium Placement** - After the shocking total (highest engagement point)

## Setup Instructions

### 1. Sign Up for Google AdSense

1. Go to https://www.google.com/adsense
2. Sign up with your Google account
3. Add your website URL (your Railway deployment URL)
4. Complete the verification process
5. Wait for approval (typically 1-3 days, can take up to 2 weeks)

### 2. Get Your Publisher ID

Once approved:

1. Log in to AdSense dashboard
2. Go to **Account** → **Account Information**
3. Copy your **Publisher ID** (format: `ca-pub-1234567890123456`)

### 3. Configure Environment Variables

**Local Development** (`.env` file):
```bash
GOOGLE_ADSENSE_CLIENT_ID=ca-pub-1234567890123456
ENABLE_ADS=true
```

**Railway Deployment**:
1. Go to your Railway project dashboard
2. Click on your service
3. Go to **Variables** tab
4. Add these environment variables:
   - `GOOGLE_ADSENSE_CLIENT_ID` = `ca-pub-1234567890123456`
   - `ENABLE_ADS` = `true`
5. Redeploy your application

### 4. Test AdSense Integration

1. Deploy your app with ads enabled
2. Visit your live site
3. Check browser console for AdSense loading
4. Note: **Ads won't show immediately** - can take 24-48 hours for AdSense to start serving ads
5. Initially you'll see blank spaces where ads will appear

### 5. Create Ad Units (Optional - for better tracking)

Instead of using auto ads (`data-ad-slot="auto"`), you can create specific ad units:

1. In AdSense dashboard, go to **Ads** → **By ad unit**
2. Click **+ New ad unit** → **Display ads**
3. Name it (e.g., "BleedRate - Top Banner", "BleedRate - Results", "BleedRate - Premium")
4. Choose **Responsive** ad type
5. Click **Create**
6. Copy the **Ad slot ID** (10-digit number)
7. Update `_ad_unit.html` template:
   ```html
   data-ad-slot="{{ ad_slot if ad_slot else 'auto' }}"
   ```
8. Pass specific slot IDs from templates:
   ```html
   {% set ad_slot = "1234567890" %}  <!-- Your actual slot ID -->
   ```

## Revenue Optimization Tips

### 1. Ad Placement Best Practices

✅ **Current placements are optimal**:
- After shocking total (highest engagement - users are emotionally invested)
- Top banner (immediate visibility)
- After results (natural break point)

❌ **Avoid**:
- Don't add too many ads (hurts user experience)
- Don't place ads before the form (users haven't seen value yet)
- Don't use intrusive ad formats (popups, interstitials)

### 2. Content Optimization

- Keep your shocking stats and dramatic UI - high engagement = more ad views
- The more calculations users run, the more ad impressions
- Consider adding a "Save Results" or "Compare Scenarios" feature to increase page views

### 3. Traffic Quality

- South African traffic has lower CPM (Cost Per Mille) than US/UK (~$1-5 vs $10-30)
- Focus on driving high-quality traffic (tax professionals, financial advisors, high earners)
- Consider targeting expats, financial bloggers, tax optimization communities

### 4. Expected Revenue (Conservative Estimates)

**Assumptions**:
- 1,000 monthly visitors
- 5 page views per visitor = 5,000 page views
- 3 ad units per page = 15,000 ad impressions
- SA CPM = $2 (R35)

**Monthly Revenue**: R525 (15,000 impressions × R35 / 1000)

**At Scale**:
- 10,000 monthly visitors = R5,250/month
- 50,000 monthly visitors = R26,250/month
- 100,000 monthly visitors = R52,500/month

## Monitoring Performance

### 1. AdSense Dashboard

- **Performance** → View earnings, clicks, impressions, RPM
- **Optimization** → Get recommendations to increase revenue
- **Blocking controls** → Block low-paying ad categories

### 2. Key Metrics to Track

- **RPM (Revenue Per Mille)**: Revenue per 1,000 impressions
- **CTR (Click-Through Rate)**: % of users who click ads
- **CPC (Cost Per Click)**: Average earnings per click
- **Page Views**: More pages = more impressions

### 3. Optimization Checklist

- [ ] Enable Auto Ads in AdSense (AI-optimized placements)
- [ ] Block sensitive categories (if needed)
- [ ] Enable "Ads.txt" (improves CPM by verifying you own the domain)
- [ ] Experiment with ad sizes (larger formats often pay better)
- [ ] A/B test ad placements

## Ads.txt Setup (Important!)

Ads.txt increases revenue by 10-20% by verifying you're authorized to sell ad inventory.

### 1. Generate ads.txt

1. In AdSense, go to **Account** → **Ads.txt**
2. Copy your ads.txt snippet (looks like):
   ```
   google.com, pub-1234567890123456, DIRECT, f08c47fec0942fa0
   ```

### 2. Add to Railway

Create `app/static/ads.txt`:
```bash
google.com, pub-YOUR_PUBLISHER_ID, DIRECT, f08c47fec0942fa0
```

### 3. Serve via FastAPI

Update `app/main.py`:
```python
from fastapi.responses import FileResponse

@app.get("/ads.txt")
async def ads_txt():
    return FileResponse("app/static/ads.txt", media_type="text/plain")
```

### 4. Verify

Visit `https://your-domain.com/ads.txt` - should show your ads.txt content

## Troubleshooting

### Ads Not Showing

1. **Wait 24-48 hours** - AdSense needs time to crawl your site
2. Check browser console for errors
3. Verify `ENABLE_ADS=true` in environment variables
4. Ensure your AdSense account is fully approved
5. Check if you have an ad blocker enabled (disable for testing)

### Low Revenue

1. **Traffic source matters** - Ensure you're getting South African traffic
2. **User engagement** - Users must actually see the ads (scroll down)
3. **Invalid clicks** - Don't click your own ads (Google will ban you)
4. **Content quality** - High-quality financial content attracts higher CPM advertisers
5. **Ad placement** - Experiment with different positions

### AdSense Policy Issues

✅ **BleedRate is compliant** because:
- No prohibited content
- Clear value proposition
- Not incentivizing ad clicks
- Privacy policy exists (via Supabase setup)

❌ **Don't**:
- Click your own ads
- Ask users to click ads
- Use misleading content
- Reload page repeatedly to inflate impressions

## Next Steps

1. **Get approved** - Apply to AdSense with your Railway URL
2. **Enable ads** - Set `ENABLE_ADS=true` in production
3. **Monitor performance** - Check AdSense dashboard weekly
4. **Optimize** - Experiment with placements and ad formats
5. **Scale traffic** - More traffic = more revenue

## Advanced: Combine with Other Monetization

AdSense works best when combined with:
- **Affiliate marketing** (financial services) - 50-70% of revenue
- **Premium features** (PDF reports) - 20-30% of revenue
- **AdSense** (passive) - 10-20% of revenue

See `docs/MONETIZATION.md` for comprehensive strategy.

## Support

- **Google AdSense Help**: https://support.google.com/adsense
- **Policy Center**: https://support.google.com/adsense/answer/48182
- **Optimization Tips**: https://support.google.com/adsense/answer/17957

---

**Revenue Formula**: `Impressions × CPM / 1000 = Revenue`

Example: 15,000 impressions × R35 CPM / 1000 = R525/month

**Goal**: Drive 100K+ page views/month for R5,000+ monthly AdSense revenue! 🚀
