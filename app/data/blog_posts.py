"""
Blog posts data for BleedRate.
All content is original and written for South African tax education.
"""

BLOG_POSTS = [
    {
        "slug": "how-much-tax-do-south-africans-really-pay",
        "title": "How Much Tax Do South Africans Really Pay? Beyond PAYE",
        "meta_description": "Most South Africans only see PAYE on their payslip, but your real tax footprint is 2-3x higher. Discover fuel levies, VAT, municipal charges and hidden taxes in this 2026/27 guide.",
        "published": "2026-03-01",
        "updated": "March 2026",
        "tax_year": "2026/27",
        "reading_time": "7 min",
        "content": """
<p class="text-lg text-gray-300 mb-6">
  Ask most South Africans how much tax they pay, and they'll tell you what's on their payslip: PAYE. 
  If you earn R40,000 per month, your PAYE might be around R7,000 — about 17.5% of your gross salary. 
  Painful, but manageable. 
  The problem? That number is just the beginning.
</p>

<p class="mb-4">
  Once you account for every rand flowing from your pocket to a government entity — SARS, your municipality, 
  the Road Accident Fund, the fuel levy board — the real figure for that R40,000 earner looks more like 
  <strong class="text-red-300">R16,000 to R18,000 per month</strong>. That's 40–45% of your gross income. 
  Here's where it all goes.
</p>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">1. PAYE — The Tax You Can See</h2>

<p class="mb-4">
  For the 2026/27 tax year, South Africa has seven income tax brackets ranging from 18% on the first 
  R245,100 of taxable income to 45% on income above R1,878,600. For our R40,000/month earner (R480,000/year):
</p>

<ul class="list-disc list-inside ml-4 mb-6 space-y-2 text-gray-300">
  <li>Taxable income: ~R450,000 (after retirement contribution deduction)</li>
  <li>Marginal rate: 31%</li>
  <li>PAYE (before rebate): ~R101,000/year</li>
  <li>Less primary rebate: R17,820</li>
  <li>Less medical aid credits (2 members): R7,920</li>
  <li><strong class="text-white">Net PAYE: ~R75,845/year (R6,320/month)</strong></li>
</ul>

<p class="mb-4">
  So yes, PAYE is real and significant. But it's the visible 40% of your total tax bill, not 100%.
</p>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">2. VAT at 15% — On Almost Everything You Buy</h2>

<p class="mb-4">
  Value-Added Tax (VAT) is charged at 15% on virtually every purchase you make — groceries (except 
  zero-rated basics), clothing, electronics, restaurant meals, subscriptions, and services. 
  If our R40,000 earner spends R25,000/month after tax and savings, a significant portion of that 
  spending attracts VAT.
</p>

<p class="mb-4">
  Assuming R18,000/month is spent on VAT-able goods and services, the embedded VAT is:
  R18,000 × (15/115) = <strong class="text-red-300">R2,348/month (R28,174/year)</strong>
</p>

<p class="mb-4 bg-gray-700 rounded p-4 text-sm text-gray-300">
  <strong class="text-yellow-300">Zero-rated items</strong> (no VAT): brown bread, maize meal, milk, 
  eggs, dried beans, pilchards, rice, fresh produce, cooking oil. If you buy these staples, 
  you save the 15% on those items.
</p>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">3. Fuel Levies — R6.35 Per Litre of Petrol (Budget 2026)</h2>

<p class="mb-4">
  Every litre of petrol you pump includes government levies that have nothing to do with the 
  actual cost of crude oil:
</p>

<ul class="list-disc list-inside ml-4 mb-4 space-y-1 text-gray-300">
  <li>General Fuel Levy: R4.10/L</li>
  <li>Road Accident Fund (RAF) Levy: R2.25/L</li>
  <li>Carbon Tax component: R0.11/L</li>
  <li>Customs & Excise: R0.01/L</li>
  <li><strong class="text-white">Total government take: ~R6.54/L</strong></li>
</ul>

<p class="mb-4">
  For someone driving 1,500 km/month in a typical sedan (~12.5 L/100km), that's 187.5 litres 
  per month, meaning <strong class="text-red-300">R1,190/month (R14,276/year) in fuel levies alone</strong> (at R6.35/L statutory).
</p>

<p class="mb-4">
  Diesel users pay slightly less: approximately R6.18/L in total levies (statutory Budget 2026), offering a small saving 
  for bakkie and 4x4 drivers. Note: temporary R3.00/L GFL relief applies 1 Apr – 5 May 2026 only.
</p>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">4. The Electricity Environmental Levy</h2>

<p class="mb-4">
  Added to your Eskom or municipality bill is an environmental levy of 
  <strong class="text-red-300">R0.035 per kWh</strong>. For a household using 800 kWh/month, 
  that's R28/month (R336/year) flowing directly to government — separate from what you pay 
  for the electricity itself.
</p>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">5. Sin Taxes — Beer, Wine, Spirits, Cigarettes</h2>

<p class="mb-4">
  SARS collects excise duties on alcohol and tobacco before the product even reaches store shelves. 
  These duties are embedded in retail prices:
</p>

<ul class="list-disc list-inside ml-4 mb-4 space-y-1 text-gray-300">
  <li><strong>Beer:</strong> R149.98/litre of absolute alcohol — a 330ml can at 5% ABV adds R2.50 to SARS</li>
  <li><strong>Wine:</strong> R6.15/litre — a R120 bottle includes ~R6 in excise duty</li>
  <li><strong>Spirits:</strong> R302.84/litre of absolute alcohol — a R400 bottle of whiskey (43% ABV) includes ~R131 in duty</li>
  <li><strong>Cigarettes:</strong> R22.81 per 20-pack OR 30% of retail price (whichever is higher)</li>
</ul>

<p class="mb-4">
  A moderate drinker buying 15L of beer and 3L of wine per month sends roughly 
  <strong class="text-red-300">R500/month to SARS in sin taxes</strong> — R6,000/year.
</p>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">6. Municipal Rates and Services</h2>

<p class="mb-4">
  Property rates, water tariffs, sewerage, refuse removal — all of these flow to your local 
  municipality (a government entity). For a middle-income household in Tshwane or Johannesburg:
</p>

<ul class="list-disc list-inside ml-4 mb-4 space-y-1 text-gray-300">
  <li>Property rates on a R2M home: ~R1,400/month</li>
  <li>Water + sewerage: ~R600/month</li>
  <li>Refuse removal: ~R300/month</li>
  <li>Electricity (municipal tariff): ~R1,200/month</li>
  <li><strong class="text-white">Total municipal payments: ~R3,500/month (R42,000/year)</strong></li>
</ul>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">7. The Hidden Tax: Corporate Tax in Every Price</h2>

<p class="mb-4">
  Every company in South Africa pays 27% Corporate Income Tax (CIT) on its profits. 
  Those costs don't disappear — they're embedded in the prices you pay. 
  Economists estimate that 40–50% of corporate tax burden ultimately passes through to consumers 
  in the form of higher prices.
</p>

<p class="mb-4">
  On top of that, companies pay 1% of payroll as the Skills Development Levy (SDL) and 
  1% as employer UIF contributions. These labour taxes also flow into retail prices.
</p>

<p class="mb-4">
  Across your R25,000/month in spending, the hidden embedded corporate and regulatory tax 
  component is estimated at <strong class="text-red-300">R1,500–R2,000/month</strong>.
</p>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">The Full Picture: R40,000 Earner</h2>

<div class="bg-gray-900 rounded border border-red-900 p-6 mb-6 overflow-x-auto">
  <table class="w-full text-sm text-left">
    <thead>
      <tr class="text-red-300 border-b border-gray-700">
        <th class="pb-2 pr-6">Tax Component</th>
        <th class="pb-2 text-right">Monthly</th>
        <th class="pb-2 text-right">Annual</th>
      </tr>
    </thead>
    <tbody class="text-gray-300 space-y-1">
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">PAYE (income tax)</td>
        <td class="py-2 text-right">R6,320</td>
        <td class="py-2 text-right">R75,840</td>
      </tr>
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">UIF (1% of salary)</td>
        <td class="py-2 text-right">R177</td>
        <td class="py-2 text-right">R2,124</td>
      </tr>
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">VAT (on spending)</td>
        <td class="py-2 text-right">R2,348</td>
        <td class="py-2 text-right">R28,174</td>
      </tr>
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">Fuel levies (187.5L/month)</td>
        <td class="py-2 text-right">R1,187</td>
        <td class="py-2 text-right">R14,244</td>
      </tr>
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">Municipal rates &amp; services</td>
        <td class="py-2 text-right">R3,500</td>
        <td class="py-2 text-right">R42,000</td>
      </tr>
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">Electricity levy</td>
        <td class="py-2 text-right">R28</td>
        <td class="py-2 text-right">R336</td>
      </tr>
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">Sin taxes (alcohol/tobacco)</td>
        <td class="py-2 text-right">R500</td>
        <td class="py-2 text-right">R6,000</td>
      </tr>
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">Embedded corporate tax</td>
        <td class="py-2 text-right">R1,750</td>
        <td class="py-2 text-right">R21,000</td>
      </tr>
      <tr class="font-bold text-red-200">
        <td class="py-3 pr-6">TOTAL TAX FOOTPRINT</td>
        <td class="py-3 text-right text-red-300">~R15,810</td>
        <td class="py-3 text-right text-red-300">~R189,718</td>
      </tr>
    </tbody>
  </table>
</div>

<p class="mb-4">
  That's approximately <strong class="text-red-300">39.5% of a R480,000/year salary</strong> 
  flowing to government in one form or another. Not 17.5%. Not even 25%. 
  Nearly 40 cents of every rand you earn ends up in a government account.
</p>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">Why This Matters</h2>

<p class="mb-4">
  Understanding your real tax footprint isn't about resenting the government — taxes fund hospitals, 
  roads, schools, and social grants that millions depend on. But knowledge is power. 
  When you know where your money goes, you can:
</p>

<ul class="list-disc list-inside ml-4 mb-4 space-y-1 text-gray-300">
  <li>Make smarter financial planning decisions (retirement annuities, medical aid)</li>
  <li>Understand why increasing your salary doesn't proportionally increase your take-home</li>
  <li>Budget more accurately by including all your tax obligations, not just PAYE</li>
  <li>Engage more meaningfully with tax policy debates</li>
</ul>

<p class="mb-6">
  Use the <a href="/" class="text-red-400 hover:text-red-300 underline">BleedRate calculator</a> 
  to enter your specific income, spending habits, and lifestyle — and get your personalised tax 
  footprint number.
</p>
""",
    },
    {
        "slug": "sars-tax-brackets-2025-2026-explained",
        "title": "SARS Tax Brackets 2025/26: What You Actually Keep",
        "meta_description": "The 2025/26 SARS tax brackets explained — marginal vs effective rates, rebates, medical aid credits. Find out what you actually take home on any salary.",
        "published": "2026-03-02",
        "updated": "March 2026",
        "tax_year": "2026/27",
        "reading_time": "6 min",
        "content": """
<p class="text-lg text-gray-300 mb-6">
  "I got a raise, but I'm taking home less because it pushed me into a higher tax bracket." 
  You've heard someone say this. It might even be you. 
  The good news: it's almost certainly not true — but understanding why requires knowing 
  how South Africa's progressive tax system actually works.
</p>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">The Seven SARS Tax Brackets (2026/27)</h2>

<p class="mb-4">
  For the tax year ending 28 February 2025, SARS applies the following brackets to taxable income 
  (salary + bonuses minus approved deductions like retirement contributions):
</p>

<div class="bg-gray-900 rounded border border-red-900 p-6 mb-6 overflow-x-auto">
  <table class="w-full text-sm text-left">
    <thead>
      <tr class="text-red-300 border-b border-gray-700">
        <th class="pb-2 pr-6">Taxable Income</th>
        <th class="pb-2 text-right">Rate</th>
        <th class="pb-2 text-right">Tax on this slice</th>
      </tr>
    </thead>
    <tbody class="text-gray-300">
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">R1 – R245,100</td>
        <td class="py-2 text-right">18%</td>
        <td class="py-2 text-right">R42,678 max</td>
      </tr>
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">R237,101 – R370,500</td>
        <td class="py-2 text-right">26%</td>
        <td class="py-2 text-right">R34,684 max</td>
      </tr>
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">R370,501 – R512,800</td>
        <td class="py-2 text-right">31%</td>
        <td class="py-2 text-right">R44,119 max</td>
      </tr>
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">R512,801 – R673,000</td>
        <td class="py-2 text-right">36%</td>
        <td class="py-2 text-right">R57,672 max</td>
      </tr>
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">R673,001 – R857,900</td>
        <td class="py-2 text-right">39%</td>
        <td class="py-2 text-right">R72,111 max</td>
      </tr>
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">R887,001 – R1,878,600</td>
        <td class="py-2 text-right">41%</td>
        <td class="py-2 text-right">R393,249 max</td>
      </tr>
      <tr>
        <td class="py-2 pr-6">R1,817,001+</td>
        <td class="py-2 text-right">45%</td>
        <td class="py-2 text-right">No cap</td>
      </tr>
    </tbody>
  </table>
</div>

<p class="mb-4">
  <strong class="text-red-300">Key principle:</strong> Each bracket rate applies only to the 
  income within that bracket — not to your entire salary. This is what "progressive" means.
</p>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">Marginal Rate vs. Effective Rate</h2>

<p class="mb-4">
  <strong class="text-white">Marginal rate</strong> = the rate applied to your last rand of income. 
  If you earn R370,501, your marginal rate just tipped into 31%.
</p>

<p class="mb-4">
  <strong class="text-white">Effective rate</strong> = what percentage of your total income goes 
  to PAYE. This is always lower than your marginal rate.
</p>

<p class="mb-4 font-semibold">
  Example: R360,000 annual income (R30,000/month):
</p>

<ul class="list-disc list-inside ml-4 mb-6 space-y-1 text-gray-300">
  <li>First R245,100 taxed at 18% = R44,118</li>
  <li>Remaining R122,900 taxed at 26% = R31,954</li>
  <li>Total tax before rebate: R74,632</li>
  <li>Less primary rebate: <strong>–R17,820</strong></li>
  <li><strong class="text-white">Tax payable: R57,397/year (R4,783/month)</strong></li>
  <li><strong class="text-red-300">Effective rate: 15.9%</strong> — NOT the 26% marginal rate</li>
</ul>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">Rebates: The Tax You Don't Actually Pay</h2>

<p class="mb-4">
  Rebates are subtracted directly from your tax bill (not your income). 
  SARS provides three age-based rebates for 2026/27:
</p>

<ul class="list-disc list-inside ml-4 mb-6 space-y-2 text-gray-300">
  <li><strong class="text-white">Primary Rebate:</strong> R17,820 — for all taxpayers under 65</li>
  <li><strong class="text-white">Secondary Rebate:</strong> R9,765 (additional) — for taxpayers aged 65 and over</li>
  <li><strong class="text-white">Tertiary Rebate:</strong> R3,249 (additional) — for taxpayers aged 75 and over</li>
</ul>

<p class="mb-4">
  The <strong class="text-white">tax threshold</strong> is the income at which the rebate offsets 
  all tax liability. For 2026/27:
</p>

<ul class="list-disc list-inside ml-4 mb-6 space-y-1 text-gray-300">
  <li>Under 65: <strong class="text-white">R99,000</strong> — no PAYE below this income</li>
  <li>Age 65–74: R153,250</li>
  <li>Age 75+: R171,300</li>
</ul>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">Medical Aid Credits</h2>

<p class="mb-4">
  Medical Aid Tax Credits (MTC) reduce your PAYE liability directly:
</p>

<ul class="list-disc list-inside ml-4 mb-4 space-y-1 text-gray-300">
  <li>Main member: <strong class="text-white">R376/month</strong></li>
  <li>First dependant: R376/month</li>
  <li>Each additional dependant: R254/month</li>
</ul>

<p class="mb-4">
  A family of four (main member + 3 dependants) saves R4,368/year in PAYE through medical 
  aid credits — provided their medical aid contributions are to a registered scheme.
</p>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">Busting the "Bonus Bracket" Myth</h2>

<p class="mb-4">
  "My annual bonus pushed me into a higher bracket, so I'm worse off."
</p>

<p class="mb-4 text-gray-300">
  This cannot happen in a progressive tax system. Here's why: only the portion of your bonus 
  that falls into the higher bracket is taxed at the higher rate. Every rand below the bracket 
  threshold is still taxed at the lower rates.
</p>

<p class="mb-4">
  <strong>Example:</strong> You earn R370,500 (top of the 26% bracket). 
  You receive a R10,000 bonus:
</p>

<ul class="list-disc list-inside ml-4 mb-4 space-y-1 text-gray-300">
  <li>R10,000 enters the 31% bracket</li>
  <li>Tax on the bonus: R3,100</li>
  <li>Net bonus in your pocket: R6,900</li>
  <li>Every rand of your base salary is still taxed at the same rates as before</li>
</ul>

<p class="mb-4">
  You always take home more after a bonus. The higher marginal rate only applies to the 
  incremental income, not your whole salary.
</p>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">Retirement Contributions: Your Best Tax Reducer</h2>

<p class="mb-4">
  Contributions to an approved retirement fund (pension, provident, RA) are deductible before 
  calculating taxable income — up to 27.5% of the higher of remuneration or taxable income, 
  capped at R350,000/year.
</p>

<p class="mb-4">
  If you earn R480,000/year and contribute R66,000 (13.75%) to your RA, your taxable income 
  drops to R414,000. That saves you approximately R18,480 in PAYE — a direct, legal, 
  SARS-approved tax reduction.
</p>

<p class="mb-6">
  Want to see exactly what your PAYE comes to — and what you could save with retirement 
  contributions? Use the <a href="/" class="text-red-400 hover:text-red-300 underline">BleedRate 
  tax calculator</a> to enter your figures and get a personalised breakdown.
</p>
""",
    },
    {
        "slug": "fuel-levy-south-africa-2025",
        "title": "Fuel Levy 2026: How Much Does Government Take Per Litre of Petrol?",
        "meta_description": "R6.35 per litre of petrol goes to government (statutory Budget 2026 rates). Here's the full breakdown of the South African fuel levy, RAF levy, and carbon tax — and how much you pay per year.",
        "published": "2026-03-03",
        "updated": "April 2026",
        "tax_year": "2026/27",
        "reading_time": "5 min",
        "content": """
<p class="text-lg text-gray-300 mb-6">
  When you pull up to a petrol pump in South Africa, you see a single price per litre. 
  But buried in that number are multiple government levies that make up a substantial 
  portion of what you pay. For 2026, the total government take on a litre of 95-octane 
  inland petrol is approximately <strong class="text-red-300">R6.35 per litre</strong> (statutory Budget 2026 rates).
</p>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">Breaking Down the Government Component of Petrol</h2>

<div class="bg-gray-900 rounded border border-red-900 p-6 mb-6 overflow-x-auto">
  <table class="w-full text-sm text-left">
    <thead>
      <tr class="text-red-300 border-b border-gray-700">
        <th class="pb-2 pr-6">Levy Component</th>
        <th class="pb-2 text-right">Amount per Litre</th>
        <th class="pb-2">Purpose</th>
      </tr>
    </thead>
    <tbody class="text-gray-300">
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">General Fuel Levy</td>
        <td class="py-2 text-right">R4.10</td>
        <td class="py-2 pl-4">National Treasury / fiscus</td>
      </tr>
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">Road Accident Fund (RAF) Levy</td>
        <td class="py-2 text-right">R2.25</td>
        <td class="py-2 pl-4">RAF compensation claims</td>
      </tr>
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">Carbon Tax component</td>
        <td class="py-2 text-right">R0.19</td>
        <td class="py-2 pl-4">Climate change / National Treasury (component of GFL)</td>
      </tr>
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">Customs &amp; Excise</td>
        <td class="py-2 text-right">R0.01</td>
        <td class="py-2 pl-4">SARS import revenue</td>
      </tr>
      <tr class="font-bold text-red-200">
        <td class="py-3 pr-6">Total Government Levies</td>
        <td class="py-3 text-right text-red-300">R6.35</td>
        <td class="py-3"></td>
      </tr>
    </tbody>
  </table>
</div>

<p class="mb-4 text-gray-400 text-sm">
  * Figures are statutory Budget 2026 rates (permanent from 6 May 2026). The fuel price is regulated by the Department of Mineral 
  Resources and Energy (DMRE) and changes monthly. Levies are fixed by Parliament and change annually.
</p>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">The General Fuel Levy: Government's Petrol Tax</h2>

<p class="mb-4">
  At R4.10/L, the General Fuel Levy is the largest levy component (increased from R4.03 in Budget 2026). 
  Unlike the RAF levy (which funds a specific scheme), the General Fuel Levy flows directly to National Treasury as 
  general government revenue.
</p>

<div class="bg-yellow-950 border border-yellow-700 rounded p-4 mb-4">
  <p class="text-yellow-200 font-semibold mb-1">&#9888;&#65039; Temporary April 2026 Relief</p>
  <p class="text-yellow-100 text-sm">
    Due to the global oil price spike, government implemented a temporary R3.00/L GFL reduction 
    from <strong>1 April to 5 May 2026</strong>. During this period, the effective petrol GFL is R1.10/L 
    and diesel GFL is R0.93/L — bringing the total government levy to R3.35/L (petrol) and R3.18/L (diesel). 
    The statutory Budget 2026 rates (R4.10/L petrol, R3.93/L diesel) resume from 6 May 2026.
  </p>
</div>

<p class="mb-4">
  South Africa's General Fuel Levy is one of the highest in sub-Saharan Africa. 
  It applies equally to petrol and diesel (though diesel has a slightly lower rate: ~R3.93/L 
  for the general levy component).
</p>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">The Road Accident Fund Levy: Insurance You Pay Per Litre</h2>

<p class="mb-4">
  The RAF levy of <strong class="text-red-300">R2.25/L</strong> funds the Road Accident Fund — 
  a state scheme that compensates victims of road accidents for loss of earnings, medical 
  expenses, and general damages.
</p>

<p class="mb-4">
  In principle, the RAF levy means that every driver contributes to a shared compensation 
  pool based on how much they drive (and therefore how much fuel they use). 
  However, the RAF is chronically underfunded despite rising levies — the organisation 
  carries billions in claims liabilities and has been subject to multiple court orders 
  for non-payment to claimants.
</p>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">How Much Does an Average Driver Pay Per Year?</h2>

<p class="mb-4">
  Let's put these numbers in context. Statistics South Africa estimates the average private 
  vehicle drives approximately 15,000 km per year (1,250 km/month). For a sedan consuming 
  8L/100km:
</p>

<ul class="list-disc list-inside ml-4 mb-4 space-y-1 text-gray-300">
  <li>Annual fuel consumption: 1,200 litres</li>
  <li>Total fuel levies: 1,200 × R6.35 = <strong class="text-red-300">R7,620/year (R635/month)</strong></li>
  <li>Of which to National Treasury (General Levy): R4,920/year</li>
  <li>Of which to the RAF: R2,700/year</li>
</ul>

<p class="mb-4">
  For a bakkie or SUV doing 12L/100km over the same distance:
</p>

<ul class="list-disc list-inside ml-4 mb-6 space-y-1 text-gray-300">
  <li>Annual fuel consumption: 1,800 litres</li>
  <li>Total fuel levies: 1,800 × R6.35 = <strong class="text-red-300">R11,430/year (R952.50/month)</strong></li>
</ul>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">Diesel vs. Petrol Levies</h2>

<p class="mb-4">
  Diesel users (bakkies, trucks, generators) pay slightly less in levies: approximately 
  <strong class="text-white">R6.18/L</strong> total (statutory Budget 2026), with the general fuel levy at R3.93/L 
  and RAF levy at R2.25/L. The small differential reflects a historical concession 
  to commercial transport and agriculture.
</p>

<p class="mb-4">
  Note that diesel users do not pay a carbon tax via the fuel levy — they pay it through 
  a separate carbon tax mechanism under the Carbon Tax Act 15 of 2019.
</p>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">The Carbon Tax Component</h2>

<p class="mb-4">
  South Africa introduced a Carbon Tax in 2019. The carbon fuel levy is now R0.19/L for petrol 
  and R0.23/L for diesel (Budget 2026), embedded within the General Fuel Levy. This component has 
  increased incrementally each year in line with the Carbon Tax Act's trajectory.
</p>

<p class="mb-6">
  You can include your monthly fuel consumption in the 
  <a href="/" class="text-red-400 hover:text-red-300 underline">BleedRate calculator</a> 
  to see exactly how much of your annual fuel spend goes to government levies — and how 
  it fits into your total tax footprint.
</p>
""",
    },
    {
        "slug": "vat-south-africa-what-is-zero-rated",
        "title": "VAT in South Africa: What's Taxed at 15% and What's Zero-Rated?",
        "meta_description": "South Africa charges 15% VAT on most goods and services, but some essentials are zero-rated. Full list of zero-rated items, how the math works, and how to budget for VAT.",
        "published": "2026-03-04",
        "updated": "April 2026",
        "tax_year": "2026/27",
        "reading_time": "5 min",
        "content": """
<p class="text-lg text-gray-300 mb-6">
  Value-Added Tax (VAT) at 15% is South Africa's most broadly applied tax — collected on 
  almost every commercial transaction in the country. Unlike PAYE which only affects formal 
  employees, VAT touches everyone who buys anything. 
  Understanding what's exempt — and what isn't — directly affects your budget.
</p>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">How VAT Works: The 15/115 Rule</h2>

<p class="mb-4">
  VAT is included in the retail price of goods and services. When you see a price of R115, 
  R15 of that is VAT going directly to SARS. To calculate the VAT content of any price:
</p>

<p class="mb-4 bg-gray-900 rounded p-4 font-mono text-yellow-300 text-center">
  VAT = Price × (15 ÷ 115)
</p>

<p class="mb-4">
  For example, if you spend R15,000 per month on VAT-able goods and services:
</p>

<ul class="list-disc list-inside ml-4 mb-6 space-y-1 text-gray-300">
  <li>VAT content = R15,000 × (15/115) = <strong class="text-red-300">R1,956.52</strong></li>
  <li>Pre-VAT equivalent = R15,000 - R1,956.52 = R13,043.48</li>
  <li>Government takes R1,957 every month from your R15,000 in spending</li>
</ul>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">Zero-Rated Items: No VAT on These Essentials</h2>

<p class="mb-4">
  The VAT Act includes a list of zero-rated basic foodstuffs, meaning VAT is charged at 0% 
  on these items. You're not exempt from tax on them — the seller still files a VAT return — 
  but the rate is zero. The current zero-rated food basket includes:
</p>

<div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
  <div class="bg-gray-900 rounded p-4 border border-green-900">
    <h3 class="text-green-300 font-semibold mb-3">🟢 Zero-Rated Foods</h3>
    <ul class="list-disc list-inside space-y-1 text-sm text-gray-300">
      <li>Brown bread (not white)</li>
      <li>Maize meal and samp</li>
      <li>Milk (fresh, long life, powdered)</li>
      <li>Eggs</li>
      <li>Fresh, frozen, or tinned vegetables</li>
      <li>Fresh, frozen, or tinned fruit</li>
      <li>Dried beans, lentils, split peas</li>
      <li>Pilchards and sardines (tinned)</li>
      <li>Vegetable cooking oil (not olive)</li>
      <li>Rice</li>
      <li>Edible legumes and pulses</li>
      <li>Certain infant formula</li>
    </ul>
  </div>
  <div class="bg-gray-900 rounded p-4 border border-red-900">
    <h3 class="text-red-300 font-semibold mb-3">🔴 VAT Applies at 15%</h3>
    <ul class="list-disc list-inside space-y-1 text-sm text-gray-300">
      <li>White bread, rolls, pastries</li>
      <li>Cheese and yoghurt</li>
      <li>Meat, poultry, fish (non-tinned)</li>
      <li>Breakfast cereals</li>
      <li>Sugar and confectionery</li>
      <li>Alcohol (beer, wine, spirits)</li>
      <li>Soft drinks and juices</li>
      <li>Restaurant meals</li>
      <li>Clothing and shoes</li>
      <li>Electronics and appliances</li>
      <li>Fuel (petrol, diesel)</li>
      <li>Most services</li>
    </ul>
  </div>
</div>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">VAT-Exempt Supplies: Not the Same as Zero-Rated</h2>

<p class="mb-4">
  Some supplies are <em>exempt</em> from VAT — meaning they're outside the VAT system entirely. 
  No VAT is charged and the supplier cannot claim input VAT credits. 
  Exempt supplies include:
</p>

<ul class="list-disc list-inside ml-4 mb-6 space-y-1 text-gray-300">
  <li><strong class="text-white">Residential rent:</strong> Renting a house or flat from a private landlord is VAT-exempt</li>
  <li><strong class="text-white">School fees:</strong> Tuition at schools (not all universities) is exempt</li>
  <li><strong class="text-white">Public road transport:</strong> Taxis, buses (where fares are below a certain threshold)</li>
  <li><strong class="text-white">Financial services:</strong> Interest income, insurance premiums, banking fees are largely exempt</li>
  <li><strong class="text-white">Childcare:</strong> Registered crèches and early childhood development centres</li>
</ul>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">The VAT Math on Your Monthly Budget</h2>

<p class="mb-4">
  Most middle-income South Africans spend a mix of zero-rated and standard-rated goods. 
  Let's model a household spending R20,000/month:
</p>

<div class="bg-gray-900 rounded border border-gray-700 p-6 mb-6 overflow-x-auto">
  <table class="w-full text-sm text-left">
    <thead>
      <tr class="text-red-300 border-b border-gray-700">
        <th class="pb-2 pr-6">Category</th>
        <th class="pb-2 text-right">Spend/month</th>
        <th class="pb-2 text-right">VAT rate</th>
        <th class="pb-2 text-right">VAT paid</th>
      </tr>
    </thead>
    <tbody class="text-gray-300">
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">Basic foodstuffs (zero-rated)</td>
        <td class="py-2 text-right">R2,500</td>
        <td class="py-2 text-right">0%</td>
        <td class="py-2 text-right">R0</td>
      </tr>
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">Rent (exempt)</td>
        <td class="py-2 text-right">R5,500</td>
        <td class="py-2 text-right">0%</td>
        <td class="py-2 text-right">R0</td>
      </tr>
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">Groceries (standard-rated)</td>
        <td class="py-2 text-right">R2,000</td>
        <td class="py-2 text-right">15%</td>
        <td class="py-2 text-right">R261</td>
      </tr>
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">Clothing &amp; personal care</td>
        <td class="py-2 text-right">R1,500</td>
        <td class="py-2 text-right">15%</td>
        <td class="py-2 text-right">R196</td>
      </tr>
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">Restaurants &amp; takeaways</td>
        <td class="py-2 text-right">R1,000</td>
        <td class="py-2 text-right">15%</td>
        <td class="py-2 text-right">R130</td>
      </tr>
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">Services (internet, insurance, etc.)</td>
        <td class="py-2 text-right">R2,500</td>
        <td class="py-2 text-right">15%</td>
        <td class="py-2 text-right">R326</td>
      </tr>
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">Fuel</td>
        <td class="py-2 text-right">R2,500</td>
        <td class="py-2 text-right">15%*</td>
        <td class="py-2 text-right">R326</td>
      </tr>
      <tr class="border-b border-gray-800">
        <td class="py-2 pr-6">Other retail</td>
        <td class="py-2 text-right">R2,500</td>
        <td class="py-2 text-right">15%</td>
        <td class="py-2 text-right">R326</td>
      </tr>
      <tr class="font-bold text-red-200">
        <td class="py-3 pr-6">TOTAL</td>
        <td class="py-3 text-right">R20,000</td>
        <td class="py-3 text-right">—</td>
        <td class="py-3 text-right text-red-300">R1,565</td>
      </tr>
    </tbody>
  </table>
  <p class="text-xs text-gray-500 mt-2">* Fuel VAT is embedded in the price but applies. Also includes separate fuel levies not shown here.</p>
</div>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">How to Reduce Your VAT Burden</h2>

<p class="mb-4">
  Unlike income tax, you can't claim deductions on VAT you pay as a consumer. But you can 
  strategically reduce how much VAT you pay:
</p>

<ul class="list-disc list-inside ml-4 mb-6 space-y-2 text-gray-300">
  <li><strong class="text-white">Buy zero-rated staples</strong> instead of convenience or premium equivalents</li>
  <li><strong class="text-white">Rent rather than buy</strong> services where exempt alternatives exist</li>
  <li><strong class="text-white">Cook at home</strong> rather than eating out (restaurant meals always attract VAT)</li>
  <li><strong class="text-white">Register a business</strong> — VAT vendors can claim back input VAT on business purchases</li>
</ul>

<p class="mb-6">
  The <a href="/" class="text-red-400 hover:text-red-300 underline">BleedRate calculator</a> 
  lets you enter your monthly standard-rated spending to calculate your annual VAT contribution. 
  See how it fits into your total government tax footprint.
</p>
""",
    },
    {
        "slug": "provisional-tax-freelancers-south-africa",
        "title": "Provisional Tax for South African Freelancers and Side Hustles",
        "meta_description": "Are you a freelancer, consultant, or have a side hustle in South Africa? Learn how provisional tax works, when to pay, and how to avoid SARS penalties.",
        "published": "2026-03-05",
        "updated": "March 2026",
        "tax_year": "2026/27",
        "reading_time": "6 min",
        "content": """
<p class="text-lg text-gray-300 mb-6">
  If you're a salaried employee with no other income, SARS collects your tax automatically 
  every month through PAYE — you don't have to do anything. But if you freelance, consult, 
  run a side business, or earn investment income above R30,000 per year, you're a 
  <strong class="text-red-300">provisional taxpayer</strong>, and you need to manage your 
  own tax payments during the year.
</p>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">What Is Provisional Tax?</h2>

<p class="mb-4">
  Provisional tax is not a separate tax — it's a <em>payment method</em> for your normal 
  income tax. Instead of paying at year-end when you file, provisional taxpayers make 
  estimated payments during the year based on expected income.
</p>

<p class="mb-4">
  This prevents the scenario where SARS is owed a large lump sum after assessment, 
  which many people wouldn't be able to pay. The same tax rates and brackets apply — 
  you're just paying earlier.
</p>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">Who Must Register as a Provisional Taxpayer?</h2>

<p class="mb-4">
  You must register and submit provisional tax returns if you:
</p>

<ul class="list-disc list-inside ml-4 mb-6 space-y-2 text-gray-300">
  <li>Earn income that is <strong class="text-white">not subject to PAYE</strong> 
  (freelance fees, consulting income, business income)</li>
  <li>Earn interest, dividends, or rental income above <strong class="text-white">R30,000 per year</strong> 
  (even if you're also a salaried employee)</li>
  <li>Own a company or CC that earns income (the entity is the provisional taxpayer)</li>
</ul>

<p class="mb-4">
  You are <strong class="text-white">NOT</strong> a provisional taxpayer if:
</p>

<ul class="list-disc list-inside ml-4 mb-6 space-y-1 text-gray-300">
  <li>Your only income is a salary with PAYE deducted</li>
  <li>Your "other income" (investments, side gigs) is below R30,000/year</li>
  <li>You are a pensioner whose only income is a pension from a registered pension fund</li>
</ul>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">The Two Mandatory Payment Dates</h2>

<p class="mb-4">
  The South African tax year runs from 1 March to 28/29 February. 
  Provisional taxpayers must make two payments:
</p>

<div class="bg-gray-900 rounded border border-red-900 p-6 mb-6">
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>
      <h3 class="text-yellow-300 font-bold text-lg mb-2">🗓️ First Payment: 31 August</h3>
      <p class="text-gray-300 text-sm mb-2">
        Due 6 months into the tax year. Based on your estimated annual taxable income 
        for the full year.
      </p>
      <p class="text-sm text-gray-400">
        Pay: 50% of your estimated annual tax liability, minus any PAYE already deducted.
      </p>
    </div>
    <div>
      <h3 class="text-yellow-300 font-bold text-lg mb-2">🗓️ Second Payment: 28 February</h3>
      <p class="text-gray-300 text-sm mb-2">
        Due at year-end. Based on your <em>actual</em> annual taxable income (now that 
        the year is over).
      </p>
      <p class="text-sm text-gray-400">
        Pay: Full annual tax liability minus first payment and PAYE already deducted.
      </p>
    </div>
  </div>
</div>

<p class="mb-4">
  There's also an optional <strong class="text-white">third payment on 30 September</strong> 
  (after the tax year ends) — essentially a top-up if your February payment was too low. 
  Making this top-up can avoid interest charges.
</p>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">How to Calculate Your Provisional Tax</h2>

<p class="mb-4">
  <strong>Step 1: Estimate your annual taxable income</strong>
</p>
<p class="mb-4 text-gray-300">
  Add up your salary, freelance income, rental income, interest income, investment returns — 
  minus approved deductions (retirement contributions, business expenses if you're a sole trader).
</p>

<p class="mb-4">
  <strong>Step 2: Apply the SARS brackets to get your tax liability</strong>
</p>
<p class="mb-4 text-gray-300">
  Use the 2026/27 brackets (18% to 45%) on your estimated taxable income. 
  Subtract the primary rebate (R17,820), secondary rebate if applicable, and medical tax credits.
</p>

<p class="mb-4">
  <strong>Step 3: Subtract PAYE already paid</strong>
</p>
<p class="mb-4 text-gray-300">
  If you also have a salary with PAYE deducted, subtract that from your total tax liability. 
  The remaining amount is what you owe through provisional tax.
</p>

<p class="mb-4">
  <strong>Step 4: Split across the two payments</strong>
</p>
<p class="mb-6 text-gray-300">
  Pay 50% by 31 August, and the remainder by 28 February.
</p>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">Worked Example: Freelance Graphic Designer</h2>

<ul class="list-disc list-inside ml-4 mb-6 space-y-1 text-gray-300">
  <li>Salary (with PAYE): R240,000/year</li>
  <li>Freelance income: R120,000/year</li>
  <li>RA contribution: R36,000/year</li>
  <li>Total taxable income: R240,000 + R120,000 – R36,000 = <strong class="text-white">R324,000</strong></li>
  <li>Tax on R324,000 (from brackets): ~R63,100</li>
  <li>Less primary rebate: –R17,820</li>
  <li>Total tax liability: <strong class="text-white">R45,865</strong></li>
  <li>PAYE already deducted: R21,000</li>
  <li>Provisional tax owed: <strong class="text-red-300">R24,865</strong></li>
  <li>First payment (31 Aug): R12,432</li>
  <li>Second payment (28 Feb): R12,433</li>
</ul>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">Penalties for Underpayment</h2>

<p class="mb-4">
  SARS charges a <strong class="text-red-300">20% penalty</strong> on the difference between 
  what you paid and the "basic amount" (previous year's tax liability, increased by 8%). 
  This only applies if your payment was significantly short — not for minor underestimates.
</p>

<p class="mb-4">
  Additionally, interest at the prescribed rate applies to any shortfall. 
  For 2026/27, the SARS interest rate on outstanding debt is 11.25% per annum.
</p>

<h2 class="text-2xl font-bold text-red-200 mt-8 mb-4">Practical Tips for Freelancers</h2>

<ul class="list-disc list-inside ml-4 mb-6 space-y-2 text-gray-300">
  <li><strong class="text-white">Open a dedicated tax savings account.</strong> 
  Set aside 25–30% of every invoice payment immediately for SARS.</li>
  <li><strong class="text-white">Keep meticulous records.</strong> 
  Track all income and business expenses throughout the year. 
  Home office, equipment, data, and professional development may be deductible.</li>
  <li><strong class="text-white">Use SARS eFiling.</strong> 
  Submit and pay provisional returns at 
  <a href="https://www.sarsefiling.co.za" target="_blank" rel="noopener" 
     class="text-blue-400 hover:text-blue-300 underline">sarsefiling.co.za</a>. 
  It's free and submitting online avoids late filing penalties.</li>
  <li><strong class="text-white">Use BleedRate to estimate.</strong> 
  The <a href="/" class="text-red-400 hover:text-red-300 underline">BleedRate calculator</a> 
  can help you estimate your PAYE and effective tax rate — useful as a starting point 
  for your provisional tax calculations.</li>
  <li><strong class="text-white">Consult an accountant for your first year.</strong> 
  The cost of a tax practitioner review is usually less than a SARS penalty.</li>
</ul>

<p class="mb-6">
  Provisional tax is manageable once you understand the system. 
  The key is to plan ahead: track your income throughout the year, save a portion consistently, 
  and submit on time. SARS penalties are avoidable with basic discipline.
</p>
""",
    },
]

# Build a quick lookup by slug
BLOG_POSTS_BY_SLUG = {post["slug"]: post for post in BLOG_POSTS}
