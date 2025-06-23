#!/usr/bin/env python3
"""
🚀 WEB 403 BYPASS TOOL - INTEGRATIONS MODULE
Integration with other security tools

Author: mrx-arafat
GitHub: https://github.com/mrx-arafat/Web-403-Bypass-Tool
Version: 4.0.0 - Performance Edition
"""

import os
import json
import time
import logging
import subprocess
import requests
from typing import Dict, List, Any, Optional, Union
from pathlib import Path

class ToolIntegration:
    """Base class for tool integrations"""
    
    def __init__(self, tool_path: Optional[str] = None):
        self.tool_path = tool_path
        self.logger = logging.getLogger(__name__)
    
    def is_installed(self) -> bool:
        """Check if the tool is installed"""
        raise NotImplementedError("Subclasses must implement this method")
    
    def run(self, target: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Run the tool against the target"""
        raise NotImplementedError("Subclasses must implement this method")

class NmapIntegration(ToolIntegration):
    """Integration with Nmap for port scanning"""
    
    def __init__(self, tool_path: Optional[str] = None):
        super().__init__(tool_path)
        self.tool_path = tool_path or "nmap"
    
    def is_installed(self) -> bool:
        """Check if Nmap is installed"""
        try:
            result = subprocess.run([self.tool_path, "--version"], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   text=True,
                                   timeout=5)
            return result.returncode == 0 and "Nmap" in result.stdout
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def run(self, target: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Run Nmap scan against the target"""
        if not self.is_installed():
            self.logger.error("Nmap is not installed or not found in PATH")
            return {"error": "Nmap is not installed or not found in PATH"}
        
        options = options or {}
        ports = options.get("ports", "80,443,8080,8443")
        arguments = options.get("arguments", "-sV")
        
        output_file = f"nmap_scan_{int(time.time())}.xml"
        
        try:
            cmd = [self.tool_path, "-p", ports, arguments, "-oX", output_file, target]
            self.logger.info(f"Running Nmap command: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   text=True,
                                   timeout=300)  # 5 minute timeout
            
            if result.returncode != 0:
                self.logger.error(f"Nmap scan failed: {result.stderr}")
                return {"error": f"Nmap scan failed: {result.stderr}"}
            
            # Parse XML output
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    xml_content = f.read()
                
                # Simple parsing to extract open ports
                open_ports = []
                for line in xml_content.split('\n'):
                    if 'portid=' in line and 'state="open"' in line:
                        port = line.split('portid="')[1].split('"')[0]
                        service = "unknown"
                        if 'service name=' in line:
                            service = line.split('service name="')[1].split('"')[0]
                        open_ports.append({"port": port, "service": service})
                
                return {
                    "target": target,
                    "timestamp": time.time(),
                    "open_ports": open_ports,
                    "raw_output": result.stdout,
                    "xml_output": xml_content
                }
            else:
                self.logger.error(f"Nmap output file not found: {output_file}")
                return {"error": f"Nmap output file not found: {output_file}"}
                
        except subprocess.TimeoutExpired:
            self.logger.error("Nmap scan timed out")
            return {"error": "Nmap scan timed out"}
        except Exception as e:
            self.logger.error(f"Error running Nmap scan: {str(e)}")
            return {"error": f"Error running Nmap scan: {str(e)}"}

class DirsearchIntegration(ToolIntegration):
    """Integration with dirsearch for directory brute forcing"""
    
    def __init__(self, tool_path: Optional[str] = None):
        super().__init__(tool_path)
        self.tool_path = tool_path or "dirsearch"
    
    def is_installed(self) -> bool:
        """Check if dirsearch is installed"""
        try:
            result = subprocess.run([self.tool_path, "--version"], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   text=True,
                                   timeout=5)
            return result.returncode == 0 and "dirsearch" in result.stdout.lower()
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def run(self, target: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Run dirsearch against the target"""
        if not self.is_installed():
            self.logger.error("dirsearch is not installed or not found in PATH")
            return {"error": "dirsearch is not installed or not found in PATH"}
        
        options = options or {}
        extensions = options.get("extensions", "php,html,js")
        wordlist = options.get("wordlist", "")
        
        output_file = f"dirsearch_scan_{int(time.time())}.json"
        
        try:
            cmd = [self.tool_path, "-u", target, "-e", extensions, "--format=json", "-o", output_file]
            
            if wordlist:
                cmd.extend(["-w", wordlist])
            
            self.logger.info(f"Running dirsearch command: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   text=True,
                                   timeout=600)  # 10 minute timeout
            
            if result.returncode != 0:
                self.logger.error(f"dirsearch scan failed: {result.stderr}")
                return {"error": f"dirsearch scan failed: {result.stderr}"}
            
            # Parse JSON output
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    try:
                        scan_results = json.load(f)
                        return {
                            "target": target,
                            "timestamp": time.time(),
                            "results": scan_results,
                            "raw_output": result.stdout
                        }
                    except json.JSONDecodeError:
                        self.logger.error(f"Failed to parse dirsearch JSON output")
                        return {"error": "Failed to parse dirsearch JSON output"}
            else:
                self.logger.error(f"dirsearch output file not found: {output_file}")
                return {"error": f"dirsearch output file not found: {output_file}"}
                
        except subprocess.TimeoutExpired:
            self.logger.error("dirsearch scan timed out")
            return {"error": "dirsearch scan timed out"}
        except Exception as e:
            self.logger.error(f"Error running dirsearch scan: {str(e)}")
            return {"error": f"Error running dirsearch scan: {str(e)}"}

class NucleiIntegration(ToolIntegration):
    """Integration with Nuclei for vulnerability scanning"""
    
    def __init__(self, tool_path: Optional[str] = None):
        super().__init__(tool_path)
        self.tool_path = tool_path or "nuclei"
    
    def is_installed(self) -> bool:
        """Check if Nuclei is installed"""
        try:
            result = subprocess.run([self.tool_path, "-version"], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   text=True,
                                   timeout=5)
            return result.returncode == 0 and "nuclei" in result.stdout.lower()
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def run(self, target: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Run Nuclei scan against the target"""
        if not self.is_installed():
            self.logger.error("Nuclei is not installed or not found in PATH")
            return {"error": "Nuclei is not installed or not found in PATH"}
        
        options = options or {}
        templates = options.get("templates", "http/misconfiguration")
        severity = options.get("severity", "medium,high,critical")
        
        output_file = f"nuclei_scan_{int(time.time())}.json"
        
        try:
            cmd = [
                self.tool_path, 
                "-u", target, 
                "-t", templates,
                "-s", severity,
                "-o", output_file,
                "-json"
            ]
            
            self.logger.info(f"Running Nuclei command: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   text=True,
                                   timeout=900)  # 15 minute timeout
            
            if result.returncode != 0:
                self.logger.error(f"Nuclei scan failed: {result.stderr}")
                return {"error": f"Nuclei scan failed: {result.stderr}"}
            
            # Parse JSON output
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    try:
                        # Nuclei outputs one JSON object per line
                        scan_results = []
                        for line in f:
                            if line.strip():
                                scan_results.append(json.loads(line))
                        
                        return {
                            "target": target,
                            "timestamp": time.time(),
                            "results": scan_results,
                            "raw_output": result.stdout
                        }
                    except json.JSONDecodeError:
                        self.logger.error(f"Failed to parse Nuclei JSON output")
                        return {"error": "Failed to parse Nuclei JSON output"}
            else:
                self.logger.error(f"Nuclei output file not found: {output_file}")
                return {"error": f"Nuclei output file not found: {output_file}"}
                
        except subprocess.TimeoutExpired:
            self.logger.error("Nuclei scan timed out")
            return {"error": "Nuclei scan timed out"}
        except Exception as e:
            self.logger.error(f"Error running Nuclei scan: {str(e)}")
            return {"error": f"Error running Nuclei scan: {str(e)}"}

class WaybackMachineIntegration:
    """Integration with Wayback Machine for historical content"""
    
    def __init__(self):
        self.base_url = "https://archive.org/wayback/available"
        self.logger = logging.getLogger(__name__)
    
    def search(self, url: str, timestamp: Optional[str] = None) -> Dict[str, Any]:
        """Search for URL in Wayback Machine"""
        params = {"url": url}
        if timestamp:
            params["timestamp"] = timestamp
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                "url": url,
                "timestamp": time.time(),
                "results": data,
                "has_snapshots": bool(data.get("archived_snapshots", {}))
            }
        except requests.RequestException as e:
            self.logger.error(f"Error querying Wayback Machine: {str(e)}")
            return {"error": f"Error querying Wayback Machine: {str(e)}"}
        except json.JSONDecodeError:
            self.logger.error("Failed to parse Wayback Machine response")
            return {"error": "Failed to parse Wayback Machine response"}

class SecurityHeadersIntegration:
    """Integration with securityheaders.com API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.base_url = "https://api.securityheaders.com"
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)
    
    def scan(self, url: str) -> Dict[str, Any]:
        """Scan URL for security headers"""
        if not self.api_key:
            # Fallback to manual check if no API key
            return self._manual_check(url)
        
        try:
            headers = {"API-Key": self.api_key}
            response = requests.get(f"{self.base_url}/v1/scan", 
                                   params={"url": url}, 
                                   headers=headers,
                                   timeout=30)
            response.raise_for_status()
            data = response.json()
            
            return {
                "url": url,
                "timestamp": time.time(),
                "results": data
            }
        except requests.RequestException as e:
            self.logger.error(f"Error scanning security headers: {str(e)}")
            return {"error": f"Error scanning security headers: {str(e)}"}
        except json.JSONDecodeError:
            self.logger.error("Failed to parse security headers response")
            return {"error": "Failed to parse security headers response"}
    
    def _manual_check(self, url: str) -> Dict[str, Any]:
        """Manually check security headers"""
        try:
            response = requests.get(url, timeout=10)
            headers = response.headers
            
            security_headers = {
                "Strict-Transport-Security": headers.get("Strict-Transport-Security"),
                "Content-Security-Policy": headers.get("Content-Security-Policy"),
                "X-Frame-Options": headers.get("X-Frame-Options"),
                "X-Content-Type-Options": headers.get("X-Content-Type-Options"),
                "Referrer-Policy": headers.get("Referrer-Policy"),
                "Permissions-Policy": headers.get("Permissions-Policy"),
                "X-XSS-Protection": headers.get("X-XSS-Protection")
            }
            
            # Filter out None values
            security_headers = {k: v for k, v in security_headers.items() if v is not None}
            
            return {
                "url": url,
                "timestamp": time.time(),
                "status_code": response.status_code,
                "security_headers": security_headers,
                "missing_headers": [k for k, v in security_headers.items() if v is None]
            }
        except requests.RequestException as e:
            self.logger.error(f"Error checking security headers: {str(e)}")
            return {"error": f"Error checking security headers: {str(e)}"}

class IntegrationManager:
    """Manager for all tool integrations"""
    
    def __init__(self):
        self.integrations = {
            "nmap": NmapIntegration(),
            "dirsearch": DirsearchIntegration(),
            "nuclei": NucleiIntegration(),
            "wayback": WaybackMachineIntegration(),
            "securityheaders": SecurityHeadersIntegration()
        }
        self.logger = logging.getLogger(__name__)
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tools"""
        available = []
        for name, integration in self.integrations.items():
            if hasattr(integration, "is_installed") and integration.is_installed():
                available.append(name)
            elif name in ["wayback", "securityheaders"]:  # Web services don't need installation
                available.append(name)
        return available
    
    def run_tool(self, tool_name: str, target: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Run a specific tool against the target"""
        if tool_name not in self.integrations:
            self.logger.error(f"Tool {tool_name} not supported")
            return {"error": f"Tool {tool_name} not supported"}
        
        integration = self.integrations[tool_name]
        
        if hasattr(integration, "is_installed") and not integration.is_installed():
            self.logger.error(f"Tool {tool_name} is not installed")
            return {"error": f"Tool {tool_name} is not installed"}
        
        if tool_name == "wayback":
            return integration.search(target, options.get("timestamp") if options else None)
        elif tool_name == "securityheaders":
            return integration.scan(target)
        else:
            return integration.run(target, options)
    
    def run_all_available(self, target: str, options: Dict[str, Dict[str, Any]] = None) -> Dict[str, Dict[str, Any]]:
        """Run all available tools against the target"""
        options = options or {}
        results = {}
        
        for tool in self.get_available_tools():
            tool_options = options.get(tool, {})
            results[tool] = self.run_tool(tool, target, tool_options)
        
        return results

# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python integrations.py <target_url>")
        sys.exit(1)
    
    target = sys.argv[1]
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    manager = IntegrationManager()
    available_tools = manager.get_available_tools()
    
    print(f"Available tools: {', '.join(available_tools)}")
    
    if available_tools:
        print(f"Running all available tools against {target}...")
        results = manager.run_all_available(target)
        
        for tool, result in results.items():
            print(f"\n=== {tool.upper()} RESULTS ===")
            if "error" in result:
                print(f"Error: {result['error']}")
            else:
                print(json.dumps(result, indent=2))
    else:
        print("No tools available. Please install at least one of: nmap, dirsearch, nuclei")