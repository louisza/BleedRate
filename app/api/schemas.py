"""Pydantic models for API requests and responses"""
from pydantic import BaseModel, Field
from typing import Optional


class Personal(BaseModel):
    """Personal income and demographics"""
    annual_salary: float = Field(ge=0, description="Annual salary in Rands")
    annual_bonus: float = Field(default=0, ge=0)
    retirement_contrib: float = Field(default=0, ge=0)
    age: int = Field(ge=0, le=120)
    medical_members: int = Field(default=0, ge=0)


class Consumption(BaseModel):
    """Monthly consumption patterns"""
    # General spending
    std_vat_spend_month: float = Field(default=0, ge=0)
    zero_vat_spend_month: float = Field(default=0, ge=0)
    
    # Fuel consumption
    litres_petrol_month: float = Field(default=0, ge=0)
    litres_diesel_month: float = Field(default=0, ge=0)
    
    # Utilities
    electricity_kwh_month: float = Field(default=0, ge=0)
    
    # Sugary drinks (Health Promotion Levy)
    sugary_drink_litres_month: float = Field(default=0, ge=0)
    sugary_avg_g_per_100ml: float = Field(default=10.0, ge=0)
    
    # Alcohol (detailed by type)
    beer_litres_month: float = Field(default=0, ge=0)
    beer_avg_abv: float = Field(default=5.0, ge=0, le=100, description="% alcohol by volume")
    wine_litres_month: float = Field(default=0, ge=0)
    wine_avg_abv: float = Field(default=12.5, ge=0, le=100)
    spirits_litres_month: float = Field(default=0, ge=0)
    spirits_avg_abv: float = Field(default=43.0, ge=0, le=100)
    
    # Tobacco (detailed by type)
    cigarette_packs_20_month: int = Field(default=0, ge=0, description="Number of 20-packs per month")
    cigarette_avg_price_per_pack: float = Field(default=45.0, ge=0, description="For ad valorem calculation")
    cigars_grams_month: float = Field(default=0, ge=0)
    pipe_tobacco_grams_month: float = Field(default=0, ge=0)
    
    # Other levies
    plastic_bags_per_month: int = Field(default=0, ge=0)


class TransportProperty(BaseModel):
    """Transport and property costs"""
    vehicle_licence_fees_annual: float = Field(default=0, ge=0)
    tolls_annual: float = Field(default=0, ge=0)
    municipal_rates_services_annual: float = Field(default=0, ge=0)
    buying_property_price: Optional[float] = Field(default=None, ge=0, description="Optional: for transfer duty")


class Investment(BaseModel):
    """Investment income and gains"""
    sa_dividends_annual: float = Field(default=0, ge=0)
    taxable_cgt_base_annual: float = Field(default=0, ge=0, description="The taxable gain (already calculated)")


class CalcRequest(BaseModel):
    """Complete calculation request"""
    personal: Personal
    consumption: Consumption
    transport_property: TransportProperty
    investment: Investment


class CalcResponse(BaseModel):
    """Calculation response"""
    breakdown: dict[str, float]
    total: float
    effective_rate_vs_gross: float
    monthly_total: float


class RatesResponse(BaseModel):
    """Tax rates response"""
    rates: dict
    version: str = "2024/25"


class ScenarioSaveRequest(BaseModel):
    """Request to save a scenario"""
    label: Optional[str] = Field(default=None, max_length=200)
    calc_request: CalcRequest
    calc_response: CalcResponse


class ScenarioResponse(BaseModel):
    """Saved scenario response"""
    id: str
    label: Optional[str]
    created_at: str
    inputs: dict
    outputs: dict
