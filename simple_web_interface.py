#!/usr/bin/env python3
"""
Simplified Web Interface for 403 Bypass Tool
"""

import asyncio
import aiohttp
import time
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI(title="403 Bypass Tool", description="Web interface for testing 403 bypass techniques")

# Create templates directory
templates_dir = Path("templates")
templates_dir.mkdir(exist_ok=True)

# Simple HTML template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>403 Bypass Tool - Simple Interface</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select { width: 100%; padding: 8px; margin-bottom: 10px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        button:disabled { background: #ccc; }
        .results { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; }
        .success { color: green; }
        .failed { color: red; }
        .interesting { color: orange; }
    </style>
</head>
<body>
    <h1>🚀 403 Bypass Tool - Simple Interface</h1>
    
    <form id="bypassForm">
        <div class="form-group">
            <label for="target_url">Target URL:</label>
            <input type="url" id="target_url" name="target_url" value="https://httpbin.org/status/403" required>
        </div>
        
        <div class="form-group">
            <label for="test_count">Number of tests:</label>
            <select id="test_count" name="test_count">
                <option value="5">Quick (5 tests)</option>
                <option value="10" selected>Medium (10 tests)</option>
                <option value="20">Full (20 tests)</option>
            </select>
        </div>
        
        <button type="submit" id="submitBtn">🚀 Start Testing</button>
    </form>
    
    <div id="results" class="results" style="display: none;">
        <h3>Test Results</h3>
        <div id="resultsContent"></div>
    </div>

    <script>
        document.getElementById('bypassForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = document.getElementById('submitBtn');
            const resultsDiv = document.getElementById('results');
            const resultsContent = document.getElementById('resultsContent');
            
            submitBtn.disabled = true;
            submitBtn.textContent = '🔄 Testing...';
            resultsDiv.style.display = 'block';
            resultsContent.innerHTML = '<p>Running tests...</p>';
            
            const formData = new FormData(e.target);
            const requestData = {
                target_url: formData.get('target_url'),
                test_count: parseInt(formData.get('test_count'))
            };
            
            try {
                const response = await fetch('/api/simple-test', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(requestData)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    displayResults(result);
                } else {
                    throw new Error(result.detail || 'Test failed');
                }
            } catch (error) {
                resultsContent.innerHTML = `<p class="failed">❌ Error: ${error.message}</p>`;
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = '🚀 Start Testing';
            }
        });
        
        function displayResults(result) {
            const resultsContent = document.getElementById('resultsContent');
            
            let html = `
                <h4>Summary</h4>
                <p><strong>Total Tests:</strong> ${result.total_tests}</p>
                <p><strong>Successful Bypasses:</strong> ${result.successful_bypasses.length}</p>
                <p><strong>Interesting Responses:</strong> ${result.interesting_responses.length}</p>
                <p><strong>Execution Time:</strong> ${result.execution_time.toFixed(2)}s</p>
                
                <h4>Results</h4>
            `;
            
            if (result.successful_bypasses.length > 0) {
                html += '<h5 class="success">✅ Successful Bypasses:</h5>';
                result.successful_bypasses.forEach(bypass => {
                    html += `<p class="success">• ${bypass.technique}: ${bypass.status_code} (${bypass.response_length} bytes)</p>`;
                });
            }
            
            if (result.interesting_responses.length > 0) {
                html += '<h5 class="interesting">🔍 Interesting Responses:</h5>';
                result.interesting_responses.forEach(resp => {
                    html += `<p class="interesting">• ${resp.technique}: ${resp.status_code} (${resp.response_length} bytes)</p>`;
                });
            }
            
            if (result.failed_attempts.length > 0) {
                html += '<h5 class="failed">❌ Failed Attempts (showing first 5):</h5>';
                result.failed_attempts.slice(0, 5).forEach(fail => {
                    html += `<p class="failed">• ${fail.technique}: ${fail.status_code}</p>`;
                });
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

async def run_simple_bypass_test(target_url: str, test_count: int):
    """Run a simplified bypass test"""
    start_time = time.time()
    successful_bypasses = []
    interesting_responses = []
    failed_attempts = []
    
    # Define simple test techniques
    techniques = [
        ("Basic Request", target_url, {}),
        ("Trailing Slash", target_url + "/", {}),
        ("Double Slash", target_url.replace("://", ":////"), {}),
        ("X-Forwarded-For", target_url, {"headers": {"X-Forwarded-For": "127.0.0.1"}}),
        ("X-Real-IP", target_url, {"headers": {"X-Real-IP": "127.0.0.1"}}),
        ("X-Originating-IP", target_url, {"headers": {"X-Originating-IP": "127.0.0.1"}}),
        ("User-Agent: Googlebot", target_url, {"headers": {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}}),
        ("Referer: google.com", target_url, {"headers": {"Referer": "https://www.google.com/"}}),
        ("Accept: text/html", target_url, {"headers": {"Accept": "text/html,application/xhtml+xml"}}),
        ("Method: POST", target_url, {"method": "POST"}),
        ("Method: HEAD", target_url, {"method": "HEAD"}),
        ("Method: OPTIONS", target_url, {"method": "OPTIONS"}),
        ("Case Variation", target_url.replace("/status/", "/STATUS/"), {}),
        ("URL Encoding", target_url.replace("/", "%2F"), {}),
        ("Query Parameter", target_url + "?test=1", {}),
        ("Fragment", target_url + "#test", {}),
        ("HTTP/1.0", target_url, {"headers": {"Connection": "close"}}),
        ("Cache-Control", target_url, {"headers": {"Cache-Control": "no-cache"}}),
        ("Authorization: Basic", target_url, {"headers": {"Authorization": "Basic dGVzdDp0ZXN0"}}),
        ("Host Header", target_url, {"headers": {"Host": "localhost"}}),
    ]
    
    # Limit techniques based on test count
    techniques = techniques[:test_count]
    
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
        for technique_name, test_url, options in techniques:
            try:
                method = options.get("method", "GET")
                headers = options.get("headers", {})
                
                request_start = time.time()
                
                async with session.request(method, test_url, headers=headers, allow_redirects=False) as response:
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
                    elif response.status != 403 or len(content) > 1000:  # Unusual response
                        interesting_responses.append(result)
                    else:
                        failed_attempts.append(result)
                
                # Small delay between requests
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
        "test_count": test_count,
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

@app.post("/api/simple-test")
async def simple_test(request: Request):
    """API endpoint to run simple bypass tests"""
    try:
        data = await request.json()
        target_url = data.get("target_url", "").strip()
        test_count = data.get("test_count", 10)
        
        if not target_url:
            raise HTTPException(status_code=400, detail="Target URL is required")
        
        if not target_url.startswith(("http://", "https://")):
            raise HTTPException(status_code=400, detail="Target URL must start with http:// or https://")
        
        results = await run_simple_bypass_test(target_url, test_count)
        
        return JSONResponse(content=results)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "403 Bypass Tool API is running"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Simple 403 Bypass Tool Web Interface...")
    print("📍 Access the interface at: http://localhost:12000")
    uvicorn.run(app, host="0.0.0.0", port=12000)