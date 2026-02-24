# Core Web Vitals Optimization Strategy

## Current Status (Baseline)

### Metrics to Measure:
- **LCP (Largest Contentful Paint):** < 2.5s target
- **INP (Interaction to Next Paint):** < 200ms target
- **CLS (Cumulative Layout Shift):** < 0.1 target

### Testing Tools:
1. **Google PageSpeed Insights** - https://pagespeed.web.dev/
2. **Google Lighthouse** (Chrome DevTools)
3. **WebPageTest** - https://www.webpagetest.org/
4. **Chrome User Experience Report** (CrUX) - Real user data

---

## Optimization Strategies

### 1. LCP (Largest Contentful Paint) Optimization

**Goal:** Get hero image or form to render < 2.5s

#### Issues to Fix:
- [ ] Large unoptimized images in hero section
- [ ] Render-blocking CSS
- [ ] Render-blocking JavaScript
- [ ] Slow web font loading
- [ ] Server response time (TTFB)

#### Solutions:

**A. Image Optimization**
```html
<!-- Use WebP with fallback -->
<picture>
  <source srcset="/img/hero.webp" type="image/webp">
  <img src="/img/hero.png" alt="Calculator hero" loading="lazy">
</picture>

<!-- Responsive images -->
<img srcset="/img/hero-sm.webp 640w, /img/hero-lg.webp 1920w" 
     sizes="100vw"
     src="/img/hero.webp"
     alt="Hero image">
```

**B. CSS Optimization**
- Split critical CSS from non-critical
- Inline critical CSS in `<head>`
- Defer non-critical CSS with `media` attribute
- Minify CSS

```html
<!-- Inline critical CSS only -->
<style>
  /* Critical styles for above-fold content only */
  body, header, hero { /* ... */ }
</style>

<!-- Defer non-critical CSS -->
<link rel="preload" href="/css/full.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="/css/full.css"></noscript>
```

**C. Font Optimization**
- Use `font-display: swap` for web fonts
- Preload critical fonts
- Limit font weights

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap" rel="stylesheet">
```

**D. Server Response Time (TTFB)**
- Enable gzip compression (✓ already done in FastAPI)
- Use CDN for static assets (Cloudflare)
- Cache HTTP headers
- Optimize database queries

---

### 2. INP (Interaction to Next Paint) Optimization

**Goal:** Form interactions < 200ms

#### Issues to Fix:
- [ ] Long JavaScript tasks blocking main thread
- [ ] Slow form validation
- [ ] Calculator calculations taking > 50ms
- [ ] HTMX request handling delays
- [ ] Event listener delays

#### Solutions:

**A. Break Up Long Tasks**
```javascript
// Instead of this (blocks for 200ms):
function calculateTaxes() {
  for (let i = 0; i < 1000000; i++) {
    // expensive calculation
  }
}

// Do this (chunked):
async function calculateTaxesFast() {
  const chunks = [];
  for (let i = 0; i < 10000; i += 1000) {
    chunks.push(doWork(i, i + 1000));
    await new Promise(resolve => setTimeout(resolve, 0));
  }
  return chunks;
}
```

**B. Optimize Form Inputs**
- Debounce form input handlers
- Use `requestAnimationFrame` for visual updates
- Lazy-validate instead of real-time validation

```html
<input type="number" 
       hx-trigger="change delay:500ms" 
       hx-post="/calc"
       name="salary">
```

**C. Optimize HTMX Requests**
- Use response streaming
- Return only changed DOM
- Minimize payload size

**D. Remove Unused JavaScript**
- Tree-shake unused code
- Load JavaScript only when needed
- Use code splitting

---

### 3. CLS (Cumulative Layout Shift) Optimization

**Goal:** No unexpected layout shifts (< 0.1)

#### Issues to Fix:
- [ ] Ad units causing shifts
- [ ] Images without fixed dimensions
- [ ] Web fonts causing FOIT/FOUT
- [ ] Dynamic content loading
- [ ] Modal/toast notifications

#### Solutions:

**A. Reserve Space for Dynamic Content**
```html
<!-- For ads (critical for AdSense!) -->
<div style="width: 300px; height: 250px; min-height: 250px;">
  <!-- Ad code loads here, no shift -->
</div>

<!-- For images -->
<img src="..." width="640" height="480" alt="">

