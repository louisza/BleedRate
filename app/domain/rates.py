"""Tax rates data models and YAML loader"""
from dataclasses import dataclass
from typing import List, Optional
import yaml
from pathlib import Path


@dataclass
class PAYEBracket:
    """PAYE income tax bracket"""
    lower: float
    up_to: Optional[float]
    rate: float
    base_tax: float


@dataclass
class TransferDutyBand:
    """Transfer duty bracket"""
    up_to: Optional[float]
    base: float
    rate: float
    excess_over: float


@dataclass
class TaxRates:
    """Complete tax rates configuration"""
    # PAYE
    paye_brackets: List[PAYEBracket]
    primary_rebate: float
    secondary_rebate: float
    tertiary_rebate: float
    
    # Medical credits
    med_credit_first_two: float
    med_credit_additional: float
    
    # UIF
    uif_employee_rate: float
    uif_monthly_cap: float
    
    # VAT
    vat_rate: float
    
    # Fuel levies
    fuel_gfl_petrol: float
    fuel_gfl_diesel: float
    fuel_raf: float
    fuel_carbon_petrol: float
    fuel_carbon_diesel: float
    
    # Environmental
    electricity_env_levy: float
    
    # Health Promotion Levy (sugary drinks)
    hpl_per_gram_over_threshold: float
    hpl_threshold_g_per_100ml: float
    
    # Alcohol excise
    beer_excise_per_laa: float
    beer_typical_abv: float
    wine_excise_per_litre: float
    fortified_wine_excise_per_litre: float
    spirits_excise_per_laa: float
    spirits_typical_abv: float
    laa_to_ml_ratio: float
    
    # Tobacco excise
    cigarette_excise_per_20: float
    cigarette_ad_valorem_rate: float
    cigar_excise_per_gram: float
    pipe_tobacco_excise_per_gram: float
    
    # Other levies
    plastic_bag_levy: float
    tyre_levy_per_kg: float
    tv_license_annual: float
    
    # Import duties
    import_duty_clothing: float
    import_duty_footwear: float
    import_duty_electronics_low: float
    import_duty_electronics_high: float
    import_duty_general: float
    import_duty_weighted_avg: float
    
    # Airport taxes
    airport_tax_domestic: float
    passenger_service_charge_domestic: float
    airport_tax_international: float
    passenger_service_charge_international: float
    tourism_levy_international: float
    
    # Tourism levies
    accommodation_tourism_levy_rate: float
    
    # Import VAT
    import_vat_rate: float
    import_vat_threshold: float
    
    # Municipal services
    municipal_water_typical_per_kl: float
    municipal_sewerage_as_percent_of_water: float
    municipal_refuse_typical_monthly: float
    
    # Investment taxes
    dividends_tax_rate: float
    cgt_effective_max_rate: float
    
    # Transfer duty
    transfer_duty: List[TransferDutyBand]
    
    @classmethod
    def load_from_yaml(cls, file_path: str | Path) -> "TaxRates":
        """Load tax rates from YAML file"""
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Parse PAYE brackets
        paye_brackets = [
            PAYEBracket(**bracket) for bracket in data['paye_brackets']
        ]
        
        # Parse transfer duty bands
        transfer_duty = [
            TransferDutyBand(**band) for band in data['transfer_duty']
        ]
        
        return cls(
            paye_brackets=paye_brackets,
            primary_rebate=data['primary_rebate'],
            secondary_rebate=data['secondary_rebate'],
            tertiary_rebate=data['tertiary_rebate'],
            med_credit_first_two=data['med_credit_first_two'],
            med_credit_additional=data['med_credit_additional'],
            uif_employee_rate=data['uif_employee_rate'],
            uif_monthly_cap=data['uif_monthly_cap'],
            vat_rate=data['vat_rate'],
            fuel_gfl_petrol=data['fuel_gfl_petrol'],
            fuel_gfl_diesel=data['fuel_gfl_diesel'],
            fuel_raf=data['fuel_raf'],
            fuel_carbon_petrol=data['fuel_carbon_petrol'],
            fuel_carbon_diesel=data['fuel_carbon_diesel'],
            electricity_env_levy=data['electricity_env_levy'],
            hpl_per_gram_over_threshold=data['hpl_per_gram_over_threshold'],
            hpl_threshold_g_per_100ml=data['hpl_threshold_g_per_100ml'],
            beer_excise_per_laa=data['beer_excise_per_laa'],
            beer_typical_abv=data['beer_typical_abv'],
            wine_excise_per_litre=data['wine_excise_per_litre'],
            fortified_wine_excise_per_litre=data['fortified_wine_excise_per_litre'],
            spirits_excise_per_laa=data['spirits_excise_per_laa'],
            spirits_typical_abv=data['spirits_typical_abv'],
            laa_to_ml_ratio=data['laa_to_ml_ratio'],
            cigarette_excise_per_20=data['cigarette_excise_per_20'],
            cigarette_ad_valorem_rate=data['cigarette_ad_valorem_rate'],
            cigar_excise_per_gram=data['cigar_excise_per_gram'],
            pipe_tobacco_excise_per_gram=data['pipe_tobacco_excise_per_gram'],
            plastic_bag_levy=data['plastic_bag_levy'],
            tyre_levy_per_kg=data['tyre_levy_per_kg'],
            tv_license_annual=data['tv_license_annual'],
            import_duty_clothing=data['import_duty_clothing'],
            import_duty_footwear=data['import_duty_footwear'],
            import_duty_electronics_low=data['import_duty_electronics_low'],
            import_duty_electronics_high=data['import_duty_electronics_high'],
            import_duty_general=data['import_duty_general'],
            import_duty_weighted_avg=data['import_duty_weighted_avg'],
            airport_tax_domestic=data['airport_tax_domestic'],
            passenger_service_charge_domestic=data['passenger_service_charge_domestic'],
            airport_tax_international=data['airport_tax_international'],
            passenger_service_charge_international=data['passenger_service_charge_international'],
            tourism_levy_international=data['tourism_levy_international'],
            accommodation_tourism_levy_rate=data['accommodation_tourism_levy_rate'],
            import_vat_rate=data['import_vat_rate'],
            import_vat_threshold=data['import_vat_threshold'],
            municipal_water_typical_per_kl=data['municipal_water_typical_per_kl'],
            municipal_sewerage_as_percent_of_water=data['municipal_sewerage_as_percent_of_water'],
            municipal_refuse_typical_monthly=data['municipal_refuse_typical_monthly'],
            dividends_tax_rate=data['dividends_tax_rate'],
            cgt_effective_max_rate=data['cgt_effective_max_rate'],
            transfer_duty=transfer_duty,
        )
