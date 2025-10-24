# Interactive Tax Category Tooltips - Implementation Summary

## What Was Added

Added interactive hover tooltips to the tax breakdown table that explain how each tax category is calculated. When users hover over any tax category name, they see a detailed explanation including formulas, rates, and the purpose of that tax.

## Files Modified

### 1. `app/templates/_breakdown_table.html`
- Added info icon (ℹ️) next to each tax category
- Implemented CSS-based tooltip using Tailwind's `group-hover` utilities
- Tooltip displays on hover with dark background for readability
- Shows tax name and detailed explanation

### 2. `app/views/pages.py`
- Added `TAX_EXPLANATIONS` dictionary with 20+ comprehensive explanations
- Each explanation includes:
  - What the tax is
  - How it's calculated (with formulas)
  - Current rates
  - Purpose/context
- Passed `TAX_EXPLANATIONS` to template in the `/calc` endpoint

### 3. `README.md`
- Added "Interactive tooltips" to features list
- Highlighted this as a key differentiator

### 4. `docs/TOOLTIPS.md` (New)
- Created comprehensive documentation
- Lists all available tooltips
- Explains implementation details
- Describes user experience benefits

## Tax Categories with Tooltips

### Income & Employment (2)
- PAYE (Income Tax) - Progressive brackets, rebates
- UIF - 1% contribution with cap

### Indirect Consumption (4)
- VAT - 15% on standard-rated goods
- Fuel Levy (Petrol) - R6.33/L breakdown
- Fuel Levy (Diesel) - R6.20/L breakdown
- Electricity Environmental Levy - R0.035/kWh

### Sin Taxes - Alcohol (3)
- Beer Excise - R14.50 per LAA formula
- Wine Excise - R6.52 per LAA formula
- Spirits Excise - R249.20 per LAA formula

### Sin Taxes - Tobacco (3)
- Cigarette Excise - Max of specific/ad valorem
- Cigar Excise - R10.96 per gram
- Pipe Tobacco Excise - R5.44 per gram

### Health & Environment (2)
- Health Promotion Levy - Sugar tax calculation
- Plastic Bag Levy - R0.32 per bag

### Transport & Property (4)
- Vehicle License Fees
- Toll Fees
- Municipal Rates
- Transfer Duty - Progressive bands

### Investment (2)
- Dividends Tax - 20% withholding
- Capital Gains Tax - 18% effective rate

## Technical Implementation

### Frontend (Pure CSS)
```html
<tr class="hover:bg-gray-50 group">
    <td class="px-4 py-3 text-sm text-gray-800 relative">
        <span class="flex items-center gap-1">
            {{ category }}
            <svg class="w-4 h-4 text-gray-400 cursor-help">...</svg>
        </span>
        <!-- Tooltip appears on group-hover -->
        <div class="hidden group-hover:block absolute...">
            <div class="font-semibold mb-1">{{ category }}</div>
            <div class="text-gray-300">{{ explanation }}</div>
        </div>
    </td>
    ...
</tr>
```

### Backend (Python)
```python
TAX_EXPLANATIONS = {
    "PAYE (Income Tax)": "Pay As You Earn - Progressive income tax...",
    "Beer Excise": "Alcohol excise on beer: R14.50 per LAA...",
    # ... 20+ more explanations
}

# Pass to template
return templates.TemplateResponse(
    "_breakdown_table.html",
    {
        ...
        "tax_explanations": TAX_EXPLANATIONS
    }
)
```

## Key Benefits

1. **Educational** - Users learn exactly how taxes are calculated
2. **Transparency** - Demystifies complex tax calculations
3. **Trust Building** - Shows accurate formulas and official rates
4. **No Performance Impact** - Pure CSS, no JavaScript required
5. **Accessible** - Visual cue (info icon) for discoverability
6. **Clean UI** - Tooltips only appear on demand, no clutter

## User Experience Flow

1. User fills out form and submits
2. Breakdown table displays with results
3. User notices small ℹ️ icon next to tax categories
4. Hovering over any row reveals detailed explanation
5. Tooltip shows:
   - Tax name (bold)
   - Detailed calculation explanation
   - Rates and formulas
   - Purpose/context

## Testing

All existing tests pass:
- ✅ 34 tests passing
- ✅ 90.58% code coverage
- ✅ No breaking changes
- ✅ Backward compatible

## Future Enhancements

Potential improvements:
- Add click-to-pin functionality for mobile users
- Include example calculations in tooltips
- Link to SARS documentation
- Add "Learn More" links for each tax type
- Show calculation breakdown (e.g., "R240,000 × 26% = R62,400")
