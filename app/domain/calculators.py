"""Tax calculation engines for different tax categories"""
from app.domain.rates import TaxRates
from app.domain.profiles import (
    PersonalProfile,
    ConsumptionProfile,
    TransportAndPropertyProfile,
    InvestmentProfile,
    TravelProfile,
)


class PAYECalculator:
    """Calculate PAYE, UIF, and medical tax credits"""
    
    def __init__(self, rates: TaxRates):
        self.rates = rates
    
    def calculate(self, profile: PersonalProfile) -> dict[str, float]:
        """Calculate direct income taxes"""
        annual_salary = profile.annual_salary + profile.annual_bonus
        
        # Calculate gross PAYE before rebates
        gross_paye = self._calculate_paye_from_brackets(annual_salary)
        
        # Apply rebates based on age
        rebates = self.rates.primary_rebate
        if profile.age >= 65:
            rebates += self.rates.secondary_rebate
        if profile.age >= 75:
            rebates += self.rates.tertiary_rebate
        
        paye_after_rebates = max(0, gross_paye - rebates)
        
        # Calculate UIF (capped monthly)
        monthly_salary = annual_salary / 12
        monthly_uif = min(
            monthly_salary * self.rates.uif_employee_rate,
            self.rates.uif_monthly_cap
        )
        annual_uif = monthly_uif * 12
        
        # Calculate medical tax credit
        if profile.medical_members > 0:
            first_two_credits = min(profile.medical_members, 2) * self.rates.med_credit_first_two
            additional_credits = max(0, profile.medical_members - 2) * self.rates.med_credit_additional
            annual_med_credit = (first_two_credits + additional_credits) * 12
        else:
            annual_med_credit = 0
        
        # Net PAYE after medical credits
        net_paye = max(0, paye_after_rebates - annual_med_credit)
        
        return {
            "PAYE (Income Tax)": net_paye,
            "UIF": annual_uif,
        }
    
    def _calculate_paye_from_brackets(self, income: float) -> float:
        """Calculate PAYE using tax brackets"""
        for bracket in self.rates.paye_brackets:
            if bracket.up_to is None or income <= bracket.up_to:
                return bracket.base_tax + (income - bracket.lower) * bracket.rate
        return 0.0


class IndirectTaxesCalculator:
    """Calculate VAT, fuel levies, environmental levies, and sin tax levies"""
    
    def __init__(self, rates: TaxRates):
        self.rates = rates
    
    def calculate(self, profile: ConsumptionProfile) -> dict[str, float]:
        """Calculate indirect taxes"""
        result = {}
        
        # VAT
        monthly_vat = profile.std_vat_spend_month * self.rates.vat_rate
        result["VAT"] = monthly_vat * 12
        
        # Fuel levies
        petrol_total = profile.litres_petrol_month * (
            self.rates.fuel_gfl_petrol + 
            self.rates.fuel_raf + 
            self.rates.fuel_carbon_petrol
        )
        diesel_total = profile.litres_diesel_month * (
            self.rates.fuel_gfl_diesel + 
            self.rates.fuel_raf + 
            self.rates.fuel_carbon_diesel
        )
        result["Fuel Levies"] = (petrol_total + diesel_total) * 12
        
        # Electricity environmental levy
        electricity_levy = profile.electricity_kwh_month * self.rates.electricity_env_levy
        result["Electricity Environmental Levy"] = electricity_levy * 12
        
        # Health Promotion Levy (sugary drinks)
        if profile.sugary_drink_litres_month > 0:
            # Calculate grams of sugar above threshold per 100ml
            sugar_above_threshold = max(
                0,
                profile.sugary_avg_g_per_100ml - self.rates.hpl_threshold_g_per_100ml
            )
            # Convert litres to 100ml units and calculate levy
            units_of_100ml = profile.sugary_drink_litres_month * 10
            monthly_hpl = units_of_100ml * sugar_above_threshold * self.rates.hpl_per_gram_over_threshold
            result["Health Promotion Levy (Sugar Tax)"] = monthly_hpl * 12
        
        # Plastic bag levy
        if profile.plastic_bags_per_month > 0:
            result["Plastic Bag Levy"] = profile.plastic_bags_per_month * self.rates.plastic_bag_levy * 12
        
        return result


