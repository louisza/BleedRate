"""Public API routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.api.schemas import CalcRequest, CalcResponse, RatesResponse, ScenarioSaveRequest, ScenarioResponse
from app.domain.rates import TaxRates
from app.domain.profiles import PersonalProfile, ConsumptionProfile, TransportAndPropertyProfile, InvestmentProfile
from app.domain.engine import TaxEngine
from app.config import settings
from db.session import get_session
from db.models import Scenario
import yaml

router = APIRouter()


def get_tax_engine() -> TaxEngine:
    """Dependency: Load tax rates and create engine"""
    rates = TaxRates.load_from_yaml(settings.TAX_RATES_PATH)
    return TaxEngine(rates)


@router.post("/api/calc", response_model=CalcResponse)
def calculate_tax(request: CalcRequest, engine: TaxEngine = Depends(get_tax_engine)):
    """Calculate tax breakdown from user input"""
    # Convert Pydantic models to domain profiles
    personal = PersonalProfile(**request.personal.model_dump())
    consumption = ConsumptionProfile(**request.consumption.model_dump())
    transport_property = TransportAndPropertyProfile(**request.transport_property.model_dump())
    investment = InvestmentProfile(**request.investment.model_dump())
    
    # Run calculation
    breakdown, total = engine.run(personal, consumption, transport_property, investment)
    
    # Calculate effective rate
    gross_income = personal.annual_salary + personal.annual_bonus
    effective_rate = (total / gross_income * 100.0) if gross_income > 0 else 0.0
    
    return CalcResponse(
        breakdown=breakdown,
        total=total,
        effective_rate_vs_gross=effective_rate,
        monthly_total=total / 12
    )


@router.get("/api/rates", response_model=RatesResponse)
def get_rates():
    """Get current tax rates"""
    with open(settings.TAX_RATES_PATH, 'r') as f:
        rates_data = yaml.safe_load(f)
    
    return RatesResponse(rates=rates_data)


@router.post("/api/scenario", response_model=ScenarioResponse)
def save_scenario(
    request: ScenarioSaveRequest,
    session: Session = Depends(get_session)
):
    """Save a calculation scenario"""
    scenario = Scenario(
        label=request.label,
        inputs_json=request.calc_request.model_dump_json(),
        outputs_json=request.calc_response.model_dump_json()
    )
    
    session.add(scenario)
    session.commit()
    session.refresh(scenario)
    
    return ScenarioResponse(
        id=scenario.id,
        label=scenario.label,
        created_at=scenario.created_at.isoformat(),
        inputs=scenario.inputs,
        outputs=scenario.outputs
    )


@router.get("/api/scenario/{scenario_id}", response_model=ScenarioResponse)
def get_scenario(scenario_id: str, session: Session = Depends(get_session)):
    """Retrieve a saved scenario"""
    scenario = session.get(Scenario, scenario_id)
    
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    return ScenarioResponse(
        id=scenario.id,
        label=scenario.label,
        created_at=scenario.created_at.isoformat(),
        inputs=scenario.inputs,
        outputs=scenario.outputs
    )
