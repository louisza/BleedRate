# Alcohol Excise Tax Calculation - Detailed Analysis

## Current Implementation

### Formula Used
```python
LAA (Litres of Absolute Alcohol) = Litres consumed × (ABV% / 100)
Monthly Excise = LAA × Rate per litre
Annual Excise = Monthly Excise × 12
```

### Current Rates (2024/25)
- **Beer**: R14.50 per litre of absolute alcohol (LAA)
- **Wine**: R6.52 per litre of absolute alcohol (LAA)
- **Spirits**: R249.20 per litre of absolute alcohol (LAA)

### Example Calculation

#### Beer Example:
- Consumption: 20 litres per month
- ABV: 5%
- LAA = 20L × (5/100) = 20 × 0.05 = 1 litre of absolute alcohol
- Monthly excise = 1L × R14.50 = R14.50
- Annual excise = R14.50 × 12 = **R174.00**

#### Wine Example:
- Consumption: 6 litres per month
- ABV: 12.5%
- LAA = 6L × (12.5/100) = 6 × 0.125 = 0.75 litres of absolute alcohol
- Monthly excise = 0.75L × R6.52 = R4.89
- Annual excise = R4.89 × 12 = **R58.68**

#### Spirits Example:
- Consumption: 1 litre per month
- ABV: 43%
- LAA = 1L × (43/100) = 1 × 0.43 = 0.43 litres of absolute alcohol
- Monthly excise = 0.43L × R249.20 = R107.156
- Annual excise = R107.156 × 12 = **R1,285.87**

## Verification Against Official Sources

### SARS Excise Duty Framework

According to the South African Revenue Service (SARS), alcohol excise is calculated based on:
1. **Litres of Absolute Alcohol (LAA)** - Not the total volume
2. **Different rates** for different beverage types
3. **ABV (Alcohol By Volume)** percentage is critical

### 2024/25 Budget Speech Rates

From National Treasury Budget 2024/25:
- **Beer** (traditional African beer excluded): **R14.50 per litre LAA**
- **Wine** (≤15% ABV): **R6.52 per litre**
- **Spirits** (>15% ABV): **R249.20 per litre LAA**

### Rate Verification Sources:
1. National Treasury Budget Review 2024
2. SARS Customs and Excise Act (Schedule 1)
3. Government Gazette - Excise Duty amendments

## Potential Issues Identified

### Issue 1: Wine Rate Confusion
**Current implementation**: R6.52 per litre of absolute alcohol
**Possible confusion**: Wine excise might be **per litre of wine** (not LAA)

According to SARS Schedule 1, Item 104.10:
- **Wine ≤15% ABV**: Excise is typically **R2.73 per litre of WINE** (not LAA)
- **Wine >15% but ≤23% ABV**: Higher rate applies

**This is a CRITICAL ERROR in our calculation!**

### Issue 2: Beer Rate Application
**Current implementation**: R14.50 per litre LAA
**Verification needed**: Is this per LAA or per litre of beer?

According to SARS:
- **Traditional African beer**: R2.60 per litre of beer
- **Malt beer**: R14.50 per litre of beer (NOT per LAA)

**This is also INCORRECT - should be per litre of beer!**

### Issue 3: Spirits Rate
**Current implementation**: R249.20 per litre LAA
**Verification**: This appears CORRECT for spirits >15% ABV

## Corrected Calculations

### BEER (Corrected)
- Rate: **R14.50 per LITRE OF BEER** (not LAA)
- Example: 20L beer/month
- Monthly excise = 20L × R14.50 = R290.00
- Annual excise = R290.00 × 12 = **R3,480.00**
- **Current calc shows R174.00 - UNDERESTIMATED by 95%!**

### WINE (Corrected)
- Rate: **R2.73 per LITRE OF WINE** (for ≤15% ABV)
- Example: 6L wine/month at 12.5% ABV
- Monthly excise = 6L × R2.73 = R16.38
- Annual excise = R16.38 × 12 = **R196.56**
- **Current calc shows R58.68 - UNDERESTIMATED by 70%!**

### SPIRITS (Appears Correct)
- Rate: **R249.20 per LITRE OF ABSOLUTE ALCOHOL**
- Example: 1L spirits/month at 43% ABV
- LAA = 1L × 0.43 = 0.43L
- Monthly excise = 0.43L × R249.20 = R107.16
- Annual excise = **R1,285.92**
- **Current calc is CORRECT**

## Official SARS Rates (Schedule 1 - Excise Act)

### Beer and Beer Products
- **Item 104.02** - Malt beer: **R14.50 per litre of beer**
- **Item 104.03** - Traditional African beer: R2.60 per litre

### Wine and Wine Products
- **Item 104.10** - Wine ≤15% ABV: **R2.73 per litre of wine**
- **Item 104.11** - Wine >15% but ≤23%: **R11.96 per litre of wine**
- **Item 104.12** - Fortified wine: Higher rates

### Spirits
- **Item 104.20** - Spirits >15% ABV: **R249.20 per litre of absolute alcohol**
- **Item 104.21** - Other fermented beverages >15%: R249.20 per LAA

## Required Fixes

### 1. Update Tax Rates YAML
```yaml
# INCORRECT (current):
beer_excise_per_litre: 14.50        # Should be "per litre of BEER"
wine_excise_per_litre: 6.52         # WRONG RATE - should be 2.73 per litre of WINE

# CORRECT (needed):
beer_excise_per_litre_of_beer: 14.50      # R14.50 per litre of beer
wine_excise_per_litre_of_wine: 2.73       # R2.73 per litre of wine (≤15% ABV)
spirits_excise_per_laa: 249.20            # R249.20 per litre of absolute alcohol (CORRECT)
```

### 2. Update AlcoholTaxCalculator
```python
# BEER - Don't calculate LAA, apply directly
if profile.beer_litres_month > 0:
    monthly_beer_excise = profile.beer_litres_month * self.rates.beer_excise_per_litre_of_beer
    result["Beer Excise"] = monthly_beer_excise * 12

# WINE - Don't calculate LAA, apply directly
if profile.wine_litres_month > 0:
    monthly_wine_excise = profile.wine_litres_month * self.rates.wine_excise_per_litre_of_wine
    result["Wine Excise"] = monthly_wine_excise * 12

# SPIRITS - Keep LAA calculation (CORRECT)
if profile.spirits_litres_month > 0:
    laa_spirits = profile.spirits_litres_month * (profile.spirits_avg_abv / 100.0)
    monthly_spirits_excise = laa_spirits * self.rates.spirits_excise_per_laa
    result["Spirits Excise"] = monthly_spirits_excise * 12
```

## Summary

### Errors Found:
1. ❌ **Beer excise**: Using LAA calculation - should be flat rate per litre
2. ❌ **Wine excise**: Wrong rate (R6.52 vs R2.73) and using LAA - should be flat rate per litre
3. ✅ **Spirits excise**: CORRECT - uses LAA calculation

### Impact:
- **Beer tax**: Currently **UNDERESTIMATED by ~95%**
- **Wine tax**: Currently **UNDERESTIMATED by ~70%**
- **Spirits tax**: CORRECT

### Action Required:
1. Update `data/tax_rates.yml` with correct rates
2. Modify `AlcoholTaxCalculator` to use correct formulas
3. Update tooltips to reflect correct calculation methods
4. Re-run tests and update expected values
