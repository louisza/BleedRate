"""Submission logging service using Supabase"""
import logging
import hashlib
import httpx
from datetime import datetime
from typing import Optional, Dict, Any
from urllib.parse import urlparse, parse_qs
from uuid import uuid4
from supabase import create_client, Client
from app.config import settings

logger = logging.getLogger(__name__)


class SubmissionLogger:
    """Log calculation submissions to Supabase with comprehensive metadata"""
    
    def __init__(self):
        self.enabled = settings.ENABLE_SUBMISSION_LOGGING
        self.client: Optional[Client] = None
        
        if self.enabled and settings.SUPABASE_URL and settings.SUPABASE_KEY:
            try:
                self.client = create_client(
                    settings.SUPABASE_URL,
                    settings.SUPABASE_KEY
                )
                logger.info("Supabase submission logging enabled")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
                self.enabled = False
        else:
            logger.info("Submission logging disabled (missing Supabase config)")
    
    async def get_geo_data(self, ip_address: str) -> Optional[Dict[str, Any]]:
        """Get geographic data from IP address using ip-api.com (free, no key needed)"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"http://ip-api.com/json/{ip_address}")
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "success":
                        return {
                            "country_code": data.get("countryCode"),
                            "country_name": data.get("country"),
                            "region": data.get("regionName"),
                            "city": data.get("city"),
                            "timezone": data.get("timezone"),
                            "latitude": data.get("lat"),
                            "longitude": data.get("lon"),
                        }
        except Exception as e:
            logger.warning(f"Failed to get geo data: {e}")
        return None
    
    def parse_user_agent(self, user_agent: str) -> Dict[str, Optional[str]]:
        """Parse user agent string to extract browser, OS, and device info"""
        # Basic parsing - you could use 'user-agents' library for more accuracy
        ua_lower = user_agent.lower()
        
        # Detect browser
        if "edg/" in ua_lower or "edge/" in ua_lower:
            browser = "Edge"
        elif "chrome/" in ua_lower and "edg/" not in ua_lower:
            browser = "Chrome"
        elif "firefox/" in ua_lower:
            browser = "Firefox"
        elif "safari/" in ua_lower and "chrome" not in ua_lower:
            browser = "Safari"
        elif "opera/" in ua_lower or "opr/" in ua_lower:
            browser = "Opera"
        else:
            browser = "Other"
        
        # Detect OS
        if "windows" in ua_lower:
            os = "Windows"
        elif "mac os x" in ua_lower or "macos" in ua_lower:
            os = "macOS"
        elif "linux" in ua_lower:
            os = "Linux"
        elif "android" in ua_lower:
            os = "Android"
        elif "iphone" in ua_lower or "ipad" in ua_lower:
            os = "iOS"
        else:
            os = "Other"
        
        # Detect device type
        if "mobile" in ua_lower or "iphone" in ua_lower:
            device_type = "mobile"
        elif "tablet" in ua_lower or "ipad" in ua_lower:
            device_type = "tablet"
        else:
            device_type = "desktop"
        
        return {
            "browser": browser,
            "os": os,
            "device_type": device_type
        }
    
    def parse_referrer(self, referrer: str) -> Dict[str, Optional[str]]:
        """Extract domain and UTM parameters from referrer URL"""
        if not referrer:
            return {"referrer_domain": None}
        
        try:
            parsed = urlparse(referrer)
            query_params = parse_qs(parsed.query)
            
            return {
                "referrer_domain": parsed.netloc,
                "utm_source": query_params.get("utm_source", [None])[0],
                "utm_medium": query_params.get("utm_medium", [None])[0],
                "utm_campaign": query_params.get("utm_campaign", [None])[0],
                "utm_term": query_params.get("utm_term", [None])[0],
                "utm_content": query_params.get("utm_content", [None])[0],
            }
        except Exception as e:
            logger.warning(f"Failed to parse referrer: {e}")
            return {"referrer_domain": None}
    
    def _validate_uuid(self, value: Optional[str]) -> Optional[str]:
        """Validate and return UUID string, or None if invalid"""
        if not value:
            return None
        
        # Check if it's a valid UUID format (8-4-4-4-12 hex characters)
        import re
        uuid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
        
        if uuid_pattern.match(value):
            return value
        else:
            logger.warning(f"Invalid UUID format: {value}, setting to None")
            return None
    
    async def log_submission(
        self,
        form_data: Dict[str, Any],
        results: Dict[str, Any],
        request_data: Dict[str, Any]
    ) -> bool:
        """
        Log a form submission with comprehensive metadata.
        
        Args:
            form_data: Form input values
            results: Calculation results
            request_data: Request metadata (headers, client info, etc.)
        
        Returns:
            True if logged successfully, False otherwise
        """
        if not self.enabled or not self.client:
            return False
        
        try:
            # Extract IP address
            ip_address = request_data.get("ip_address", "")
            ip_hash = hashlib.sha256(ip_address.encode()).hexdigest() if ip_address else None
            
            # Get geographic data
            geo_data = await self.get_geo_data(ip_address) if ip_address else {}
            
            # Parse user agent
            user_agent = request_data.get("user_agent", "")
            ua_data = self.parse_user_agent(user_agent) if user_agent else {}
            
            # Parse referrer
            referrer = request_data.get("referrer", "")
            referrer_data = self.parse_referrer(referrer)
            
            # Build submission record
            submission = {
                # Core metrics (ensure proper types)
                "timestamp": datetime.utcnow().isoformat(),
                "annual_salary": int(float(form_data.get("annual_salary", 0))) if form_data.get("annual_salary") else None,
                "total_to_govt": float(results.get("total_annual", 0)) if results.get("total_annual") else None,
                "effective_rate": float(results.get("percentage", 0)) if results.get("percentage") else None,
                
                # Full data
                "form_data": form_data,
                "results": results,
                
                # Geographic data
                "ip_hash": ip_hash,
                "country_code": geo_data.get("country_code") if geo_data else None,
                "country_name": geo_data.get("country_name") if geo_data else None,
                "region": geo_data.get("region") if geo_data else None,
                "city": geo_data.get("city") if geo_data else None,
                "timezone": geo_data.get("timezone") if geo_data else None,
                "latitude": float(geo_data.get("latitude")) if geo_data and geo_data.get("latitude") else None,
                "longitude": float(geo_data.get("longitude")) if geo_data and geo_data.get("longitude") else None,
                
                # Browser & Device
                "user_agent": user_agent[:500] if user_agent else None,
                "browser": ua_data.get("browser"),
                "os": ua_data.get("os"),
                "device_type": ua_data.get("device_type"),
                
                # Screen & Display (from client-side data, ensure integers)
                "screen_width": int(request_data.get("screen_width")) if request_data.get("screen_width") else None,
                "screen_height": int(request_data.get("screen_height")) if request_data.get("screen_height") else None,
                "screen_color_depth": int(request_data.get("screen_color_depth")) if request_data.get("screen_color_depth") else None,
                "pixel_ratio": float(request_data.get("pixel_ratio")) if request_data.get("pixel_ratio") else None,
                "viewport_width": int(request_data.get("viewport_width")) if request_data.get("viewport_width") else None,
                "viewport_height": int(request_data.get("viewport_height")) if request_data.get("viewport_height") else None,
                
                # Traffic Source
                "referrer": referrer[:500] if referrer else None,
                "referrer_domain": referrer_data.get("referrer_domain"),
                "utm_source": referrer_data.get("utm_source"),
                "utm_medium": referrer_data.get("utm_medium"),
                "utm_campaign": referrer_data.get("utm_campaign"),
                "utm_term": referrer_data.get("utm_term"),
                "utm_content": referrer_data.get("utm_content"),
                
                # Session & Behavior (validate UUID format)
                "session_id": self._validate_uuid(request_data.get("session_id")),
                "language": request_data.get("language", "")[:20] if request_data.get("language") else None,
                "languages": request_data.get("languages", "")[:200] if request_data.get("languages") else None,
                "time_to_complete_seconds": int(request_data.get("time_to_complete_seconds")) if request_data.get("time_to_complete_seconds") else None,
                
                # Browser Capabilities (from client-side)
                "cookies_enabled": request_data.get("cookies_enabled"),
                "do_not_track": request_data.get("do_not_track"),
                "online": request_data.get("online"),
                "touch_support": request_data.get("touch_support"),
                "webgl_support": request_data.get("webgl_support"),
                "local_storage_support": request_data.get("local_storage_support"),
            }
            
            # Insert into Supabase
            response = self.client.table("submissions").insert(submission).execute()
            
            if response.data:
                logger.info(f"Logged submission {response.data[0].get('id')}")
                return True
            else:
                logger.warning("Submission logged but no data returned")
                return True
                
        except Exception as e:
            logger.error(f"Failed to log submission: {e}")
            return False
    
    def get_statistics(self) -> Optional[Dict[str, Any]]:
        """
        Get basic statistics about submissions (for admin dashboard).
        
        Returns:
            Dict with statistics or None if disabled
        """
        if not self.enabled or not self.client:
            return None
        
        try:
            # Get total submissions
            response = self.client.table('submissions').select('id', count='exact').execute()
            total_count = response.count if hasattr(response, 'count') else 0
            
            # Get average effective rate
            response = self.client.rpc('get_avg_effective_rate').execute()
            avg_rate = response.data[0].get('avg_rate', 0) if response.data else 0
            
            return {
                'total_submissions': total_count,
                'average_effective_rate': avg_rate,
            }
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return None


# Global instance
submission_logger = SubmissionLogger()
