"""View handlers for server-rendered pages"""
import hashlib
from typing import Optional
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.config import settings
from app.domain.rates import TaxRates
from app.domain.profiles import PersonalProfile, ConsumptionProfile, TransportAndPropertyProfile, InvestmentProfile, TravelProfile
from app.domain.engine import TaxEngine
from app.services.logger import submission_logger

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))


# Tax explanation tooltips - emphasizing money flow to government
TAX_EXPLANATIONS = {
    "PAYE (Income Tax)": "Money to Government: Progressive income tax deducted from every paycheck. Government takes 18%-45% based on 7 tax brackets, minus age-based rebates. This flows directly to National Treasury.",
    "UIF": "Money to Government: 1% of your salary (capped at R177.12/month) goes to the Unemployment Insurance Fund. Both you and your employer contribute.",
    "VAT": "Money to Government: 15% of every Rand you spend on most goods and services goes straight to SARS. Every purchase you make includes this government charge.",
    "Fuel Levy (Petrol)": "Money to Government: R6.33 of every litre of petrol goes to government (R4.01 General Fuel Levy + R2.18 RAF + R0.14 Carbon Tax). Based on your monthly fuel consumption.",
    "Fuel Levy (Diesel)": "Money to Government: R6.20 of every litre of diesel goes to government (R3.85 General Fuel Levy + R2.18 RAF + R0.17 Carbon Tax). Based on your monthly fuel consumption.",
    "Electricity Environmental Levy": "Money to Government: R0.035 per kWh of your electricity bill goes to government for renewable energy funding. Adds up with every unit consumed.",
    "Health Promotion Levy (HPL)": "Money to Government: R0.021 per gram of sugar above 4g/100ml threshold. Government collects this 'sin tax' on sugary beverages to discourage consumption.",
    "Beer Excise": "Money to Government: R121.41 per litre of absolute alcohol (LAA) goes to SARS. Formula: Litres × (ABV%/100) × R121.41 × 12 months. Example: 20L at 5% ABV = R1,456.92/year to government.",
    "Wine Excise": "Money to Government: R4.96 per litre of wine (regardless of alcohol content) goes to SARS. Formula: Litres × R4.96 × 12 months. Example: 6L/month = R357.12/year to government.",
    "Spirits Excise": "Money to Government: R249.20 per litre of absolute alcohol goes to SARS. Formula: Litres × (ABV%/100) × R249.20 × 12 months. Example: 1L at 40% ABV = R1,196.16/year to government.",
    "Cigarette Excise": "Money to Government: SARS takes max of R18.22 per 20-pack or 30% of retail price - whichever is higher. Heavy 'sin tax' on tobacco products.",
    "Cigar Excise": "Money to Government: R10.96 per gram of cigars smoked goes to SARS annually. Luxury tobacco excise tax.",
    "Pipe Tobacco Excise": "Money to Government: R5.44 per gram of pipe tobacco consumed goes to government coffers annually.",
    "Plastic Bag Levy": "Money to Government: R0.32 per plastic bag goes to environmental fund. Small but adds up with every shopping trip.",
    "Vehicle License Fees": "Money to Government: Annual license fees go to provincial government. Varies by vehicle type, weight, and province - mandatory to legally drive.",
    "Toll Fees": "Money to Government: Road usage fees collected on toll routes - funds road maintenance but operated by SANRAL (state-owned entity).",
    "Municipal Rates": "Money to Government: Property rates and service charges go to your local municipality (government). Based on property value and services consumed.",
    "Transfer Duty": "Money to Government: One-time property purchase tax (3%-13% on amounts above R1.21M) goes straight to SARS when you buy property.",
    "Vehicle Import Duty (in installments)": "Money to Government: 25% import duty on vehicles NOT assembled in SA. If financing imported vehicle, ~20% of EVERY monthly installment is government duty. DUTY-FREE (locally assembled): VW Polo/Vivo, Toyota Corolla Cross/Fortuner, Mercedes C-Class, BMW X3. IMPORTED (25% to government): Most European/Asian brands.",
    "Dividends Tax": "Money to Government: 20% of dividend income withheld by SARS before you receive payment. Government takes its cut before money reaches your account.",
    "Capital Gains Tax (CGT)": "Money to Government: 18% effective rate (40% inclusion × 45% marginal) on profit from asset sales above R40k annual exclusion. Government's share of your investment gains.",
    
    # Embedded Corporate Taxes - highlighting hidden government revenue
    "Corporate Income Tax (embedded)": "HIDDEN Money to Government: Companies pay 27% CIT on profits, but YOU pay through higher prices. Economic research shows 40-50% of corporate tax burden passes to consumers. This is government revenue hidden in every price tag.",
    "SDL/UIF Employer Contribution (embedded)": "HIDDEN Money to Government: Employers pay 1% SDL + 1% UIF, but costs pass to you through prices. Employment taxes funded by your purchases, estimated at ~15% of embedded government revenue.",
    "Tax Administration Costs (embedded)": "HIDDEN Money to Government: Companies spend 0.5-1% of revenue on tax compliance systems and audits - these costs are built into your prices. Government regulations create costs you ultimately bear.",
    "Regulatory Compliance Costs (embedded)": "HIDDEN Money to Government: BBBEE compliance, labour audits, environmental regulations, industry levies - businesses pay 2-5% of turnover in regulatory costs, all passed to you through pricing. Government-mandated expenses in every purchase.",
    "Supply Chain Tax Cascade (embedded)": "HIDDEN Money to Government: Each supplier (raw materials → manufacturer → distributor → retailer) pays corporate taxes before reaching you. Multiple layers of government revenue hidden in final price. ~15% of total embedded tax burden.",
    
    # Additional levies
    "Tyre Levy": "Money to Government: R2.30 per kg of tyre mass goes to government environmental fund. Typical passenger car tyre (~10kg) = R23 per tyre. Formula: Tyres × Weight × R2.30. Funds waste management and recycling programs.",
    "TV License": "Money to Government: R265 per year goes to SABC (state broadcaster) if you own a TV or device capable of receiving broadcasts. Legally required even if you don't watch SABC channels. Enforcement through detector vans and penalties for non-compliance.",
    "Import Duties (Consumer Goods)": "Money to Government: 15-40% customs duty on imported clothing, footwear, electronics, and other goods goes to SARS. Clothing (40%), footwear (30%), general goods (20%). Calculated on your monthly imported goods spending. These duties are IN ADDITION to VAT.",
    "Import VAT (Online Purchases)": "Money to Government: 15% VAT charged on ALL international online purchases (no minimum threshold). Applied to (item cost + shipping + import duty). SARS collects before delivery. Every overseas online order includes this government charge.",
    "Import Duties (Online Purchases)": "Money to Government: Customs duties (averaging 20%) on international online purchases flow to SARS. Combined with 15% Import VAT, government takes ~35-40% of your overseas online shopping total before you receive the item.",
    "Airport Taxes (Domestic)": "Money to Government: ~R125 per domestic flight (R100 airport tax + R25 passenger service charge) goes to government/state entities. Hidden in your ticket price but flows to ACSA (state-owned) and aviation authorities.",
    "Airport Taxes & Tourism Levy (International)": "Money to Government: ~R295 per international departure (R190 airport tax + R75 passenger service charge + R30 tourism levy) goes to government. SARS collects the tourism levy; ACSA (state-owned) gets airport taxes. Built into every international ticket.",
    "Accommodation Tourism Levy": "Money to Government: 1% of ALL accommodation charges (hotels, B&Bs, guesthouses, Airbnb, lodges) flows to provincial tourism boards (government entities). Typical family holiday R10,000 accommodation = R100 to government. Business travelers spending R50,000/year = R500. Collected by accommodation providers and remitted to provincial treasuries.",
    
    # Municipal Services - 100% to government
    "Municipal Water Charges": "Money to Government: 100% of water charges flow to government entities. Your municipality bills you, but sources water from state-owned water boards (Rand Water, Umgeni Water, etc.) regulated by Department of Water and Sanitation. Typical household: R300-R800/month = R3,600-R9,600/year to government coffers.",
    "Municipal Sewerage Charges": "Money to Government: 100% of sewerage/sanitation charges go to your local municipality (government entity). Funds wastewater treatment plants and sewer infrastructure. Typically 70-90% of your water charge. R250-R600/month = R3,000-R7,200/year flowing to government.",
    "Municipal Refuse Removal": "Money to Government: 100% of refuse removal fees go to local municipality. Government-provided waste collection and landfill management service. Fixed monthly charge typically R200-R400 = R2,400-R4,800/year to government.",
    "Other Municipal Charges": "Money to Government: Stormwater drainage fees, water meter rental, sewerage connection fees - all flow 100% to your municipality (government). These 'other' municipal charges add R50-R200/month = R600-R2,400/year to government revenue.",
}