class AlcoholTaxCalculator:
    """Calculate alcohol excise duties"""
    
    def __init__(self, rates: TaxRates):
        self.rates = rates
    
    def calculate(self, profile: ConsumptionProfile) -> dict[str, float]:
        """Calculate alcohol excise taxes
        
        Official SARS rates (National Treasury 2024):
        - Beer/Fermented: R121.41 per LITRE OF ABSOLUTE ALCOHOL (LAA)
        - Wine: R4.96 per LITRE OF WINE (volumetric, NOT LAA-based)
        - Spirits: R249.20 per LITRE OF ABSOLUTE ALCOHOL (LAA)
        
        LAA Calculation: litres × (ABV% / 100) × rate per LAA
        Example: 20L beer at 5% ABV = 20 × 0.05 × R121.41 = R121.41/month
        """
        result = {}
        
        # Beer excise - LAA-based calculation
        if profile.beer_litres_month > 0:
            laa_beer = profile.beer_litres_month * (profile.beer_avg_abv / 100.0)
            monthly_beer_excise = laa_beer * self.rates.beer_excise_per_laa
            result["Beer Excise"] = monthly_beer_excise * 12
        
        # Wine excise - volumetric rate (NOT LAA-based)
        if profile.wine_litres_month > 0:
            monthly_wine_excise = profile.wine_litres_month * self.rates.wine_excise_per_litre
            result["Wine Excise"] = monthly_wine_excise * 12
        
        # Spirits excise - LAA-based calculation
        if profile.spirits_litres_month > 0:
            laa_spirits = profile.spirits_litres_month * (profile.spirits_avg_abv / 100.0)
            monthly_spirits_excise = laa_spirits * self.rates.spirits_excise_per_laa
            result["Spirits Excise"] = monthly_spirits_excise * 12
        
        return result


class TobaccoTaxCalculator:
    """Calculate tobacco excise duties"""
    
    def __init__(self, rates: TaxRates):
        self.rates = rates
    
    def calculate(self, profile: ConsumptionProfile) -> dict[str, float]:
        """Calculate tobacco excise taxes
        
        For cigarettes: Apply BOTH specific and ad valorem, take the maximum
        For cigars and pipe tobacco: Simple per-gram calculation
        """
        result = {}
        
        # Cigarette excise (specific + ad valorem, max applies)
        if profile.cigarette_packs_20_month > 0:
            # Specific excise
            specific_excise = profile.cigarette_packs_20_month * self.rates.cigarette_excise_per_20
            
            # Ad valorem excise (% of retail price)
            ad_valorem_excise = (
                profile.cigarette_packs_20_month * 
                profile.cigarette_avg_price_per_pack * 
                self.rates.cigarette_ad_valorem_rate
            )
            
            # Take maximum as per SARS rules
            monthly_cigarette_excise = max(specific_excise, ad_valorem_excise)
            result["Cigarette Excise"] = monthly_cigarette_excise * 12
        
        # Cigar excise
        if profile.cigars_grams_month > 0:
            monthly_cigar_excise = profile.cigars_grams_month * self.rates.cigar_excise_per_gram
            result["Cigar Excise"] = monthly_cigar_excise * 12
        
        # Pipe tobacco excise
        if profile.pipe_tobacco_grams_month > 0:
            monthly_pipe_excise = profile.pipe_tobacco_grams_month * self.rates.pipe_tobacco_excise_per_gram
            result["Pipe Tobacco Excise"] = monthly_pipe_excise * 12
        
        return result


class PropertyTransportCalculator:
    """Calculate property and transport taxes"""
    
    def __init__(self, rates: TaxRates):
        self.rates = rates
    
    def calculate(self, profile: TransportAndPropertyProfile) -> dict[str, float]:
        """Calculate property and transport taxes"""
        result = {}
        
        # Vehicle license fees
        if profile.vehicle_licence_fees_annual > 0:
            result["Vehicle License Fees"] = profile.vehicle_licence_fees_annual
        
        # Toll fees
        if profile.tolls_annual > 0:
            result["Toll Fees"] = profile.tolls_annual
        
        # Municipal rates and services
        if profile.municipal_rates_services_annual > 0:
            result["Municipal Rates & Services"] = profile.municipal_rates_services_annual
        
        # Transfer duty (one-time purchase)
        if profile.buying_property_price:
            transfer_duty = self._calculate_transfer_duty(profile.buying_property_price)
            if transfer_duty > 0:
                result["Transfer Duty (One-time)"] = transfer_duty
        
        # Vehicle import duty (embedded in financing if imported)
        if profile.vehicle_monthly_installment > 0 and profile.vehicle_is_imported:
            # 25% import duty is embedded in the purchase price
            # Calculate the portion attributable to import duty
            annual_installments = profile.vehicle_monthly_installment * 12
            # Import duty is 25% of base price, so it's 20% of inflated price (25/125)
            import_duty_portion = annual_installments * (25 / 125)
            result["Vehicle Import Duty (in installments)"] = import_duty_portion
        
        return result
    
    def _calculate_transfer_duty(self, property_price: float) -> float:
        """Calculate transfer duty using bands"""
        for band in self.rates.transfer_duty:
            if band.up_to is None or property_price <= band.up_to:
                return band.base + (property_price - band.excess_over) * band.rate
        return 0.0


