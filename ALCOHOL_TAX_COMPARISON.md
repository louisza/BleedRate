# Alcohol Tax Calculation Comparison

## Official National Treasury 2024 vs Previous Implementation

### Summary Table

| Beverage | Previous Rate | NT 2024 Rate | Calculation Method | Change |
|----------|---------------|--------------|-------------------|---------|
| **Beer** | R14.50/L | R121.41/LAA | Changed: Flat → LAA-based | -58% tax for 5% ABV |
| **Wine** | R2.73/L | R4.96/L | Same: Volumetric | +82% tax |
| **Spirits** | R249.20/LAA | R249.20/LAA | Same: LAA-based | No change |

### Detailed Comparison

#### Beer (20L/month at 5% ABV)

**Previous (Incorrect)**:
```
Formula: Litres × Rate × 12
Calculation: 20L × R14.50 × 12
Annual Tax: R3,480.00
```

**National Treasury 2024 (Correct)**:
```
Formula: Litres × (ABV% / 100) × Rate per LAA × 12
Calculation: 20L × 0.05 × R121.41 × 12
Annual Tax: R1,456.92
```

**Impact**: -R2,023.08 (-58.1%)

#### Wine (6L/month at 12.5% ABV)

**Previous (Incorrect)**:
```
Formula: Litres × Rate × 12
Calculation: 6L × R2.73 × 12
Annual Tax: R196.56
```

**National Treasury 2024 (Correct)**:
```
Formula: Litres × Rate × 12
Calculation: 6L × R4.96 × 12
Annual Tax: R357.12
```

**Impact**: +R160.56 (+81.7%)

#### Spirits (1L/month at 40% ABV)

**Previous (Correct)**:
```
Formula: Litres × (ABV% / 100) × Rate per LAA × 12
Calculation: 1L × 0.40 × R249.20 × 12
Annual Tax: R1,196.16
```

**National Treasury 2024 (Correct)**:
```
Formula: Litres × (ABV% / 100) × Rate per LAA × 12
Calculation: 1L × 0.40 × R249.20 × 12
Annual Tax: R1,196.16
```

**Impact**: No change (was already correct)

### Total Impact Example

**Typical Monthly Consumption**:
- 20L beer (5% ABV)
- 6L wine (12.5% ABV)
- 1L spirits (40% ABV)

| Beverage | Previous | NT 2024 | Change |
|----------|----------|---------|--------|
| Beer | R3,480.00 | R1,456.92 | -R2,023.08 |
| Wine | R196.56 | R357.12 | +R160.56 |
| Spirits | R1,196.16 | R1,196.16 | R0.00 |
| **TOTAL** | **R4,872.72** | **R3,010.20** | **-R1,862.52** |

**Net Impact**: -38.2% reduction in total alcohol excise

### Why the Changes?

#### Beer: LAA vs Flat Rate

**Previous Error**: Used a flat rate of R14.50 per litre regardless of alcohol content
- This was likely a misinterpretation or outdated rate
- Did not match SARS official framework

**National Treasury 2024**: Uses LAA-based calculation (R121.41 per LAA)
- Aligns with official SARS excise schedule
- Equals beer/spirits on absolute alcohol content basis
- For 5% ABV beer: Effective rate = R121.41 × 0.05 = **R6.07/L**

**Impact**: The flat R14.50 was overcharging by 139% for typical 5% beer!

#### Wine: Rate Increase

**Previous Error**: Used R2.73 per litre
- Source unknown - may have been proposed rate or outdated

**National Treasury 2024**: Uses R4.96 per litre (volumetric)
- Official SARS 2024/25 rate from excise schedule
- Volumetric taxation (NOT alcohol content based)
- Wine is uniquely taxed this way in SA framework

**Impact**: +81.7% increase to match official rate

#### Spirits: No Change

**Previous Implementation**: Already correct at R249.20/LAA
- Was using official SARS rate
- LAA calculation was correct

### Understanding LAA (Litre of Absolute Alcohol)

**Definition**: The volume of pure alcohol in a beverage

**Formula**: `LAA = Volume (litres) × (ABV% / 100)`

**Examples**:
- 1L of 5% beer = 1 × 0.05 = 0.05 LAA
- 1L of 12.5% wine = 1 × 0.125 = 0.125 LAA (but wine uses volumetric!)
- 1L of 40% spirits = 1 × 0.40 = 0.40 LAA

**Beer Tax Example**:
```
20L beer at 5% ABV
= 20 × 0.05 LAA
= 1 LAA per month
= 1 × R121.41
= R121.41 per month
= R121.41 × 12
= R1,456.92 per year
```

### Policy Context

From the National Treasury 2024 document:

**Current Framework**:
- Beer: R121.41/LAA (23% excise incidence target)
- Wine: R4.96/L volumetric (11% excise incidence target)
- Spirits: R249.20/LAA (36% excise incidence target)

**Proposed Reforms**:
1. Increase incidence targets: Wine 11%→16%, Beer 23%→28%, Spirits 36%→42%
2. Targeted band framework: Annual adjustments capped at inflation + 0-10%
3. 3-band progressive systems for wine and beer based on ABV
4. Potential move of wine to LAA-based taxation

**Public Health Goals**:
- Reduce harmful alcohol consumption (59% of consumers engage in heavy episodic drinking)
- WHO Global Strategy compliance
- Price intervention to target affordability

### Verification Sources

1. **SARS Excise Schedule 1** (2024/25 fiscal year)
   - Beer/Fermented: R121.41 per LAA
   - Wine (≤16.5% ABV): R4.96 per litre
   - Spirits: R249.20 per LAA

2. **National Treasury (2024)**: *The Taxation of Alcoholic Beverages*
   - Comprehensive policy review
   - Current rates and proposed reforms
   - Public health context

3. **Test Validation**: All 34 tests passing with NT 2024 rates ✅

### Calculator Implementation

**Files Updated**:
- `data/tax_rates.yml`: Official NT 2024 rates
- `app/domain/calculators.py`: LAA calculation for beer
- `app/domain/rates.py`: New rate field structure
- `app/views/pages.py`: Updated tooltip explanations
- `tests/*.py`: Updated all test expectations

**Result**: Calculator now 100% aligned with official National Treasury 2024 framework.
