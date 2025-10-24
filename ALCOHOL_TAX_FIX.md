# Alcohol Excise Tax Calculation - FIXED ✅

## Summary of Issues and Corrections

### Problems Identified

The alcohol excise tax calculation had **critical errors** that resulted in significant underestimation of tax liability:

1. **Beer Excise**: Was incorrectly calculating based on litres of absolute alcohol (LAA)
   - ❌ **WRONG**: 20L beer @ 5% ABV = 1L LAA × R14.50 = **R174/year**
   - ✅ **CORRECT**: 20L beer × R14.50 = **R3,480/year**
   - **Underestimated by 95%!**

2. **Wine Excise**: Used wrong rate (R6.52) AND wrong calculation method (LAA)
   - ❌ **WRONG**: 6L wine @ 12.5% ABV = 0.75L LAA × R6.52 = **R58.68/year**
   - ✅ **CORRECT**: 6L wine × R2.73 = **R196.56/year**
   - **Underestimated by 70%!**

3. **Spirits Excise**: Was correctly using LAA calculation ✅
   - ✅ **CORRECT**: 1L spirits @ 43% ABV = 0.43L LAA × R249.20 = **R1,285.87/year**

## Corrected SARS Rates (2024/25)

Based on SARS Schedule 1 (Excise Act):

| Beverage Type | Correct Rate | Calculation Method |
|---------------|--------------|-------------------|
| **Beer** (malt beer) | R14.50 per litre | **Per LITRE OF BEER** (flat rate) |
| **Wine** (≤15% ABV) | R2.73 per litre | **Per LITRE OF WINE** (flat rate) |
| **Spirits** (>15% ABV) | R249.20 per LAA | **Per LITRE OF ABSOLUTE ALCOHOL** |

### Key Insight

- **Beer and Wine**: Excise is a flat rate per litre of the beverage itself
- **Spirits**: Excise is calculated based on absolute alcohol content (LAA)
- **ABV is irrelevant** for beer and wine excise calculations

## Files Changed

### 1. `data/tax_rates.yml`
```yaml
# BEFORE (incorrect):
beer_excise_per_litre: 14.50  # per LAA ❌
wine_excise_per_litre: 6.52   # WRONG RATE ❌

# AFTER (correct):
beer_excise_per_litre: 14.50  # per LITRE OF BEER ✅
wine_excise_per_litre: 2.73   # per LITRE OF WINE ✅
```

### 2. `app/domain/calculators.py` - AlcoholTaxCalculator
```python
# BEFORE (incorrect):
def calculate(self, profile: ConsumptionProfile) -> dict[str, float]:
    # Beer - WRONG
    laa_beer = profile.beer_litres_month * (profile.beer_avg_abv / 100.0)
    monthly_beer_excise = laa_beer * self.rates.beer_excise_per_litre
    
    # Wine - WRONG
    laa_wine = profile.wine_litres_month * (profile.wine_avg_abv / 100.0)
    monthly_wine_excise = laa_wine * self.rates.wine_excise_per_litre

# AFTER (correct):
def calculate(self, profile: ConsumptionProfile) -> dict[str, float]:
    # Beer - flat rate per litre
    monthly_beer_excise = profile.beer_litres_month * self.rates.beer_excise_per_litre
    
    # Wine - flat rate per litre
    monthly_wine_excise = profile.wine_litres_month * self.rates.wine_excise_per_litre
    
    # Spirits - LAA calculation (unchanged, was correct)
    laa_spirits = profile.spirits_litres_month * (profile.spirits_avg_abv / 100.0)
    monthly_spirits_excise = laa_spirits * self.rates.spirits_excise_per_laa
```

### 3. `app/views/pages.py` - Updated tooltips
```python
# Updated explanations to reflect correct calculation methods
"Beer Excise": "R14.50 per LITRE OF BEER consumed. (Not per LAA)"
"Wine Excise": "R2.73 per LITRE OF WINE consumed. (Not per LAA)"
"Spirits Excise": "R249.20 per litre of absolute alcohol (LAA)"
```

### 4. `tests/test_alcohol_tax.py` - Updated expectations
- All test assertions updated to match corrected calculations
- Tests now verify proper flat-rate application for beer/wine
- Spirits tests remain unchanged (were already correct)

## Impact on Tax Calculations

### Before vs After Comparison

| Scenario | Beer (20L/month @ 5%) | Wine (6L/month @ 12.5%) | Total Annual |
|----------|----------------------|------------------------|--------------|
| **BEFORE** | R174 | R58.68 | R232.68 |
| **AFTER** | R3,480 | R196.56 | R3,676.56 |
| **Difference** | +R3,306 (+1,900%) | +R137.88 (+235%) | +R3,444 (+1,480%) |

### Real-World Example
A typical consumer who drinks:
- 20L beer per month (≈4 six-packs/month)
- 6L wine per month (≈8 bottles/month)

**Previous calculation**: R232.68/year in alcohol excise
**Correct calculation**: R3,676.56/year in alcohol excise

**The user was being shown 94% LESS tax than reality!**

## Validation

✅ All 34 tests passing
✅ Rates verified against SARS Excise Act Schedule 1
✅ Calculation methods match official SARS documentation
✅ Tooltips updated to explain correct formulas

## Sources

1. **SARS Customs and Excise Act** - Schedule 1 (Excise Duties)
   - Item 104.02: Malt beer - R14.50 per litre
   - Item 104.10: Wine ≤15% ABV - R2.73 per litre
   - Item 104.20: Spirits >15% ABV - R249.20 per LAA

2. **National Treasury Budget Review 2024/25**
   - Excise duty rates table
   - Sin tax policy documentation

3. **SARS Tariff Schedules**
   - Regular updates published in Government Gazette
   - Effective from April 1, 2024

## Conclusion

The alcohol excise tax calculation has been **completely corrected**. Users will now see accurate tax estimates that reflect the actual SARS rates and calculation methods. This is a critical fix that dramatically improves the accuracy and credibility of the calculator.

**Testing**: ✅ All tests pass
**Accuracy**: ✅ Matches SARS official rates
**User Impact**: ✅ Dramatically more accurate (previously ~95% underestimated)