class InvestmentTaxesCalculator:
    """Calculate investment-related taxes"""
    
    def __init__(self, rates: TaxRates):
        self.rates = rates
    
    def calculate(self, profile: InvestmentProfile) -> dict[str, float]:
        """Calculate investment taxes"""
        result = {}
        
        # Dividends tax
        if profile.sa_dividends_annual > 0:
            dividends_tax = profile.sa_dividends_annual * self.rates.dividends_tax_rate
            result["Dividends Tax"] = dividends_tax
        
        # Capital Gains Tax
        if profile.taxable_cgt_base_annual > 0:
            cgt = profile.taxable_cgt_base_annual * self.rates.cgt_effective_max_rate
            result["Capital Gains Tax"] = cgt
        
        return result


class EmbeddedCorporateTaxCalculator:
    """Estimate corporate taxes embedded in consumer prices
    
    This calculator estimates the portion of consumer spending that represents
    corporate taxes passed through to consumers via higher prices. These include:
    - Corporate Income Tax (27% of profits)
    - Skills Development Levy (1% of payroll)
    - UIF Employer Contribution (1% of payroll)
    - VAT/PAYE administration and compliance costs
    - Regulatory compliance costs (BBBEE, labour law, environmental, etc.)
    - Supply chain cascade effects (taxes paid by suppliers)
    
    Economic research suggests 50-70% of corporate tax burden is ultimately
    borne by consumers through higher prices and employees through lower wages.
    This calculator focuses on the consumer price component.
    
    References:
    - Harberger (1962): Corporate tax incidence theory
    - OECD (2018): Tax incidence studies
    - IMF research on developing economies
    """
    
    def __init__(self, rates: TaxRates):
        self.rates = rates
        
        # Conservative embedded tax rate estimates by industry
        # These represent the portion of price attributable to corporate taxes
        self.embedded_rates = {
            "labour_intensive": 0.17,  # Restaurants, hospitality (high SDL/UIF impact)
            "manufacturing": 0.13,      # Consumer goods (supply chain cascade)
            "retail": 0.10,             # Standard retail (thin margins)
            "services": 0.15,           # Professional services (high compliance)
            "technology": 0.08,         # Software, online (lower physical chain)
            "weighted_average": 0.12,   # Conservative economy-wide average
        }
        
        # Component breakdown of embedded taxes (proportions)
        self.component_weights = {
            "corporate_income_tax": 0.40,    # 40% of embedded is CIT
            "sdl_uif_employer": 0.15,        # 15% is SDL/UIF employer portion
            "vat_paye_admin": 0.10,          # 10% is tax admin costs
            "regulatory_compliance": 0.20,    # 20% is regulatory costs
            "supply_chain_cascade": 0.15,     # 15% is upstream taxes
        }
    
    def calculate(self, profile: ConsumptionProfile) -> dict[str, float]:
        """Calculate estimated embedded corporate taxes in annual spending
        
        Uses conservative weighted average rate across all spending.
        """
        result = {}
        
        # Total annual spending subject to embedded corporate taxes
        # We use VAT-bearing spending as proxy for total consumption
        annual_vat_spend = profile.std_vat_spend_month * 12
        
        if annual_vat_spend <= 0:
            return result
        
        # Apply conservative weighted average embedded rate
        embedded_rate = self.embedded_rates["weighted_average"]
        total_embedded = annual_vat_spend * embedded_rate
        
        # Break down by component for transparency
        result["Corporate Income Tax (embedded)"] = total_embedded * self.component_weights["corporate_income_tax"]
        result["SDL/UIF Employer Contribution (embedded)"] = total_embedded * self.component_weights["sdl_uif_employer"]
        result["Tax Administration Costs (embedded)"] = total_embedded * self.component_weights["vat_paye_admin"]
        result["Regulatory Compliance Costs (embedded)"] = total_embedded * self.component_weights["regulatory_compliance"]
        result["Supply Chain Tax Cascade (embedded)"] = total_embedded * self.component_weights["supply_chain_cascade"]
        
        return result
    
    def get_total_embedded(self, profile: ConsumptionProfile) -> float:
        """Get total embedded corporate taxes as single figure"""
        annual_vat_spend = profile.std_vat_spend_month * 12
        return annual_vat_spend * self.embedded_rates["weighted_average"]
    
    def calculate_by_industry(self, spending_by_category: dict[str, float]) -> dict[str, float]:
        """More granular calculation by spending category
        
        Args:
            spending_by_category: Dict mapping category names to annual spending
                e.g. {"groceries": 50000, "restaurants": 30000, ...}
        
        Returns:
            Dict of embedded taxes by category
        """
        result = {}
        
        # Map spending categories to industry types
        category_to_industry = {
            "groceries": "retail",
            "restaurants": "labour_intensive",
            "clothing": "manufacturing",
            "electronics": "manufacturing",
            "online_shopping": "technology",
            "professional_services": "services",
            "entertainment": "labour_intensive",
            "general": "weighted_average",
        }
        
        for category, annual_spend in spending_by_category.items():
            if annual_spend <= 0:
                continue
            
            # Determine industry type for this category
            industry = category_to_industry.get(category, "weighted_average")
            rate = self.embedded_rates[industry]
            
            embedded_tax = annual_spend * rate
            result[f"Embedded Tax: {category.title()}"] = embedded_tax
        
        return result


