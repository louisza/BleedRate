# Tax Category Tooltips

## Overview

Each tax category in the breakdown table includes an interactive tooltip that explains how that specific tax is calculated. Simply hover over the ℹ️ icon next to any tax category to see the explanation.

## Available Tooltips

### Income & Employment Taxes

- **PAYE (Income Tax)**: Progressive income tax on salary and bonuses. Calculated using 7 tax brackets (18%-45%) with age-based rebates deducted.
- **UIF**: Unemployment Insurance Fund - 1% of salary (capped at R177.12/month). Mandatory contribution for income protection.

### Indirect Consumption Taxes

- **VAT**: Value Added Tax - 15% on most goods and services. Calculated from your monthly standard-rated spending (excludes zero-rated items like basic foods).
- **Fuel Levy (Petrol)**: Fuel levies on petrol: General Fuel Levy (R4.01/L) + RAF (R2.18/L) + Carbon Tax (R0.14/L) = R6.33/L. Based on litres consumed monthly.
- **Fuel Levy (Diesel)**: Fuel levies on diesel: General Fuel Levy (R3.85/L) + RAF (R2.18/L) + Carbon Tax (R0.17/L) = R6.20/L. Based on litres consumed monthly.
- **Electricity Environmental Levy**: Environmental levy on electricity: R0.035 per kWh. Applied to all electricity usage to fund renewable energy initiatives.

### Sin Taxes - Alcohol

- **Beer Excise**: Alcohol excise on beer: R14.50 per litre of absolute alcohol (LAA). Formula: Litres × (ABV%/100) × R14.50 per LAA × 12 months.
- **Wine Excise**: Alcohol excise on wine: R6.52 per litre of absolute alcohol (LAA). Formula: Litres × (ABV%/100) × R6.52 per LAA × 12 months.
- **Spirits Excise**: Alcohol excise on spirits: R249.20 per litre of absolute alcohol (LAA). Formula: Litres × (ABV%/100) × R249.20 per LAA × 12 months.

### Sin Taxes - Tobacco

- **Cigarette Excise**: Tobacco excise on cigarettes: Max of specific rate (R18.22 per 20-pack) or ad valorem (30% of retail price). Higher amount applies annually.
- **Cigar Excise**: Tobacco excise on cigars: R10.96 per gram. Calculated as grams consumed monthly × R10.96 × 12 months.
- **Pipe Tobacco Excise**: Tobacco excise on pipe tobacco: R5.44 per gram. Calculated as grams consumed monthly × R5.44 × 12 months.

### Health & Environment

- **Health Promotion Levy (HPL)**: Sugar tax on beverages exceeding 4g sugar per 100ml: R0.021 per gram of sugar above threshold. Aims to reduce sugar consumption.
- **Plastic Bag Levy**: Environmental levy on single-use plastic bags: R0.32 per bag. Encourages reusable bag usage and reduces plastic waste.

### Transport & Property

- **Vehicle License Fees**: Annual motor vehicle license fees paid to provincial government. Varies by vehicle type, weight, and province.
- **Toll Fees**: Road usage fees collected on national toll routes. Funds road maintenance and infrastructure development.
- **Municipal Rates**: Property rates and service charges paid to local municipality. Based on property value and services used (water, waste, etc.).
- **Transfer Duty**: One-time tax on property purchases over R1.21M. Progressive rates: 0% up to R1.21M, then 3%-13% on amounts above thresholds.

### Investment Taxes

- **Dividends Tax**: Withholding tax on dividends from SA companies: 20% of dividend amount. Deducted at source before payment to shareholders.
- **Capital Gains Tax (CGT)**: Tax on profit from asset sales. Effective rate: 18% (40% inclusion × 45% marginal rate). Applied to net capital gains after R40k annual exclusion.

## Implementation Details

The tooltips are implemented using:
- **Pure CSS**: Tailwind CSS utility classes for styling
- **HTML Attributes**: No JavaScript required for basic functionality
- **Responsive Design**: Tooltips position automatically based on available space
- **Accessibility**: Info icon provides visual cue for hover interaction

### Technical Implementation

```html
<span class="flex items-center gap-1">
    {{ category }}
    <svg class="w-4 h-4 text-gray-400 cursor-help" ...>
        <!-- Info icon -->
    </svg>
</span>
<!-- Tooltip -->
<div class="hidden group-hover:block absolute ...">
    <div class="font-semibold mb-1">{{ category }}</div>
    <div class="text-gray-300">{{ explanation }}</div>
</div>
```

The explanations are stored in a Python dictionary (`TAX_EXPLANATIONS`) in `app/views/pages.py` and passed to the template for rendering.

## User Experience

1. **Visual Cue**: Each tax category has a small ℹ️ info icon
2. **Hover Interaction**: Moving your mouse over the row reveals the tooltip
3. **Dark Tooltip**: Dark background ensures readability against light page background
4. **Comprehensive Info**: Includes rates, formulas, and purpose of each tax
5. **No Clutter**: Tooltips only appear on hover, keeping the interface clean

## Benefits

- **Educational**: Users learn exactly how each tax is calculated
- **Transparency**: Demystifies complex tax calculations
- **Verification**: Users can manually verify calculations if desired
- **Trust**: Shows the application uses official tax rates and formulas
