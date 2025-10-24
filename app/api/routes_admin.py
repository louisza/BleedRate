"""Admin API routes for rate management"""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.config import settings
from app.domain.rates import TaxRates
import yaml

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))


@router.get("/admin/rates", response_class=HTMLResponse)
async def admin_rates_page(request: Request):
    """Admin page to view/edit tax rates"""
    if not settings.ADMIN_ENABLED:
        raise HTTPException(status_code=403, detail="Admin interface disabled")
    
    # Read current rates YAML
    with open(settings.TAX_RATES_PATH, 'r') as f:
        rates_yaml = f.read()
    
    return templates.TemplateResponse(
        "admin_rates.html",
        {"request": request, "rates_yaml": rates_yaml}
    )


@router.post("/admin/rates")
async def update_rates(request: Request):
    """Update tax rates from admin interface"""
    if not settings.ADMIN_ENABLED:
        raise HTTPException(status_code=403, detail="Admin interface disabled")
    
    # Get form data
    form = await request.form()
    new_rates_yaml = form.get("rates_yaml")
    
    if not new_rates_yaml:
        raise HTTPException(status_code=400, detail="No rates data provided")
    
    # Validate YAML syntax
    try:
        yaml.safe_load(new_rates_yaml)
    except yaml.YAMLError as e:
        raise HTTPException(status_code=400, detail=f"Invalid YAML: {str(e)}")
    
    # Validate rates structure by trying to load it
    try:
        # Write to a temp location first
        temp_path = settings.TAX_RATES_PATH.with_suffix('.tmp')
        with open(temp_path, 'w') as f:
            f.write(new_rates_yaml)
        
        # Try to load it
        TaxRates.load_from_yaml(temp_path)
        
        # If successful, replace the original
        temp_path.replace(settings.TAX_RATES_PATH)
        
    except Exception as e:
        # Clean up temp file if it exists
        if temp_path.exists():
            temp_path.unlink()
        raise HTTPException(status_code=400, detail=f"Invalid rates structure: {str(e)}")
    
    return {"status": "success", "message": "Rates updated successfully"}
