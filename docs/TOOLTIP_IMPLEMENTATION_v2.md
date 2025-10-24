# 💡 Tooltip Implementation Guide

## Tooltip System Added to BleedRate

### What Was Added:

1. **Interactive Help Icons** - Blue "?" circles next to confusing field labels
2. **Hover Tooltips** - Detailed explanations appear on hover/focus
3. **Plain Language** - Complex tax terms explained in everyday language
4. **Examples** - What's included vs. excluded for each field

### Tooltip Structure:

```html
<label class="block text-sm font-bold text-gray-200 mb-2">
    Field Label
    <span class="tooltip-container">
        <span class="tooltip-icon" tabindex="0">?</span>
        <span class="tooltip-text">
            <strong>What is this?</strong><br>
            Clear explanation in plain language<br>
            <div class="tooltip-example">
                ✅ Includes: List of what counts<br>
                ❌ Excludes: List of what doesn't count
            </div>
        </span>
    </span>
</label>
```

### Fields That Need Tooltips (Priority Order):

#### 🔴 **High Priority (Most Confusing)**
1. ✅ **VAT-able Spending** - Users don't know what includes VAT
2. ✅ **Accommodation** - Is it my house or hotels?
3. **Embedded Corporate Tax** - What is this?
4. **Property Transfer Duty** - When does this apply?
5. **Import Duty** - Do I pay this?
6. **Sugary Drinks** - How do I calculate this?

#### 🟡 **Medium Priority**
7. **Annual Bonus** - Is 13th cheque included?
8. **Medical Aid Members** - Who counts?
9. **Retirement Contributions** - What qualifies?
10. **Petrol/Diesel** - How to estimate liters?
11. **Electricity (kWh)** - How to find this?
12. **Beer/Wine/Spirits** - Standard drink sizes?

#### 🟢 **Nice to Have**
13. **Cigarettes/Cigars** - Pack sizes
14. **Airport Taxes** - When applicable?
15. **Investments** - Dividends vs capital gains

### Tooltip Content Guidelines:

1. **Start with a Question**: "What is this?" or "What counts?"
2. **Simple Explanation**: One sentence in plain English
3. **Includes/Excludes**: Use ✅ and ❌ emojis
4. **Examples**: Real-world scenarios
5. **Typical Values**: Help users estimate if unsure

### Example Tooltips:

#### VAT-able Spending
```
What is this?
Most things you buy include 15% VAT that goes to government.

✅ Includes: Groceries, clothes, electronics, restaurant meals
❌ Excludes: Rent, school fees, medical aid, some basic foods

Typical: R10,000 - R20,000/month
```

#### Accommodation
```
What counts as accommodation?
Only commercial accommodation like hotels, Airbnb, B&Bs.

✅ Includes: Hotels, guest houses, Airbnb, lodges
❌ Excludes: Your own home/rent, staying with friends

Typical: R5,000 - R15,000/year for holidays
```

#### Embedded Corporate Tax
```
What is this?
Companies pay 27% tax, which they pass to you in higher prices.
We estimate ~12% of your spending goes to this hidden tax.

This is automatically calculated - you don't enter anything.
```

#### Property Transfer Duty
```
When do I pay this?
Only when buying a property. It's a one-time tax.

✅ Pay if: Buying a house/flat this year
❌ Don't pay if: Renting, already own, or property under R1.1M

Enter the purchase price only if buying this year.
```

#### Annual Bonus
```
What counts as a bonus?
Any extra payments beyond your monthly salary.

✅ Includes: 13th cheque, performance bonus, commission
❌ Excludes: Regular overtime, allowances (already in salary)

Leave blank if you only get 12 months' salary.
```

#### Medical Aid Members
```
Who counts as a member?
You plus any dependents on your medical aid.

Examples:
- Just you = 1
- You + spouse = 2
- You + spouse + 2 kids = 4

This gives you a tax credit to reduce your PAYE.
```

### CSS Features:

- **Responsive**: Works on mobile and desktop
- **Accessible**: Keyboard navigable with tab+focus
- **Smooth Animations**: Fade in/out on hover
- **Professional Design**: Matches site theme
- **Non-Intrusive**: Small blue icon, doesn't clutter

### Mobile Optimization:

- Tooltips work on tap (touch devices)
- Smaller width on mobile (240px vs 280px)
- Positioned to avoid screen edges
- Readable font size on small screens

### Implementation Status:

- ✅ Tooltip CSS and JavaScript added
- ✅ VAT-able Spending - Complete with tooltip
- ✅ Accommodation - Complete with tooltip
- ⏳ Need to add ~10 more critical tooltips
- ⏳ Test on mobile devices
- ⏳ Get user feedback

### Next Steps:

1. Add tooltips to remaining high-priority fields
2. Test with real users
3. Refine explanations based on feedback
4. Consider adding "Learn More" links to docs
5. Add tooltips to results page for tax categories

### User Benefits:

- ✅ **Reduced Confusion** - Clear explanations
- ✅ **Better Estimates** - Examples help users guess
- ✅ **Increased Trust** - Shows we care about clarity
- ✅ **Higher Completion** - Less abandonment
- ✅ **Fewer Support Questions** - Self-service help

---

**Remember**: The goal is to make a complex tax calculator accessible to everyone, not just accountants!
