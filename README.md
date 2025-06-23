# 🚀 403 Bypass Tool - Professional Edition

A comprehensive web application for testing 403 Forbidden bypass techniques with **150+ advanced methods** across 6 major categories.

## 🌟 Features

- **150+ Bypass Techniques**: Comprehensive collection across 6 major categories
- **Advanced Header Manipulation**: 40+ IP spoofing, User-Agent, and authentication headers
- **HTTP Method Variations**: 25+ methods including WebDAV and custom protocols
- **Path Manipulation**: 50+ encoding, case variation, and special character techniques
- **Protocol Testing**: HTTP/1.0, HTTP/1.1, HTTP/2.0 support
- **Host Header Attacks**: 20+ localhost and internal domain variations
- **Encoding Techniques**: Base64, Hex, Unicode, ROT13, and HTML entities
- **Batch Testing**: Test multiple URLs simultaneously with concurrent processing
- **Professional Web Interface**: Modern glassmorphism design with real-time results
- **Multiple Test Modes**: Quick (20), Medium (50), Full (150+ techniques)
- **Show All Responses**: Option to view all attempts including failed ones
- **Detailed Analytics**: Success rates, response analysis, timing metrics
- **Production Ready**: Docker support, health checks, CI/CD pipeline

## 🚀 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/mrx-arafat/Web-403-Bypass-Tool.git
cd Web-403-Bypass-Tool

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Visit `http://localhost:8000` to access the web interface.

### Docker Deployment

```bash
# Build and run with Docker
docker-compose up -d

# Or build manually
docker build -t bypass-tool .
docker run -p 8000:8000 bypass-tool
```

## 🎯 Usage

1. **Enter Target URLs**: Add one or more URLs to test (one per line)
2. **Select Test Mode**: Choose from Quick, Medium, or Full testing
3. **Configure Settings**: Set timeout and concurrency limits
4. **Start Testing**: Click "Start Comprehensive Testing"
5. **Analyze Results**: Review successful bypasses and interesting responses

### Example URLs to Test

```
https://example.com/admin
https://target.com/api/v1
https://site.com/restricted
https://app.com/dashboard
https://domain.com/private
```

## 🛠️ Comprehensive Bypass Techniques (150+)

### 🎯 Header Manipulation (40+ techniques)
- **IP Spoofing**: X-Forwarded-For, X-Real-IP, X-Originating-IP, X-Remote-IP
- **User-Agent Variations**: Googlebot, Bingbot, wget, curl, mobile browsers
- **Authentication Headers**: X-API-Key, Authorization, X-Auth-Token
- **Proxy Headers**: X-Forwarded-Host, X-Forwarded-Proto, Via
- **Custom Headers**: X-Custom-IP-Authorization, X-Rewrite-URL

### 🔄 HTTP Method Variations (25+ techniques)
- **Standard Methods**: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS
- **WebDAV Methods**: PROPFIND, PROPPATCH, MKCOL, COPY, MOVE, LOCK, UNLOCK
- **Version Control**: VERSION-CONTROL, REPORT, CHECKOUT, CHECKIN
- **Advanced Methods**: TRACE, CONNECT, BASELINE-CONTROL, MKACTIVITY

### 🛤️ Path Manipulation (50+ techniques)
- **Encoding Variations**: URL encoding, double encoding, Unicode normalization
- **Case Sensitivity**: Mixed case, uppercase, lowercase variations
- **Special Characters**: Null bytes, asterisks, pipes, ampersands, percent signs
- **Path Traversal**: Dot segments, double slashes, trailing slashes
- **Semicolon Injection**: Parameter pollution, path confusion

### 🌐 Protocol Variations (15+ techniques)
- **HTTP Versions**: HTTP/0.9, HTTP/1.0, HTTP/1.1, HTTP/2.0
- **Protocol Downgrade**: Force older protocol versions
- **Connection Types**: Keep-alive, close, upgrade

### 🏠 Host Header Manipulation (20+ techniques)
- **Localhost Variations**: 127.0.0.1, ::1, localhost, 0.0.0.0
- **Internal Networks**: 192.168.x.x, 10.x.x.x, 172.16.x.x
- **Domain Variations**: Empty host, malformed hosts, port variations

### 🔤 Encoding Techniques (20+ techniques)
- **Base64 Encoding**: Path and parameter encoding
- **Hex Encoding**: URL hex encoding variations
- **Unicode**: UTF-8, UTF-16 normalization
- **ROT13**: Simple character rotation
- **HTML Entities**: Entity encoding for special characters

## 📊 API Endpoints

- `GET /` - Web interface
- `POST /api/test-bypass` - Main testing endpoint
- `GET /api/techniques` - Available techniques
- `GET /health` - Health check

## 🔧 Configuration

### Environment Variables

```bash
# Application settings
PORT=8000
HOST=0.0.0.0
TIMEOUT=10
MAX_CONCURRENT=5

# Production settings
PYTHONUNBUFFERED=1
```

### Test Modes

- **Quick (20 techniques)**: Essential headers and basic methods
- **Medium (50 techniques)**: Extended headers, path variations, and encoding
- **Full (150+ techniques)**: Complete arsenal of all available bypass methods

## 🚀 Production Deployment

### Domain Setup

1. **DNS Configuration**: Point `bypass403.arafatops.com` to your server
2. **SSL Certificate**: Use Let's Encrypt or Cloudflare SSL
3. **Reverse Proxy**: Configure Nginx/Apache if needed

### Cloudflare Setup

```bash
# Add DNS record in Cloudflare
Type: A
Name: bypass403
Content: YOUR_SERVER_IP
Proxy: Enabled (Orange cloud)
```

### Server Deployment

```bash
# Clone and deploy
git clone https://github.com/mrx-arafat/Web-403-Bypass-Tool.git
cd Web-403-Bypass-Tool

# Production deployment
docker-compose up -d

# Or with custom port
docker run -d -p 80:8000 --name bypass-tool bypass-tool
```

## 🔒 Security Considerations

- **Authorized Testing Only**: Only test systems you own or have permission to test
- **Rate Limiting**: Built-in concurrency limits to prevent abuse
- **No Data Storage**: No request/response data is stored permanently
- **Ethical Use**: Tool designed for legitimate security testing

## 📈 Performance

- **Async Processing**: Concurrent request handling
- **Optimized Timeouts**: Configurable request timeouts
- **Resource Management**: Automatic connection pooling
- **Scalable Architecture**: Docker-ready for horizontal scaling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add new bypass techniques or improvements
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is for educational and authorized security testing purposes only. Users are responsible for ensuring they have proper authorization before testing any systems.

## 🔗 Links

- **Live Demo**: [bypass403.arafatops.com](https://bypass403.arafatops.com)
- **GitHub**: [mrx-arafat/Web-403-Bypass-Tool](https://github.com/mrx-arafat/Web-403-Bypass-Tool)
- **Issues**: [Report bugs or request features](https://github.com/mrx-arafat/Web-403-Bypass-Tool/issues)

---

**Developed by [mrx-arafat](https://github.com/mrx-arafat) with ❤️ for the security community**

## 👨‍💻 Author

**mrx-arafat** - Security Researcher & Developer
- GitHub: [@mrx-arafat](https://github.com/mrx-arafat)
- Website: [arafatops.com](https://arafatops.com)
- Tool: [bypass403.arafatops.com](https://bypass403.arafatops.com)