def get_tax_engine() -> TaxEngine:
    """Load tax rates and create engine"""
    rates = TaxRates.load_from_yaml(settings.TAX_RATES_PATH)
    return TaxEngine(rates)


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main calculation form page"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "settings": settings
    })


@router.post("/calc", response_class=HTMLResponse)
async def calculate(
    request: Request,
    # Personal
    annual_salary: float = Form(...),
    annual_bonus: float = Form(0),
    retirement_contrib: float = Form(0),
    age: int = Form(...),
    medical_members: int = Form(0),
    # Consumption - VAT
    std_vat_spend_month: float = Form(0),
    # Fuel
    litres_petrol_month: float = Form(0),
    litres_diesel_month: float = Form(0),
    # Utilities
    electricity_kwh_month: float = Form(0),
    # Alcohol
    beer_litres_month: float = Form(0),
    beer_avg_abv: float = Form(5.0),
    wine_litres_month: float = Form(0),
    wine_avg_abv: float = Form(12.5),
    spirits_litres_month: float = Form(0),
    spirits_avg_abv: float = Form(43.0),
    # Tobacco
    cigarette_packs_20_month: int = Form(0),
    cigarette_avg_price_per_pack: float = Form(45.0),
    # Other levies
    tyres_purchased_per_year: int = Form(0),
    tyre_avg_weight_kg: float = Form(10.0),
    tv_licenses_count: int = Form(0),
    monthly_imported_goods_spend: float = Form(0),
    imported_goods_avg_duty_rate: float = Form(0.20),
    monthly_international_online_spend: float = Form(0),
    # Travel
    domestic_flights_per_year: int = Form(0),
    international_flights_per_year: int = Form(0),
    annual_accommodation_spend: float = Form(0),
    # Transport/Property
    vehicle_licence_fees_annual: float = Form(0),
    tolls_annual: float = Form(0),
    municipal_rates_services_annual: float = Form(0),
    vehicle_monthly_installment: float = Form(0),
    vehicle_is_imported: str = Form("false"),
    # Municipal Services
    municipal_water_monthly: float = Form(0),
    municipal_sewerage_monthly: float = Form(0),
    municipal_refuse_monthly: float = Form(0),
    municipal_other_monthly: float = Form(0),
    # Investment
    sa_dividends_annual: float = Form(0),
    taxable_cgt_base_annual: float = Form(0),
    # Client-side metadata (optional, for analytics)
    screen_width: Optional[int] = Form(None),
    screen_height: Optional[int] = Form(None),
    screen_color_depth: Optional[int] = Form(None),
    pixel_ratio: Optional[float] = Form(None),
    viewport_width: Optional[int] = Form(None),
    viewport_height: Optional[int] = Form(None),
    time_to_complete_seconds: Optional[int] = Form(None),
    cookies_enabled: Optional[str] = Form(None),
    do_not_track: Optional[str] = Form(None),
    online: Optional[str] = Form(None),
    touch_support: Optional[str] = Form(None),
    webgl_support: Optional[str] = Form(None),
    local_storage_support: Optional[str] = Form(None),
    session_id: Optional[str] = Form(None),
    engine: TaxEngine = Depends(get_tax_engine)
):
    """Calculate and return results partial (HTMX target)"""
    
    # Build profiles
    personal = PersonalProfile(
        annual_salary=annual_salary,
        annual_bonus=annual_bonus,
        retirement_contrib=retirement_contrib,
        age=age,
        medical_members=medical_members
    )
    
    consumption = ConsumptionProfile(
        std_vat_spend_month=std_vat_spend_month,
        litres_petrol_month=litres_petrol_month,
        litres_diesel_month=litres_diesel_month,
        electricity_kwh_month=electricity_kwh_month,
        beer_litres_month=beer_litres_month,
        beer_avg_abv=beer_avg_abv,
        wine_litres_month=wine_litres_month,
        wine_avg_abv=wine_avg_abv,
        spirits_litres_month=spirits_litres_month,
        spirits_avg_abv=spirits_avg_abv,
        cigarette_packs_20_month=cigarette_packs_20_month,
        cigarette_avg_price_per_pack=cigarette_avg_price_per_pack,
        tyres_purchased_per_year=tyres_purchased_per_year,
        tyre_avg_weight_kg=tyre_avg_weight_kg,
        tv_licenses_count=tv_licenses_count,
        monthly_imported_goods_spend=monthly_imported_goods_spend,
        imported_goods_avg_duty_rate=imported_goods_avg_duty_rate,
        monthly_international_online_spend=monthly_international_online_spend,
    )
    
    transport_property = TransportAndPropertyProfile(
        vehicle_licence_fees_annual=vehicle_licence_fees_annual,
        tolls_annual=tolls_annual,
        municipal_rates_services_annual=municipal_rates_services_annual,
        vehicle_monthly_installment=vehicle_monthly_installment,
        vehicle_is_imported=(vehicle_is_imported == "true"),
        municipal_water_monthly=municipal_water_monthly,
        municipal_sewerage_monthly=municipal_sewerage_monthly,
        municipal_refuse_monthly=municipal_refuse_monthly,
        municipal_other_monthly=municipal_other_monthly,
    )
    
    investment = InvestmentProfile(
        sa_dividends_annual=sa_dividends_annual,
        taxable_cgt_base_annual=taxable_cgt_base_annual
    )
    
    travel = TravelProfile(
        domestic_flights_per_year=domestic_flights_per_year,
        international_flights_per_year=international_flights_per_year,
        annual_accommodation_spend=annual_accommodation_spend,
    )
    
    # Calculate
    breakdown, total = engine.run(personal, consumption, transport_property, investment, travel)
    
    # Calculate effective rate
    gross_income = personal.annual_salary + personal.annual_bonus
    effective_rate = (total / gross_income * 100.0) if gross_income > 0 else 0.0
    
    # Sort breakdown by amount (descending)
    sorted_breakdown = sorted(breakdown.items(), key=lambda x: x[1], reverse=True)
    
    # Log submission to Supabase (async, non-blocking)
    try:
        # Prepare form data (all inputs)
        form_data = {
            'annual_salary': annual_salary,
            'annual_bonus': annual_bonus,
            'age': age,
            'medical_members': medical_members,
            'std_vat_spend_month': std_vat_spend_month,
            'litres_petrol_month': litres_petrol_month,
            'litres_diesel_month': litres_diesel_month,
            'electricity_kwh_month': electricity_kwh_month,
            'beer_litres_month': beer_litres_month,
            'wine_litres_month': wine_litres_month,
            'spirits_litres_month': spirits_litres_month,
            'cigarette_packs_20_month': cigarette_packs_20_month,
            'tv_licenses_count': tv_licenses_count,
            'tyres_purchased_per_year': tyres_purchased_per_year,
            'monthly_imported_goods_spend': monthly_imported_goods_spend,
            'monthly_international_online_spend': monthly_international_online_spend,
            'domestic_flights_per_year': domestic_flights_per_year,
            'international_flights_per_year': international_flights_per_year,
            'annual_accommodation_spend': annual_accommodation_spend,
            'vehicle_licence_fees_annual': vehicle_licence_fees_annual,
            'tolls_annual': tolls_annual,
            'municipal_rates_services_annual': municipal_rates_services_annual,
            'vehicle_monthly_installment': vehicle_monthly_installment,
            'vehicle_is_imported': vehicle_is_imported == "true",
            'municipal_water_monthly': municipal_water_monthly,
            'municipal_sewerage_monthly': municipal_sewerage_monthly,
            'municipal_refuse_monthly': municipal_refuse_monthly,
            'municipal_other_monthly': municipal_other_monthly,
            'sa_dividends_annual': sa_dividends_annual,
            'taxable_cgt_base_annual': taxable_cgt_base_annual,
        }
        
        # Prepare results summary
        results_summary = {
            'total_annual': total,
            'monthly_total': total / 12,
            'percentage': effective_rate,
            'gross_income': gross_income,
            'breakdown': dict(sorted_breakdown),
        }
        
        # Collect request metadata
        request_data = {
            # Server-side data
            'ip_address': request.headers.get('x-forwarded-for', '').split(',')[0].strip() or (request.client.host if request.client else ''),
            'user_agent': request.headers.get('user-agent', ''),
            'referrer': request.headers.get('referer', ''),
            'languages': request.headers.get('accept-language', ''),
            'language': request.headers.get('accept-language', '').split(',')[0].strip() if request.headers.get('accept-language') else '',
            
            # Client-side data (from form parameters)
            'screen_width': screen_width,
            'screen_height': screen_height,
            'screen_color_depth': screen_color_depth,
            'pixel_ratio': pixel_ratio,
            'viewport_width': viewport_width,
            'viewport_height': viewport_height,
            'time_to_complete_seconds': time_to_complete_seconds,
            'cookies_enabled': cookies_enabled == 'true' if cookies_enabled else None,
            'do_not_track': do_not_track == 'true' if do_not_track else None,
            'online': online == 'true' if online else None,
            'touch_support': touch_support == 'true' if touch_support else None,
            'webgl_support': webgl_support == 'true' if webgl_support else None,
            'local_storage_support': local_storage_support == 'true' if local_storage_support else None,
            'session_id': session_id,
        }
        
        # Log to Supabase (async)
        import asyncio
        asyncio.create_task(
            submission_logger.log_submission(
                form_data=form_data,
                results=results_summary,
                request_data=request_data
            )
        )
    except Exception as e:
        # Never fail the main request due to logging errors
        print(f"Logging error (non-critical): {e}")
    
    return templates.TemplateResponse(
        "_breakdown_table.html",
        {
            "request": request,
            "breakdown": sorted_breakdown,
            "total": total,
            "monthly_total": total / 12,
            "effective_rate": effective_rate,
            "gross_income": gross_income,
            "tax_explanations": TAX_EXPLANATIONS,
            "settings": settings
        }
    )


@router.get("/results", response_class=HTMLResponse)
async def results_page(request: Request):
    """Full results page with charts"""
    # This would typically load from a saved scenario
    # For now, just show the template
    return templates.TemplateResponse("results.html", {"request": request})