<!-- Calculate aspect ratio -->
<img src="..." style="aspect-ratio: 16/9;" alt="">
```

**B. Font Loading Strategy**
- Use `font-display: swap` (already done)
- Preload critical fonts
- System fonts as fallback

**C. Avoid Inserting Content Above Fold**
```javascript
// ❌ Bad: Inserts above the form
document.body.insertAdjacentHTML('afterbegin', '<div>Ad</div>');

// ✅ Good: Inserts in reserved space
document.getElementById('ad-container').innerHTML = '...';
```

**D. Modal & Toast Management**
- Use `position: fixed` for modals
- Prevent layout shift from scrollbar hiding
```css
body.modal-open {
  overflow: hidden;
  padding-right: 15px; /* Account for scrollbar width */
}
```

---

## Implementation Checklist

### Phase 1: Critical Fixes
- [ ] Optimize hero image (compress, WebP, responsive sizes)
- [ ] Inline critical CSS
- [ ] Preload web fonts
- [ ] Defer non-critical CSS
- [ ] Defer non-critical JavaScript

### Phase 2: Form/Interaction Optimization
- [ ] Optimize calculator JavaScript
- [ ] Debounce form inputs
- [ ] Cache form state
- [ ] Optimize HTMX requests

### Phase 3: Ad & Layout Stability
- [ ] Reserve space for all ad units (300x250, 728x90, etc.)
- [ ] Fix image dimensions
- [ ] Test with Google PageSpeed Insights
- [ ] Test on real mobile devices

### Phase 4: Testing & Validation
- [ ] Run PageSpeed Insights (target > 80 mobile)
- [ ] Run Lighthouse audit
- [ ] Test on 4G throttled network
- [ ] Test on low-end devices
- [ ] Test on real mobile phone

---

## Current Asset Audit

### CSS
- Tailwind CSS (CDN) - ~50KB compressed
- Custom styles in `<style>` blocks
- No custom CSS files currently

### JavaScript
- HTMX (CDN) - ~15KB
- Chart.js (CDN) - ~35KB
- Google Analytics
- Google AdSense

### Images
- legalwills-estate-planning.png (55KB)
- No hero image optimized yet

---

## Recommendations for BleedRate

### Immediate (Easy Wins)
1. **Optimize legalwills image** → WebP + responsive sizes (potential: -40KB)
2. **Move Google Analytics to async** (potential: -5ms LCP)
3. **Add missing image dimensions** (potential: 0 CLS)
4. **Set `font-display: swap`** for Inter font (already done)

### Short-term (Medium Effort)
5. **Create optimized hero image** with srcset
6. **Inline above-fold CSS** (critical path)
7. **Defer below-fold CSS loading**
8. **Cache static assets** with max-age headers
9. **Enable GZIP** (✓ already enabled)

### Medium-term (More Effort)
10. **Code-split calculator JavaScript**
11. **Lazy-load Chart.js** (only if charts visible)
12. **Preload critical resources** (fonts, images)
13. **Set up service worker** for offline capability
14. **Use CDN for static assets** (Cloudflare)

---

## Testing Workflow

### Before Making Changes
1. Run PageSpeed Insights on home page
2. Record baseline LCP, INP, CLS, Performance Score
3. Document in this file

### After Each Optimization
1. Run PageSpeed Insights again
2. Compare metrics
3. Document improvement or issue
4. Commit with metrics in message

### Example Commit Message
```
Optimize images: WebP + responsive srcset

LCP: 3.2s → 2.8s ✓
INP: 250ms → 180ms ✓
CLS: 0.12 → 0.08 ✓
Performance: 65 → 78
```

---

## Tools & Resources

- **PageSpeed Insights:** https://pagespeed.web.dev/
- **Lighthouse:** Chrome DevTools → Audit
- **WebPageTest:** https://webpagetest.org/
- **TinyPNG/TinyJPG:** Image compression
- **Squoosh:** Google's image optimizer
- **GTMetrix:** Performance monitoring
- **Chrome DevTools:** Network tab, Performance tab

---

## Success Criteria

✅ **Phase 1 Complete When:**
- LCP < 2.5s on mobile (4G)
- INP < 200ms on mobile
- CLS < 0.1 on all pages
- PageSpeed score > 80 on mobile
- No CLS from ads or dynamic content
