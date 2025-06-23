#!/usr/bin/env python3
"""
🚀 Web 403 Bypass Tool - Production Web Interface
A comprehensive web application for testing 403 bypass techniques
"""

import asyncio
import aiohttp
import time
import json
import re
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, HttpUrl
import uvicorn
import logging
from bypass_techniques import BypassTechniques

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="403 Bypass Tool",
    description="Comprehensive 403 Forbidden bypass testing tool",
    version="2.0.0"
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class BypassRequest(BaseModel):
    urls: List[str]
    test_mode: str = "medium"  # quick, medium, full, custom
    custom_techniques: Optional[List[str]] = None
    timeout: int = 10
    max_concurrent: int = 5
    show_all_responses: bool = False  # Show all responses including failed ones

class BypassResult(BaseModel):
    url: str
    technique: str
    status_code: int
    response_size: int
    response_time: float
    success: bool
    interesting: bool
    error: Optional[str] = None

class ComprehensiveBypassTester:
    """Enhanced bypass tester with all 150+ techniques"""
    
    def __init__(self, timeout: int = 10, max_concurrent: int = 5):
        self.timeout = timeout
        self.max_concurrent = max_concurrent
        self.session = None
        
    async def __aenter__(self):
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=20)
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def get_bypass_techniques(self, mode: str = "medium") -> List[Dict[str, Any]]:
        """Get comprehensive bypass techniques from external module"""
        return BypassTechniques.get_techniques_by_mode(mode)
    
    def _case_variation(self, url: str) -> str:
        """Apply case variation to URL path"""
        parsed = urlparse(url)
        if parsed.path:
            # Alternate case for path
            path_chars = list(parsed.path)
            for i in range(1, len(path_chars), 2):  # Skip first char (/)
                if path_chars[i].isalpha():
                    path_chars[i] = path_chars[i].upper()
            return url.replace(parsed.path, ''.join(path_chars))
        return url
    
    def _unicode_normalize(self, url: str) -> str:
        """Apply Unicode normalization"""
        # Simple Unicode variation - replace some chars with similar Unicode
        return url.replace('a', 'а').replace('o', 'о')  # Cyrillic lookalikes
    
    def _double_encode(self, url: str) -> str:
        """Apply double URL encoding"""
        return url.replace('/', '%252F')  # %2F -> %252F
    
    async def test_single_technique(self, url: str, technique: Dict[str, Any]) -> BypassResult:
        """Test a single bypass technique"""
        start_time = time.time()
        
        try:
            # Prepare request parameters
            test_url = url
            headers = {}
            method = "GET"
            
            # Apply technique modifications based on new format
            if technique.get("headers"):
                headers.update(technique["headers"])
            
            if technique.get("method"):
                method = technique["method"]
            
            # Handle path modifications
            if technique.get("path_modifier"):
                parsed = urlparse(url)
                modified_path = technique["path_modifier"](parsed.path or "/")
                test_url = f"{parsed.scheme}://{parsed.netloc}{modified_path}"
                if parsed.query:
                    test_url += f"?{parsed.query}"
                if parsed.fragment:
                    test_url += f"#{parsed.fragment}"
            
            # Handle legacy url_modifier for backward compatibility
            elif technique.get("url_modifier"):
                test_url = technique["url_modifier"](url)
            
            # Handle protocol version
            if technique.get("version"):
                # For HTTP version, we'll add it as a header hint
                headers["Connection"] = "close" if technique["version"] == "1.0" else "keep-alive"
            
            # Make request
            async with self.session.request(method, test_url, headers=headers) as response:
                content = await response.read()
                response_time = time.time() - start_time
                
                # Determine if this is a successful bypass
                success = response.status == 200
                interesting = response.status not in [403, 404, 500] and response.status != 200
                
                return BypassResult(
                    url=test_url,
                    technique=technique["name"],
                    status_code=response.status,
                    response_size=len(content),
                    response_time=response_time,
                    success=success,
                    interesting=interesting
                )
                
        except Exception as e:
            response_time = time.time() - start_time
            return BypassResult(
                url=url,
                technique=technique["name"],
                status_code=0,
                response_size=0,
                response_time=response_time,
                success=False,
                interesting=False,
                error=str(e)
            )
    
    async def test_url(self, url: str, techniques: List[Dict[str, Any]]) -> List[BypassResult]:
        """Test all techniques against a single URL"""
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def test_with_semaphore(technique):
            async with semaphore:
                return await self.test_single_technique(url, technique)
        
        tasks = [test_with_semaphore(technique) for technique in techniques]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and return valid results
        valid_results = []
        for result in results:
            if isinstance(result, BypassResult):
                valid_results.append(result)
            elif isinstance(result, Exception):
                logger.error(f"Error testing technique: {result}")
        
        return valid_results

# Global tester instance
bypass_tester = None

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    logger.info("🚀 Starting 403 Bypass Tool Web Interface...")
    logger.info("📍 Interface will be available at the configured host and port")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global bypass_tester
    if bypass_tester and hasattr(bypass_tester, 'session') and bypass_tester.session:
        await bypass_tester.session.close()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/api/test-bypass")
async def test_bypass(request: BypassRequest):
    """Main bypass testing endpoint"""
    try:
        # Validate URLs
        valid_urls = []
        for url in request.urls:
            url = url.strip()
            if not url:
                continue
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            valid_urls.append(url)
        
        if not valid_urls:
            raise HTTPException(status_code=400, detail="No valid URLs provided")
        
        # Initialize tester
        async with ComprehensiveBypassTester(
            timeout=request.timeout,
            max_concurrent=request.max_concurrent
        ) as tester:
            
            # Get techniques based on mode
            techniques = tester.get_bypass_techniques(request.test_mode)
            
            # Test all URLs
            all_results = []
            for url in valid_urls:
                logger.info(f"Testing URL: {url}")
                url_results = await tester.test_url(url, techniques)
                all_results.extend(url_results)
        
        # Organize results
        results_by_url = {}
        for result in all_results:
            parsed_url = urlparse(result.url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
            
            if base_url not in results_by_url:
                results_by_url[base_url] = {
                    "url": base_url,
                    "total_tests": 0,
                    "successful_bypasses": 0,
                    "interesting_responses": 0,
                    "results": [],
                    "all_results": []  # Store all results for show_all_responses option
                }
            
            results_by_url[base_url]["total_tests"] += 1
            result_dict = result.dict()
            
            # Always store in all_results
            results_by_url[base_url]["all_results"].append(result_dict)
            
            # Store in filtered results based on show_all_responses setting
            if request.show_all_responses or result.success or result.interesting:
                results_by_url[base_url]["results"].append(result_dict)
            
            if result.success:
                results_by_url[base_url]["successful_bypasses"] += 1
            elif result.interesting:
                results_by_url[base_url]["interesting_responses"] += 1
        
        return {
            "success": True,
            "total_urls": len(valid_urls),
            "total_tests": len(all_results),
            "results_by_url": results_by_url,
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Error in bypass testing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/techniques")
async def get_techniques():
    """Get available bypass techniques"""
    tester = ComprehensiveBypassTester()
    return {
        "quick": tester.get_bypass_techniques("quick"),
        "medium": tester.get_bypass_techniques("medium"),
        "full": tester.get_bypass_techniques("full")
    }

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=12000,
        reload=False,
        access_log=True
    )