"""Tax calculation engine - orchestrates all calculators"""
from app.domain.rates import TaxRates
from app.domain.profiles import (
    PersonalProfile,
    ConsumptionProfile,
    TransportAndPropertyProfile,
    InvestmentProfile,
    TravelProfile,
)
from app.domain.calculators import (
    PAYECalculator,
    IndirectTaxesCalculator,
    AlcoholTaxCalculator,
    TobaccoTaxCalculator,
    PropertyTransportCalculator,
    InvestmentTaxesCalculator,
    EmbeddedCorporateTaxCalculator,
    OtherLeviesCalculator,
    MunicipalServicesCalculator,
)


class TaxEngine:
    """Orchestrates all tax calculations"""
    
    def __init__(self, rates: TaxRates):
        self.rates = rates
        self.paye_calc = PAYECalculator(rates)
        self.indirect_calc = IndirectTaxesCalculator(rates)
        self.alcohol_calc = AlcoholTaxCalculator(rates)
        self.tobacco_calc = TobaccoTaxCalculator(rates)
        self.property_calc = PropertyTransportCalculator(rates)
        self.investment_calc = InvestmentTaxesCalculator(rates)
        self.embedded_calc = EmbeddedCorporateTaxCalculator(rates)
        self.other_levies_calc = OtherLeviesCalculator(rates)
        self.municipal_calc = MunicipalServicesCalculator(rates)
    
    def run(
        self,
        personal: PersonalProfile,
        consumption: ConsumptionProfile,
        transport_property: TransportAndPropertyProfile,
        investment: InvestmentProfile,
        travel: TravelProfile | None = None,
    ) -> tuple[dict[str, float], float]:
        """Run all tax calculations and return breakdown + total
        
        Returns:
            tuple of (breakdown_dict, total_tax_amount)
        """
        breakdown = {}
        
        # Calculate each category
        breakdown.update(self.paye_calc.calculate(personal))
        breakdown.update(self.indirect_calc.calculate(consumption))
        breakdown.update(self.alcohol_calc.calculate(consumption))
        breakdown.update(self.tobacco_calc.calculate(consumption))
        breakdown.update(self.property_calc.calculate(transport_property))
        breakdown.update(self.investment_calc.calculate(investment))
        breakdown.update(self.embedded_calc.calculate(consumption))
        
        # Add other levies if travel profile provided
        if travel is None:
            travel = TravelProfile()
        breakdown.update(self.other_levies_calc.calculate(consumption, travel))
        
        # Add municipal services
        breakdown.update(self.municipal_calc.calculate(transport_property))
        
        # Calculate total
        total = sum(breakdown.values())
        
        return breakdown, total
    
    def summary_list(
        self,
        personal: PersonalProfile,
        consumption: ConsumptionProfile,
        transport_property: TransportAndPropertyProfile,
        investment: InvestmentProfile,
        travel: TravelProfile | None = None,
    ) -> list[dict[str, float]]:
        """Return breakdown as a list of dicts for easier export"""
        breakdown, total = self.run(personal, consumption, transport_property, investment, travel)
        
        items = [
            {"category": k, "annual": v, "monthly": v / 12}
            for k, v in breakdown.items()
        ]
        
        # Add total row
        items.append({"category": "TOTAL", "annual": total, "monthly": total / 12})
        
        return items
