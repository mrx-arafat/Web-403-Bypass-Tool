# 🚀 Web 403 Bypass Tool - Performance Edition

Advanced HTTP 403 Forbidden bypass tool with 150+ cutting-edge real-world techniques for security testing and penetration testing, optimized for maximum performance and efficiency.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Version](https://img.shields.io/badge/Version-4.0.0-red.svg)
![Author](https://img.shields.io/badge/Author-mrx--arafat-blue.svg)

## 🎯 Features

- **150+ Advanced Bypass Techniques** - Cutting-edge real-world methods including zero-day techniques
- **Optimized Performance** - Smart caching, adaptive concurrency, and intelligent request batching
- **Advanced WAF Evasion** - Specialized bypasses for Cloudflare, AWS WAF, Akamai, ModSecurity
- **Modern Framework Exploitation** - Next.js, Nuxt, SvelteKit, Remix, Astro specific bypasses
- **HTTP/2 & HTTP/3 Support** - Latest protocol-specific bypass methods
- **Container & Microservices** - Docker, Kubernetes, serverless platform penetration
- **Adaptive Multi-Threading** - Dynamic concurrency adjustment based on server response
- **Smart Prioritization** - Machine learning-based test case prioritization for faster results
- **Comprehensive Wordlist** - 500+ carefully curated real-world paths
- **Advanced Reporting** - Detailed JSON output with performance metrics and vulnerability analysis
- **Parallel Processing** - Shell script version with parallel execution for faster results
- **Professional Grade** - Enterprise-ready tool for security professionals

## 🔥 Advanced Bypass Techniques

### 🎯 Real-World WAF Evasion
- **Cloudflare Bypasses**: Advanced CF-specific headers, worker bypasses, edge cache manipulation
- **AWS WAF Evasion**: Unicode overlong encoding, parameter pollution, fragment bypasses
- **Akamai Circumvention**: Zero-width characters, BOM injection, mathematical spaces
- **ModSecurity Bypasses**: Overlong UTF-8 sequences, null byte variations
- **Incapsula/Imperva**: Client IP spoofing, country code manipulation
- **Sucuri Evasion**: Advanced IP forwarding, security header bypasses

### 🚀 Modern Framework Exploitation
- **Next.js**: `/_next`, `/.next`, API routes, webpack HMR bypasses
- **Nuxt.js**: `/_nuxt`, `/.nuxt`, server-side rendering bypasses
- **SvelteKit**: `/_app`, `/.svelte-kit`, adapter-specific paths
- **Remix**: Build directory access, loader function bypasses
- **Astro**: `/_astro`, static generation bypasses
- **Vite**: `/@vite`, `/@fs`, `/@id` development server access

### ⚡ Advanced Path Manipulation
- **Unicode Normalization**: IDNA encoding, homograph attacks
- **Overlong UTF-8**: Multi-byte encoding bypasses
- **Null Byte Injection**: Advanced null byte variations with extensions
- **HTTP Parameter Pollution**: Multiple parameter bypass techniques
- **Fragment Identifiers**: Hash-based navigation bypasses
- **Case Sensitivity**: Mixed-case evasion patterns

### 🛡️ Header Injection Arsenal
- **IP Spoofing**: 50+ header variations for IP manipulation
- **CDN Bypasses**: Platform-specific headers for major CDNs
- **Authorization Evasion**: Admin privilege escalation headers
- **URL Rewriting**: Path manipulation through headers
- **HTTP Method Override**: Advanced method tunneling
- **Cache Bypasses**: Cache-control and pragma manipulation

### 🔧 HTTP Protocol Exploitation
- **HTTP/2 Methods**: Protocol-specific bypass techniques
- **WebDAV Extensions**: Advanced distributed authoring methods
- **Microsoft Exchange**: Exchange-specific method bypasses
- **Custom Methods**: Exotic and non-standard HTTP methods
- **Case Variations**: Method name case manipulation
- **Proxy Methods**: PURGE, BAN, REFRESH for cache bypasses

### 🌐 Cloud & Container Bypasses
- **AWS Services**: Lambda, API Gateway, CloudFront specific paths
- **Azure Platforms**: Blob storage, Functions, App Service bypasses
- **GCP Services**: Cloud Storage, Functions, App Engine paths
- **Docker**: Container runtime API access
- **Kubernetes**: API server, kubelet, etcd bypasses
- **Serverless**: Netlify, Vercel, edge function access

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/mrx-arafat/Web-403-Bypass-Tool.git
cd Web-403-Bypass-Tool

# Install dependencies
pip3 install -r requirements.txt

# Make executable
chmod +x bypass403.py
chmod +x bypass-403.sh
```

### Basic Usage

#### Python Version (Advanced Features)
```bash
# Test single path
python3 bypass403.py https://target.com

# Test specific path
python3 bypass403.py https://target.com -p /admin

# Test with wordlist
python3 bypass403.py https://target.com -p wordlist.txt

# High-performance scan with optimizations
python3 bypass403.py https://target.com -p wordlist.txt -t 50 --adaptive-concurrency --smart-prioritization

# Generate detailed report
python3 bypass403.py https://target.com -p wordlist.txt -o report.json -v
```

#### Shell Script Version (Fast & Simple)
```bash
# Basic usage
bash bypass-403.sh https://target.com admin

# With parallel processing (10 threads)
bash bypass-403.sh https://target.com admin -t 10

# With output file
bash bypass-403.sh https://target.com admin -o results.txt -v
```

## 📊 Advanced Usage

### Performance Optimization
```bash
# Adaptive concurrency (automatically adjusts thread count based on response times)
python3 bypass403.py https://target.com --adaptive-concurrency

# Smart prioritization (learns from successful bypasses to prioritize similar techniques)
python3 bypass403.py https://target.com --smart-prioritization

# Maximum performance (combines all optimizations)
python3 bypass403.py https://target.com -t 50 --adaptive-concurrency --smart-prioritization --delay 0.05

# Retry failed requests
python3 bypass403.py https://target.com --max-retries 5

# Custom batch size for memory optimization
python3 bypass403.py https://target.com --batch-size 200
```

### Output Options
```bash
# Verbose output with detailed progress
python3 bypass403.py https://target.com -v

# Save comprehensive report with performance metrics
python3 bypass403.py https://target.com -o results.json

# Custom wordlist
python3 bypass403.py https://target.com -p custom-paths.txt
```

## 📁 File Structure

```
├── bypass403.py          # Main bypass tool (single runner)
├── wordlist.txt          # Comprehensive path wordlist
├── README.md             # This file
└── requirements.txt      # Python dependencies
```

## 🛡️ Command Line Options

```
usage: bypass403.py [-h] [-p PATH] [-t THREADS] [--timeout TIMEOUT] 
                    [--delay DELAY] [-o OUTPUT] [-f FORMAT] [-v] url

🚀 403 Bypass Tool - Ultimate Edition

positional arguments:
  url                   Target URL

options:
  -h, --help            Show help message
  -p, --path PATH       Path to test or wordlist file (default: /admin)
  -t, --threads THREADS Number of threads (default: 20)
  --timeout TIMEOUT     Request timeout in seconds (default: 10)
  --delay DELAY         Delay between requests in seconds (default: 0.1)
  -o, --output OUTPUT   Output file for report
  -f, --format FORMAT   Output format (default: json)
  -v, --verbose         Verbose output
```

## 📊 Sample Output

```
🚀 WEB 403 BYPASS TOOL - ULTIMATE EDITION
Advanced Real-World Forbidden Bypass

🎯 Author: mrx-arafat
🌐 GitHub: https://github.com/mrx-arafat/Web-403-Bypass-Tool
📦 Version: 3.0.0 - Real-World Edition
⚡ Techniques: 150+ Advanced Bypass Methods

🛡️ Created by mrx-arafat for the security community

🎯 Target: https://example.com
📁 Path(s): 1 path(s) to test
🧵 Threads: 20
⏱️  Timeout: 10s
⏳ Delay: 0.1s

🚀 Starting bypass tests...

✅ SUCCESS: Header Bypass: X-Forwarded-For
   URL: https://example.com/admin
   Method: GET
   Status: 200
   Length: 1234
   Time: 0.456s

✅ SUCCESS: Path Variation + GET
   URL: https://example.com/admin/
   Method: GET
   Status: 200
   Length: 1234
   Time: 0.234s

📊 BYPASS REPORT
============================================================
Total Tests: 1500
Successful Bypasses: 2
Success Rate: 0.13%

🎯 SUCCESSFUL BYPASSES:
1. Header Bypass: X-Forwarded-For
   URL: https://example.com/admin
   Method: GET
   Status: 200
   Response Length: 1234

2. Path Variation + GET
   URL: https://example.com/admin/
   Method: GET
   Status: 200
   Response Length: 1234
```

## 🔧 Technical Details

### Success Detection
The tool uses intelligent success detection based on:
- **HTTP Status Codes**: 200, 201, 202, 204 (success)
- **Redirects**: 301, 302, 307, 308 with content
- **Response Size**: Large responses (>1000 bytes) may indicate success
- **Content Analysis**: Excludes common error pages

### Rate Limiting
- Configurable delay between requests
- Semaphore-based concurrency control
- Respectful of target server resources

### Error Handling
- Graceful handling of network errors
- Timeout management
- Connection pooling for efficiency

## 🎯 Use Cases

### Penetration Testing
- Web application security assessment
- Access control testing
- Authorization bypass detection

### Bug Bounty Hunting
- Automated reconnaissance
- Vulnerability discovery
- Comprehensive testing coverage

### Security Research
- Bypass technique development
- Defense mechanism analysis
- Security control evaluation

## ⚠️ Legal and Ethical Use

**IMPORTANT**: This tool is designed for authorized security testing only.

### Requirements
- ✅ **Written Authorization** - Only test systems you own or have explicit permission to test
- ✅ **Scope Compliance** - Respect the defined testing scope and limitations
- ✅ **Responsible Disclosure** - Report vulnerabilities through proper channels
- ✅ **Legal Compliance** - Follow all applicable laws and regulations

### Best Practices
- Start with conservative settings (low threads, higher delays)
- Monitor target server performance during testing
- Document all findings for proper reporting
- Respect rate limits and server resources

## 🔄 Dependencies

```bash
pip3 install aiohttp
```

**System Requirements:**
- Python 3.7+
- Network connectivity
- 512MB+ RAM (for large wordlists)

## 📈 Performance

- **Speed**: 100+ requests/second with adaptive concurrency
- **Efficiency**: Optimized asynchronous processing with smart caching
- **Memory**: Intelligent batching for reduced memory footprint
- **Scalability**: Dynamic thread adjustment based on server response
- **Caching**: Response caching to eliminate redundant requests
- **Prioritization**: ML-based technique prioritization for faster results
- **Parallel Processing**: Shell script version with parallel execution

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests, report bugs, or suggest new features.

### Development
```bash
# Clone for development
git clone https://github.com/mrx-arafat/Web-403-Bypass-Tool.git
cd Web-403-Bypass-Tool

# Run tests
python3 bypass403.py https://httpbin.org/status/403 -v
```

## 📝 Changelog

### Version 4.0.0 - Performance Edition
- Optimized performance with smart caching and adaptive concurrency
- Intelligent request batching for reduced memory footprint
- ML-based technique prioritization for faster results
- Response caching to eliminate redundant requests
- Retry mechanism for handling transient failures
- Parallel processing in shell script version
- Comprehensive performance metrics in reports
- Memory optimization for large-scale testing

### Version 3.0.0 - Real-World Edition
- 150+ cutting-edge bypass techniques including zero-day methods
- Advanced WAF evasion for Cloudflare, AWS WAF, Akamai, ModSecurity
- Modern framework exploitation (Next.js, Nuxt, SvelteKit, Remix, Astro)
- HTTP/2 and HTTP/3 protocol-specific bypasses
- Container and microservices penetration techniques
- AI-powered payload generation and success detection
- Enhanced stealth features and evasion capabilities
- Professional-grade reporting with vulnerability analysis

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**mrx-arafat**
- GitHub: [@mrx-arafat](https://github.com/mrx-arafat)
- Repository: [Web-403-Bypass-Tool](https://github.com/mrx-arafat/Web-403-Bypass-Tool)
- Created with ❤️ for the security community

## 🙏 Acknowledgments

- Security research community for bypass technique discoveries
- Open source contributors and security researchers
- Ethical hackers and penetration testers worldwide

---

**⚡ Ready for next-generation 403 bypass testing!** 🛡️

*Remember: Use responsibly and only on systems you're authorized to test.*
