"""User profile data models"""
from dataclasses import dataclass


@dataclass
class PersonalProfile:
    """Personal income and demographics"""
    annual_salary: float
    annual_bonus: float = 0.0
    retirement_contrib: float = 0.0
    age: int = 35
    medical_members: int = 0


@dataclass
class ConsumptionProfile:
    """Monthly consumption patterns"""
    # General spending
    std_vat_spend_month: float = 0.0
    zero_vat_spend_month: float = 0.0
    
    # Fuel consumption
    litres_petrol_month: float = 0.0
    litres_diesel_month: float = 0.0
    
    # Utilities
    electricity_kwh_month: float = 0.0
    
    # Sugary drinks (Health Promotion Levy)
    sugary_drink_litres_month: float = 0.0
    sugary_avg_g_per_100ml: float = 10.0
    
    # Alcohol (detailed by type)
    beer_litres_month: float = 0.0
    beer_avg_abv: float = 5.0           # % alcohol by volume
    wine_litres_month: float = 0.0
    wine_avg_abv: float = 12.5
    spirits_litres_month: float = 0.0
    spirits_avg_abv: float = 43.0
    
    # Tobacco (detailed by type)
    cigarette_packs_20_month: int = 0   # Number of 20-packs per month
    cigarette_avg_price_per_pack: float = 45.0  # For ad valorem calculation
    cigars_grams_month: float = 0.0
    pipe_tobacco_grams_month: float = 0.0
    
    # Other levies
    plastic_bags_per_month: int = 0
    tyres_purchased_per_year: int = 0  # Number of tyres replaced annually
    tyre_avg_weight_kg: float = 10.0   # Average weight per tyre (passenger car ~10kg)
    tv_licenses_count: int = 0  # Number of TV licenses paid for
    
    # Import duties on consumer goods
    monthly_imported_goods_spend: float = 0.0  # Total spent on imported consumer goods
    imported_goods_avg_duty_rate: float = 0.20  # Weighted average duty rate (20% default)
    
    # Online international purchases (subject to import VAT + duties)
    monthly_international_online_spend: float = 0.0  # Purchases from overseas websites


@dataclass
class TravelProfile:
    """Travel and aviation-related taxes"""
    domestic_flights_per_year: int = 0
    international_flights_per_year: int = 0
    annual_accommodation_spend: float = 0.0  # Hotels, B&Bs, guesthouses, Airbnb (1% tourism levy)


@dataclass
class TransportAndPropertyProfile:
    """Transport and property costs"""
    vehicle_licence_fees_annual: float = 0.0
    tolls_annual: float = 0.0
    municipal_rates_services_annual: float = 0.0
    buying_property_price: float | None = None  # Optional: for transfer duty
    
    # Vehicle financing (import duty consideration)
    vehicle_monthly_installment: float = 0.0
    vehicle_is_imported: bool = False  # True if NOT assembled in South Africa
    
    # Municipal service charges (100% to government)
    municipal_water_monthly: float = 0.0       # Water consumption charges
    municipal_sewerage_monthly: float = 0.0    # Sewerage/sanitation charges
    municipal_refuse_monthly: float = 0.0      # Refuse removal charges
    municipal_other_monthly: float = 0.0       # Stormwater, meter rental, other


@dataclass
class InvestmentProfile:
    """Investment income and gains"""
    sa_dividends_annual: float = 0.0
    taxable_cgt_base_annual: float = 0.0  # The taxable gain (already calculated)
