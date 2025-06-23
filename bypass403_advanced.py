#!/usr/bin/env python3
"""
🚀 WEB 403 BYPASS TOOL - ADVANCED EDITION
All-in-one script that combines all features

Author: mrx-arafat
GitHub: https://github.com/mrx-arafat/Web-403-Bypass-Tool
Version: 4.0.0 - Advanced Edition
"""

import os
import sys
import json
import time
import logging
import argparse
import asyncio
import webbrowser
from typing import Dict, List, Any, Optional, Union
from pathlib import Path

# Import core modules
from bypass403 import Bypass403, BypassTechniques, BypassResult
from integrations import IntegrationManager
from visualizer import BypassVisualizer

# Import web interface (optional)
try:
    import uvicorn
    from web_interface import app as web_app
    WEB_INTERFACE_AVAILABLE = True
except ImportError:
    WEB_INTERFACE_AVAILABLE = False

class AdvancedBypassTool:
    """Advanced 403 Bypass Tool with all features"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.integration_manager = IntegrationManager()
        self.output_dir = "reports"
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def run_scan(self, args):
        """Run the bypass scan"""
        # Initialize bypass tool
        bypass_tool = Bypass403(
            target_url=args.url,
            path=args.path,
            threads=args.threads,
            timeout=args.timeout,
            delay=args.delay,
            verbose=args.verbose,
            max_retries=args.max_retries,
            adaptive_concurrency=args.adaptive_concurrency,
            smart_prioritization=args.smart_prioritization
        )
        
        # Run bypass tests
        self.logger.info(f"Starting bypass tests against {args.url}")
        start_time = time.time()
        await bypass_tool.run_bypass_tests()
        total_time = time.time() - start_time
        
        # Generate report
        self.logger.info("Generating report")
        report_file = args.output or f"bypass_report_{int(time.time())}.json"
        report_path = os.path.join(self.output_dir, report_file)
        
        # Basic statistics
        total_tests = len(bypass_tool.results)
        successful_tests = len(bypass_tool.successful_bypasses)
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Performance metrics
        cache_hits = sum(1 for result in bypass_tool.results if hasattr(result, 'from_cache') and result.from_cache)
        cache_hit_rate = (cache_hits / total_tests * 100) if total_tests > 0 else 0
        
        # Response time analysis
        response_times = [result.response_time for result in bypass_tool.results if result.response_time > 0]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        min_response_time = min(response_times) if response_times else 0
        max_response_time = max(response_times) if response_times else 0
        
        # Most effective techniques
        technique_success = {}
        for result in bypass_tool.successful_bypasses:
            technique_type = result.technique.split(':')[0] if ':' in result.technique else result.technique
            technique_success[technique_type] = technique_success.get(technique_type, 0) + 1
        
        # Sort by count
        most_effective = dict(sorted(technique_success.items(), key=lambda x: x[1], reverse=True)[:5])
        
        # Prepare report data
        report_data = {
            "target": bypass_tool.target_url,
            "timestamp": time.time(),
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_tests": total_tests,
            "successful_bypasses": successful_tests,
            "success_rate": success_rate,
            "performance_metrics": {
                "cache_hit_rate": cache_hit_rate,
                "avg_response_time": avg_response_time,
                "min_response_time": min_response_time,
                "max_response_time": max_response_time,
                "final_concurrency": bypass_tool.current_concurrency,
                "most_effective_techniques": most_effective,
                "total_time": total_time
            },
            "successful_results": [bypass_tool.result_to_dict(result) for result in bypass_tool.successful_bypasses],
            "results_summary": [{
                "url": r.url,
                "method": r.method,
                "status_code": r.status_code,
                "response_length": r.response_length,
                "response_time": r.response_time,
                "success": r.success,
                "technique": r.technique
            } for r in bypass_tool.results]
        }
        
        # Save report to file
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        self.logger.info(f"Report saved to {report_path}")
        
        # Run integrations if requested
        if args.integrations:
            self.logger.info("Running integrations")
            integration_results = await self.run_integrations(args.url, args)
            
            # Add integration results to report
            report_data["integrations"] = integration_results
            
            # Save updated report
            with open(report_path, 'w') as f:
                json.dump(report_data, f, indent=2)
            
            self.logger.info(f"Updated report with integration results")
        
        # Generate visualizations if requested
        if args.visualize:
            self.logger.info("Generating visualizations")
            visualizer = BypassVisualizer(report_path, self.output_dir)
            
            if args.report_format == "html" or args.report_format == "all":
                html_path = visualizer.generate_html_report()
                self.logger.info(f"HTML report generated: {html_path}")
            
            if args.report_format == "pdf" or args.report_format == "all":
                pdf_path = visualizer.generate_pdf_report()
                if pdf_path:
                    self.logger.info(f"PDF report generated: {pdf_path}")
                else:
                    self.logger.warning("PDF report generation failed. Make sure weasyprint is installed.")
            
            if args.report_format == "csv" or args.report_format == "all":
                csv_path = visualizer.generate_csv_report()
                self.logger.info(f"CSV report generated: {csv_path}")
        
        # Print summary
        print("\n" + "="*50)
        print(f"SCAN SUMMARY FOR {bypass_tool.target_url}")
        print("="*50)
        print(f"Total Tests: {total_tests}")
        print(f"Successful Bypasses: {successful_tests}")
        print(f"Success Rate: {success_rate:.2f}%")
        print(f"Total Time: {total_time:.2f}s")
        print("\nMost Effective Techniques:")
        for technique, count in most_effective.items():
            print(f"- {technique}: {count} successful bypasses")
        print("\nReport saved to:", report_path)
        
        if args.visualize:
            if args.report_format == "html" or args.report_format == "all":
                print("HTML report:", html_path)
            if args.report_format == "pdf" or args.report_format == "all" and pdf_path:
                print("PDF report:", pdf_path)
            if args.report_format == "csv" or args.report_format == "all":
                print("CSV report:", csv_path)
        
        return report_data
    
    async def run_integrations(self, target: str, args):
        """Run integrations with other security tools"""
        available_tools = self.integration_manager.get_available_tools()
        
        if not available_tools:
            self.logger.warning("No integration tools available")
            return {}
        
        # Filter tools based on args
        tools_to_run = []
        if args.integrations == "all":
            tools_to_run = available_tools
        else:
            requested_tools = args.integrations.split(",")
            tools_to_run = [tool for tool in requested_tools if tool in available_tools]
        
        if not tools_to_run:
            self.logger.warning(f"No requested integration tools available. Available tools: {', '.join(available_tools)}")
            return {}
        
        self.logger.info(f"Running integrations: {', '.join(tools_to_run)}")
        
        # Prepare options for each tool
        options = {}
        for tool in tools_to_run:
            if tool == "nmap":
                options[tool] = {
                    "ports": args.nmap_ports or "80,443,8080,8443",
                    "arguments": args.nmap_args or "-sV"
                }
            elif tool == "dirsearch":
                options[tool] = {
                    "extensions": args.dirsearch_extensions or "php,html,js",
                    "wordlist": args.dirsearch_wordlist or ""
                }
            elif tool == "nuclei":
                options[tool] = {
                    "templates": args.nuclei_templates or "http/misconfiguration",
                    "severity": args.nuclei_severity or "medium,high,critical"
                }
        
        # Run tools
        results = {}
        for tool in tools_to_run:
            self.logger.info(f"Running {tool}...")
            tool_result = self.integration_manager.run_tool(tool, target, options.get(tool, {}))
            results[tool] = tool_result
            self.logger.info(f"{tool} scan completed")
        
        return results
    
    def start_web_interface(self, args):
        """Start the web interface"""
        if not WEB_INTERFACE_AVAILABLE:
            self.logger.error("Web interface dependencies not installed. Install with: pip install fastapi uvicorn jinja2")
            return False
        
        host = args.host or "0.0.0.0"
        port = args.port or 12000
        
        if args.open_browser:
            webbrowser.open(f"http://{host if host != '0.0.0.0' else 'localhost'}:{port}")
        
        self.logger.info(f"Starting web interface on http://{host}:{port}")
        uvicorn.run(web_app, host=host, port=port)
        return True

def main():
    parser = argparse.ArgumentParser(
        description="🚀 403 Bypass Tool - Advanced Edition",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 bypass403_advanced.py https://example.com
  python3 bypass403_advanced.py https://example.com -p /admin --visualize
  python3 bypass403_advanced.py https://example.com -p wordlist.txt -t 50
  python3 bypass403_advanced.py https://example.com --integrations all
  python3 bypass403_advanced.py --web-interface --open-browser
        """
    )
    
    # Main command groups
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Run a bypass scan")
    scan_parser.add_argument("url", help="Target URL")
    scan_parser.add_argument("-p", "--path", default="/admin", 
                           help="Path to test or wordlist file (default: /admin)")
    scan_parser.add_argument("-t", "--threads", type=int, default=20,
                           help="Number of threads (default: 20)")
    scan_parser.add_argument("--timeout", type=int, default=10,
                           help="Request timeout in seconds (default: 10)")
    scan_parser.add_argument("--delay", type=float, default=0.1,
                           help="Delay between requests in seconds (default: 0.1)")
    scan_parser.add_argument("-o", "--output", help="Output file for report")
    scan_parser.add_argument("-v", "--verbose", action="store_true",
                           help="Verbose output")
    
    # Performance optimization parameters
    scan_parser.add_argument("--max-retries", type=int, default=3,
                           help="Maximum number of retries for failed requests (default: 3)")
    scan_parser.add_argument("--adaptive-concurrency", action="store_true",
                           help="Enable adaptive concurrency based on response times")
    scan_parser.add_argument("--smart-prioritization", action="store_true",
                           help="Enable smart prioritization of test cases based on success patterns")
    scan_parser.add_argument("--no-cache", action="store_true",
                           help="Disable response caching")
    scan_parser.add_argument("--batch-size", type=int, default=100,
                           help="Batch size for processing test cases (default: 100)")
    
    # Visualization parameters
    scan_parser.add_argument("--visualize", action="store_true",
                           help="Generate visualizations and reports")
    scan_parser.add_argument("--report-format", choices=["html", "pdf", "csv", "all"], default="html",
                           help="Report format for visualizations (default: html)")
    
    # Integration parameters
    scan_parser.add_argument("--integrations", 
                           help="Run integrations with other security tools (comma-separated list or 'all')")
    scan_parser.add_argument("--nmap-ports", help="Ports for Nmap scan (default: 80,443,8080,8443)")
    scan_parser.add_argument("--nmap-args", help="Additional arguments for Nmap scan (default: -sV)")
    scan_parser.add_argument("--dirsearch-extensions", help="Extensions for dirsearch (default: php,html,js)")
    scan_parser.add_argument("--dirsearch-wordlist", help="Wordlist for dirsearch")
    scan_parser.add_argument("--nuclei-templates", help="Templates for Nuclei scan (default: http/misconfiguration)")
    scan_parser.add_argument("--nuclei-severity", help="Severity for Nuclei scan (default: medium,high,critical)")
    
    # Web interface command
    web_parser = subparsers.add_parser("web", help="Start the web interface")
    web_parser.add_argument("--host", default="0.0.0.0", help="Host to bind the server to")
    web_parser.add_argument("--port", type=int, default=12000, help="Port to bind the server to")
    web_parser.add_argument("--open-browser", action="store_true", help="Open browser automatically")
    
    # Visualize command
    viz_parser = subparsers.add_parser("visualize", help="Generate visualizations from an existing report")
    viz_parser.add_argument("report_file", help="Path to the JSON report file")
    viz_parser.add_argument("--output-dir", default="reports", help="Output directory for reports and charts")
    viz_parser.add_argument("--format", choices=["html", "pdf", "csv", "all"], default="html", 
                           help="Output format (default: html)")
    
    # For backwards compatibility, allow running without a subcommand
    parser.add_argument("target_url", nargs="?", help="Target URL (for backwards compatibility)")
    parser.add_argument("--web-interface", action="store_true", help="Start the web interface")
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose if hasattr(args, 'verbose') else False else logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create tool instance
    tool = AdvancedBypassTool()
    
    # Handle backwards compatibility
    if args.target_url and not args.command:
        args.command = "scan"
        args.url = args.target_url
    
    # Handle web interface flag
    if args.web_interface and not args.command:
        args.command = "web"
    
    # Execute command
    if args.command == "scan":
        asyncio.run(tool.run_scan(args))
    elif args.command == "web":
        tool.start_web_interface(args)
    elif args.command == "visualize":
        visualizer = BypassVisualizer(args.report_file, args.output_dir)
        
        if args.format == "html" or args.format == "all":
            html_path = visualizer.generate_html_report()
            print(f"HTML report generated: {html_path}")
        
        if args.format == "pdf" or args.format == "all":
            pdf_path = visualizer.generate_pdf_report()
            if pdf_path:
                print(f"PDF report generated: {pdf_path}")
            else:
                print("PDF report generation failed. Make sure weasyprint is installed.")
        
        if args.format == "csv" or args.format == "all":
            csv_path = visualizer.generate_csv_report()
            print(f"CSV report generated: {csv_path}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()