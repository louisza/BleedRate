# National Treasury 2024 Alcohol Tax Framework Update

## Executive Summary

This document summarizes the updates made to the SA Tax Footprint Calculator to align with the **National Treasury 2024 - The Taxation of Alcoholic Beverages** policy framework.

## Key Changes

### 1. Updated to Official SARS Rates (2024/25)

#### Beer/Fermented Beverages
- **NEW Rate**: R121.41 per litre of absolute alcohol (LAA)
- **Calculation Method**: LAA-based
- **Formula**: `Litres × (ABV% / 100) × R121.41 × 12 months`
- **Example**: 20L beer at 5% ABV = 20 × 0.05 × R121.41 × 12 = **R1,456.92/year**

**Previous (Incorrect)**: Was using R14.50 per litre of beer (flat rate)

#### Wine
- **Current Rate**: R4.96 per litre of wine
- **Calculation Method**: Volumetric (NOT LAA-based)
- **Formula**: `Litres × R4.96 × 12 months`
- **Example**: 6L wine/month = 6 × R4.96 × 12 = **R357.12/year**

**Previous (Incorrect)**: Was using R2.73 per litre

#### Spirits
- **Current Rate**: R249.20 per litre of absolute alcohol (LAA)
- **Calculation Method**: LAA-based
- **Formula**: `Litres × (ABV% / 100) × R249.20 × 12 months`
- **Example**: 1L spirits at 40% ABV = 1 × 0.40 × R249.20 × 12 = **R1,196.16/year**

**Status**: No change (was already correct)

### 2. Policy Framework Context

#### Current Excise Incidence Guidelines
- Wine: 11% of weighted average retail price (proposed: 16%)
- Beer: 23% of weighted average retail price (proposed: 28%)
- Spirits: 36% of weighted average retail price (proposed: 42%)

#### Proposed Reforms (Under Consideration)

**Targeted Band Framework**:
- Annual excise adjustments between inflation (minimum) and 10% (maximum)
- Eliminates reliance on industry price changes
- Provides predictable adjustment framework

**Wine - 3-Band System** (Proposed):
1. 0.5-4.5% ABV: R4.96/L (current rate)
2. 4.5-9% ABV: R6.94/L (1.4x current)
3. 9-16.5% ABV: R8.93/L (1.8x current)

Alternative: Move wine to LAA-based taxation like beer/spirits

**Beer - 3-Band System** (Proposed):
1. 0.5-2.5% ABV: R121.41/LAA (current rate)
2. 2.5-9% ABV: R145.69/LAA (1.2x current)
3. 9-15% ABV: R169.97/LAA (1.4x current)

### 3. Technical Implementation

#### Files Updated

**data/tax_rates.yml**:
- Changed `beer_excise_per_litre` → `beer_excise_per_laa: 121.41`
- Added `beer_typical_abv: 0.05` for calculator estimates
- Changed `wine_excise_per_litre` from 2.73 → `4.96`
- Added `fortified_wine_excise_per_litre: 8.36`
- Added `spirits_typical_abv: 0.40` for calculator estimates
- Comprehensive comments explaining current framework and proposed reforms

**app/domain/rates.py**:
- Updated `TaxRates` dataclass fields
- Added new LAA-based fields for beer
- Added typical ABV fields for estimates

**app/domain/calculators.py**:
- `AlcoholTaxCalculator.calculate()` updated:
  - Beer: Now uses LAA calculation (litres × ABV% × rate)
  - Wine: Uses volumetric rate (litres × rate) - unchanged structure
  - Spirits: LAA calculation - unchanged

**app/views/pages.py**:
- Updated `TAX_EXPLANATIONS` dictionary with accurate formulas
- Added examples showing real calculations

**tests/test_alcohol_tax.py**:
- Updated all 6 test expectations to match official rates
- Beer test: R3,480 → R1,456.92
- Wine test: R196.56 → R357.12
- All tests passing ✅

**tests/test_rates.py**:
- Updated to check for LAA-based beer fields

**tests/test_api_public.py**:
- Updated API rate validation to check correct field names

### 4. Impact on Tax Calculations

#### Example: Typical Monthly Consumption

**Scenario**: 
- 20L beer at 5% ABV
- 6L wine at 12.5% ABV
- 1L spirits at 40% ABV

**Before Update** (Incorrect Rates):
- Beer: R3,480.00/year (using flat R14.50/L)
- Wine: R196.56/year (using R2.73/L)
- Spirits: R1,196.16/year (correct)
- **Total: R4,872.72/year**

**After Update** (Official National Treasury 2024):
- Beer: **R1,456.92/year** (R121.41/LAA, 5% ABV)
- Wine: **R357.12/year** (R4.96/L volumetric)
- Spirits: **R1,196.16/year** (R249.20/LAA, 40% ABV)
- **Total: R3,010.20/year**

**Net Change**: -R1,862.52/year (-38.2% reduction for this profile)

### 5. Key Insights from National Treasury Document

#### Public Health Context
- 59% of SA alcohol consumers engage in heavy episodic drinking
- Average daily consumption: 64.6 grams of pure alcohol
- Alcohol causes 5.3% of global deaths (WHO 2018)
- South Africa committed to WHO Global Strategy implementation

#### Illicit Trade
- Estimated at 14-22% of market
- Undermines health and revenue objectives
- Requires coordinated enforcement across multiple agencies

#### Minimum Unit Pricing
- Not a tax but a pricing floor mechanism
- Prevents producers absorbing tax increases
- National Treasury supports in principle
- Complements existing interventions

#### Rate Differentials
- Beer/spirits differential widened 148% (2012-2023)
- Wine/spirits differential widened 136%
- Beer/wine differential widened 118%
- Raises equity concerns across beverage types

### 6. Future Considerations

The calculator is designed to accommodate proposed reforms:
- 3-band systems can be added by updating `tax_rates.yml`
- LAA-based wine taxation ready when implemented
- Progressive rate structures supported in data model
- Typical ABV fields allow for estimate calculations

### 7. Validation

✅ All 34 tests passing (90.62% code coverage)
✅ Alcohol calculations match National Treasury 2024 framework
✅ API endpoints return correct rate structure
✅ Tooltips explain calculations accurately
✅ Documentation updated with official sources

## References

1. **National Treasury (2024)**. *The Taxation of Alcoholic Beverages*. 
   - Source document for all rate updates
   - Includes proposed reform framework
   - Public health context and policy rationale

2. **SARS Excise Schedule 1** (2024/25)
   - Official excise duty rates
   - Beer: R121.41/LAA
   - Wine: R4.96/L
   - Spirits: R249.20/LAA

3. **WHO Global Strategy** (2022-2030)
   - Action Plan to reduce harmful alcohol use
   - Tax policy as public health intervention

## Summary

The calculator now accurately reflects the **official National Treasury 2024 alcohol tax framework**, including:
- LAA-based calculation for beer (R121.41/LAA)
- Volumetric taxation for wine (R4.96/L)
- Current policy guidelines and proposed reforms
- Comprehensive documentation and test coverage

All calculations are **verified against official SARS rates** and the **National Treasury 2024 policy document**.