class OtherLeviesCalculator:
    """Calculate tyre levy, import duties, airport taxes, etc."""
    
    def __init__(self, rates: TaxRates):
        self.rates = rates
    
    def calculate(self, consumption: ConsumptionProfile, travel: 'TravelProfile') -> dict[str, float]:
        """Calculate additional government money flows"""
        result = {}
        
        # Tyre Levy
        if consumption.tyres_purchased_per_year > 0:
            annual_tyre_levy = (
                consumption.tyres_purchased_per_year *
                consumption.tyre_avg_weight_kg *
                self.rates.tyre_levy_per_kg
            )
            result["Tyre Levy"] = annual_tyre_levy
        
        # TV License (multiple licenses possible)
        if consumption.tv_licenses_count > 0:
            result["TV License"] = consumption.tv_licenses_count * self.rates.tv_license_annual
        
        # Import Duties on Consumer Goods (non-vehicle)
        if consumption.monthly_imported_goods_spend > 0:
            annual_import_duty = (
                consumption.monthly_imported_goods_spend * 12 *
                consumption.imported_goods_avg_duty_rate
            )
            result["Import Duties (Consumer Goods)"] = annual_import_duty
        
        # Import VAT on international online purchases
        if consumption.monthly_international_online_spend > 0:
            # Import VAT is charged on (Cost + Shipping + Duty)
            # Simplified: assume 15% VAT on the purchase amount
            # Plus duties at weighted average rate
            annual_online_spend = consumption.monthly_international_online_spend * 12
            
            # Duty component
            import_duty_online = annual_online_spend * self.rates.import_duty_weighted_avg
            # VAT on (goods + duty)
            import_vat_online = (annual_online_spend + import_duty_online) * self.rates.import_vat_rate
            
            result["Import VAT (Online Purchases)"] = import_vat_online
            if import_duty_online > 0:
                result["Import Duties (Online Purchases)"] = import_duty_online
        
        # Domestic Flight Taxes
        if travel.domestic_flights_per_year > 0:
            domestic_airport_tax = (
                travel.domestic_flights_per_year *
                (self.rates.airport_tax_domestic + self.rates.passenger_service_charge_domestic)
            )
            result["Airport Taxes (Domestic)"] = domestic_airport_tax
        
        # International Flight Taxes
        if travel.international_flights_per_year > 0:
            international_airport_tax = (
                travel.international_flights_per_year *
                (self.rates.airport_tax_international + 
                 self.rates.passenger_service_charge_international +
                 self.rates.tourism_levy_international)
            )
            result["Airport Taxes & Tourism Levy (International)"] = international_airport_tax
        
        # Accommodation Tourism Levy (provincial)
        if travel.annual_accommodation_spend > 0:
            accommodation_levy = travel.annual_accommodation_spend * self.rates.accommodation_tourism_levy_rate
            result["Accommodation Tourism Levy"] = accommodation_levy
        
        return result


class MunicipalServicesCalculator:
    """
    Calculator for municipal water, sewerage, and refuse charges.
    
    These charges flow 100% to government entities:
    - Local municipalities (billing and primary service)
    - Water boards (bulk water supply - state entities)
    - Department of Water and Sanitation (regulation and infrastructure)
    """
    
    def __init__(self, rates: TaxRates):
        self.rates = rates
    
    def calculate(self, profile: TransportAndPropertyProfile) -> dict[str, float]:
        """Calculate annual municipal service charges that flow to government."""
        result = {}
        
        if profile.municipal_water_monthly > 0:
            result["Municipal Water Charges"] = profile.municipal_water_monthly * 12
        
        if profile.municipal_sewerage_monthly > 0:
            result["Municipal Sewerage Charges"] = profile.municipal_sewerage_monthly * 12
        
        if profile.municipal_refuse_monthly > 0:
            result["Municipal Refuse Removal"] = profile.municipal_refuse_monthly * 12
        
        if profile.municipal_other_monthly > 0:
            result["Other Municipal Charges"] = profile.municipal_other_monthly * 12
        
        return result
