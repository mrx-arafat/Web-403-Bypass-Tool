#!/usr/bin/env python3
"""
Simple test script to debug the API issue
"""

import asyncio
import aiohttp
import time

async def test_simple_bypass():
    """Test a simple bypass technique"""
    target_url = "https://httpbin.org/status/403"
    
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
        print(f"Testing {target_url}...")
        
        # Test 1: Basic request
        try:
            async with session.get(target_url) as response:
                content = await response.read()
                print(f"Basic request: {response.status} ({len(content)} bytes)")
        except Exception as e:
            print(f"Basic request failed: {e}")
        
        # Test 2: With X-Forwarded-For header
        try:
            headers = {"X-Forwarded-For": "127.0.0.1"}
            async with session.get(target_url, headers=headers) as response:
                content = await response.read()
                print(f"X-Forwarded-For: {response.status} ({len(content)} bytes)")
        except Exception as e:
            print(f"X-Forwarded-For failed: {e}")
        
        # Test 3: Path variation
        try:
            test_url = target_url + "/"
            async with session.get(test_url) as response:
                content = await response.read()
                print(f"Path with slash: {response.status} ({len(content)} bytes)")
        except Exception as e:
            print(f"Path variation failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_simple_bypass())