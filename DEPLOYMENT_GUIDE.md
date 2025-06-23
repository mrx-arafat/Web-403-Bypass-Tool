# 🚀 Deployment Guide - bypass403.arafatops.com

## 📋 Prerequisites

- Domain: `bypass403.arafatops.com`
- Server with Docker support
- Cloudflare account for DNS management
- SSL certificate (Let's Encrypt or Cloudflare)

## 🌐 Cloudflare DNS Setup

1. **Add DNS Record:**
   ```
   Type: A
   Name: bypass403
   Content: YOUR_SERVER_IP
   Proxy: ✅ Enabled (Orange cloud)
   TTL: Auto
   ```

2. **SSL/TLS Settings:**
   - Mode: Full (strict) or Flexible
   - Always Use HTTPS: ✅ Enabled
   - Minimum TLS Version: 1.2

## 🐳 Docker Deployment

### Option 1: Docker Compose (Recommended)

```bash
# Clone repository
git clone https://github.com/mrx-arafat/Web-403-Bypass-Tool.git
cd Web-403-Bypass-Tool

# Deploy with Docker Compose
docker-compose up -d

# Check status
docker-compose ps
docker-compose logs -f
```

### Option 2: Manual Docker

```bash
# Build image
docker build -t bypass-tool .

# Run container
docker run -d \
  --name bypass-tool \
  -p 80:8000 \
  --restart unless-stopped \
  bypass-tool

# Check logs
docker logs -f bypass-tool
```

## 🔧 Nginx Reverse Proxy (Optional)

If using Nginx as reverse proxy:

```nginx
server {
    listen 80;
    server_name bypass403.arafatops.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name bypass403.arafatops.com;

    ssl_certificate /path/to/certificate.pem;
    ssl_certificate_key /path/to/private.key;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔍 Health Monitoring

### Health Check Endpoint
```bash
curl https://bypass403.arafatops.com/health
```

Expected response:
```json
{"status":"healthy","timestamp":1750694236.9663937}
```

### Docker Health Check
```bash
# Check container health
docker ps
docker inspect bypass-tool | grep Health -A 10
```

## 🚀 Auto-Deployment with GitHub Actions

The repository includes CI/CD pipeline that:

1. **Tests** the application on every push
2. **Builds** Docker image
3. **Validates** health endpoints
4. **Deploys** to production (when configured)

### Setup Auto-Deployment

1. **Add GitHub Secrets:**
   ```
   SERVER_HOST: your-server-ip
   SERVER_USER: deployment-user
   SSH_PRIVATE_KEY: your-ssh-key
   ```

2. **Update workflow** in `.github/workflows/deploy.yml`

3. **Push to main branch** triggers deployment

## 📊 Performance Optimization

### Resource Limits
```yaml
# docker-compose.yml
services:
  bypass-tool:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

### Environment Variables
```bash
# Production settings
PYTHONUNBUFFERED=1
MAX_CONCURRENT=10
TIMEOUT=15
LOG_LEVEL=INFO
```

## 🔒 Security Considerations

### Rate Limiting
```nginx
# Nginx rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

location /api/ {
    limit_req zone=api burst=20 nodelay;
    proxy_pass http://localhost:8000;
}
```

### Firewall Rules
```bash
# UFW firewall
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable
```

## 📈 Monitoring & Logs

### Application Logs
```bash
# Docker logs
docker logs -f bypass-tool

# Application logs
tail -f /var/log/bypass-tool/app.log
```

### System Monitoring
```bash
# Resource usage
docker stats bypass-tool

# Disk usage
df -h
du -sh /var/lib/docker/
```

## 🔧 Troubleshooting

### Common Issues

1. **Port Already in Use:**
   ```bash
   sudo lsof -i :8000
   sudo kill -9 <PID>
   ```

2. **Docker Build Fails:**
   ```bash
   docker system prune -a
   docker build --no-cache -t bypass-tool .
   ```

3. **SSL Certificate Issues:**
   ```bash
   # Check certificate
   openssl s_client -connect bypass403.arafatops.com:443
   
   # Renew Let's Encrypt
   certbot renew --nginx
   ```

4. **Memory Issues:**
   ```bash
   # Check memory usage
   free -h
   docker stats
   
   # Restart container
   docker restart bypass-tool
   ```

### Debug Mode
```bash
# Run in debug mode
docker run -it --rm \
  -p 8000:8000 \
  -e LOG_LEVEL=DEBUG \
  bypass-tool
```

## 🎯 Production Checklist

- [ ] Domain DNS configured in Cloudflare
- [ ] SSL certificate installed and working
- [ ] Docker container running and healthy
- [ ] Health check endpoint responding
- [ ] Firewall rules configured
- [ ] Monitoring and logging setup
- [ ] Backup strategy implemented
- [ ] Auto-deployment pipeline tested

## 📞 Support

- **GitHub Issues**: [Report bugs](https://github.com/mrx-arafat/Web-403-Bypass-Tool/issues)
- **Documentation**: [README.md](README.md)
- **Live Demo**: [bypass403.arafatops.com](https://bypass403.arafatops.com)

---

**🚀 Ready for production deployment at bypass403.arafatops.com!**