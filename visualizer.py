#!/usr/bin/env python3
"""
🚀 WEB 403 BYPASS TOOL - VISUALIZATION MODULE
Advanced visualization for bypass results

Author: mrx-arafat
GitHub: https://github.com/mrx-arafat/Web-403-Bypass-Tool
Version: 4.0.0 - Performance Edition
"""

import os
import json
import time
import logging
import argparse
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
from jinja2 import Environment, FileSystemLoader

class BypassVisualizer:
    """Visualize bypass results with advanced charts and reports"""
    
    def __init__(self, report_file: str, output_dir: str = "reports"):
        self.report_file = report_file
        self.output_dir = output_dir
        self.report_data = None
        self.logger = logging.getLogger(__name__)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Load report data
        self._load_report()
    
    def _load_report(self):
        """Load report data from file"""
        try:
            with open(self.report_file, 'r') as f:
                self.report_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            self.logger.error(f"Error loading report file: {str(e)}")
            raise ValueError(f"Error loading report file: {str(e)}")
    
    def generate_status_code_chart(self, output_file: Optional[str] = None) -> str:
        """Generate status code distribution chart"""
        if not self.report_data:
            return ""
        
        # Count status codes
        status_codes = {}
        for result in self.report_data.get("results_summary", []):
            status = result.get("status_code", 0)
            status_codes[status] = status_codes.get(status, 0) + 1
        
        # Sort by status code
        sorted_codes = sorted(status_codes.items())
        codes = [str(code) for code, _ in sorted_codes]
        counts = [count for _, count in sorted_codes]
        
        # Create color map
        colors = []
        for code in [int(c) for c in codes]:
            if code >= 200 and code < 300:
                colors.append('green')
            elif code >= 300 and code < 400:
                colors.append('blue')
            elif code >= 400 and code < 500:
                colors.append('red')
            elif code >= 500:
                colors.append('purple')
            else:
                colors.append('gray')
        
        # Create chart
        plt.figure(figsize=(12, 6))
        plt.bar(codes, counts, color=colors)
        plt.title('HTTP Status Code Distribution')
        plt.xlabel('Status Code')
        plt.ylabel('Count')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add count labels on top of bars
        for i, count in enumerate(counts):
            plt.text(i, count + 0.5, str(count), ha='center')
        
        # Save chart if output file is provided
        if output_file:
            output_path = os.path.join(self.output_dir, output_file)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            return output_path
        else:
            plt.close()
            return ""
    
    def generate_technique_success_chart(self, output_file: Optional[str] = None) -> str:
        """Generate technique success chart"""
        if not self.report_data:
            return ""
        
        # Count successful techniques
        techniques = {}
        for result in self.report_data.get("successful_results", []):
            technique = result.get("technique", "").split(':')[0] if ':' in result.get("technique", "") else result.get("technique", "")
            techniques[technique] = techniques.get(technique, 0) + 1
        
        # Sort by count (descending)
        sorted_techniques = sorted(techniques.items(), key=lambda x: x[1], reverse=True)
        
        # Limit to top 10 for readability
        if len(sorted_techniques) > 10:
            sorted_techniques = sorted_techniques[:10]
            other_count = sum(count for _, count in sorted_techniques[10:])
            if other_count > 0:
                sorted_techniques.append(("Other", other_count))
        
        labels = [tech for tech, _ in sorted_techniques]
        counts = [count for _, count in sorted_techniques]
        
        # Create chart
        plt.figure(figsize=(12, 8))
        bars = plt.barh(labels, counts, color=plt.cm.viridis(np.linspace(0, 1, len(labels))))
        plt.title('Most Successful Bypass Techniques')
        plt.xlabel('Number of Successful Bypasses')
        plt.ylabel('Technique')
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        
        # Add count labels on bars
        for i, (count, bar) in enumerate(zip(counts, bars)):
            plt.text(count + 0.1, i, str(count), va='center')
        
        # Save chart if output file is provided
        if output_file:
            output_path = os.path.join(self.output_dir, output_file)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            return output_path
        else:
            plt.close()
            return ""
    
    def generate_response_time_chart(self, output_file: Optional[str] = None) -> str:
        """Generate response time distribution chart"""
        if not self.report_data:
            return ""
        
        # Get response times
        response_times = [result.get("response_time", 0) for result in self.report_data.get("results_summary", [])]
        
        # Create bins for histogram
        bins = [0, 0.1, 0.5, 1, 2, 5, 10, max(response_times) + 0.1]
        
        # Create chart
        plt.figure(figsize=(12, 6))
        plt.hist(response_times, bins=bins, alpha=0.7, color='blue', edgecolor='black')
        plt.title('Response Time Distribution')
        plt.xlabel('Response Time (seconds)')
        plt.ylabel('Count')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add vertical line for average
        avg_time = sum(response_times) / len(response_times) if response_times else 0
        plt.axvline(x=avg_time, color='red', linestyle='--', label=f'Average: {avg_time:.2f}s')
        plt.legend()
        
        # Save chart if output file is provided
        if output_file:
            output_path = os.path.join(self.output_dir, output_file)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            return output_path
        else:
            plt.close()
            return ""
    
    def generate_method_chart(self, output_file: Optional[str] = None) -> str:
        """Generate HTTP method distribution chart"""
        if not self.report_data:
            return ""
        
        # Count methods
        methods = {}
        for result in self.report_data.get("results_summary", []):
            method = result.get("method", "UNKNOWN")
            methods[method] = methods.get(method, 0) + 1
        
        # Sort by count (descending)
        sorted_methods = sorted(methods.items(), key=lambda x: x[1], reverse=True)
        labels = [method for method, _ in sorted_methods]
        counts = [count for _, count in sorted_methods]
        
        # Create pie chart
        plt.figure(figsize=(10, 10))
        plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90, 
                colors=plt.cm.tab10(np.linspace(0, 1, len(labels))))
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title('HTTP Method Distribution')
        
        # Save chart if output file is provided
        if output_file:
            output_path = os.path.join(self.output_dir, output_file)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            return output_path
        else:
            plt.close()
            return ""
    
    def generate_success_rate_chart(self, output_file: Optional[str] = None) -> str:
        """Generate success rate chart"""
        if not self.report_data:
            return ""
        
        # Get success rate
        total_tests = self.report_data.get("total_tests", 0)
        successful_tests = self.report_data.get("successful_bypasses", 0)
        
        if total_tests == 0:
            return ""
        
        success_rate = (successful_tests / total_tests) * 100
        failure_rate = 100 - success_rate
        
        # Create chart
        plt.figure(figsize=(10, 10))
        plt.pie([success_rate, failure_rate], labels=['Success', 'Failure'], 
                autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
        plt.axis('equal')
        plt.title('Bypass Success Rate')
        
        # Save chart if output file is provided
        if output_file:
            output_path = os.path.join(self.output_dir, output_file)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            return output_path
        else:
            plt.close()
            return ""
    
    def generate_all_charts(self) -> Dict[str, str]:
        """Generate all charts and return paths"""
        timestamp = int(time.time())
        
        charts = {
            "status_code": self.generate_status_code_chart(f"status_code_{timestamp}.png"),
            "technique_success": self.generate_technique_success_chart(f"technique_success_{timestamp}.png"),
            "response_time": self.generate_response_time_chart(f"response_time_{timestamp}.png"),
            "method": self.generate_method_chart(f"method_{timestamp}.png"),
            "success_rate": self.generate_success_rate_chart(f"success_rate_{timestamp}.png")
        }
        
        return charts
    
    def generate_html_report(self, output_file: Optional[str] = None) -> str:
        """Generate HTML report with charts"""
        if not self.report_data:
            return ""
        
        # Generate all charts
        charts = self.generate_all_charts()
        
        # Create HTML template
        template_dir = os.path.join(self.output_dir, "templates")
        os.makedirs(template_dir, exist_ok=True)
        
        # Create template file
        template_file = os.path.join(template_dir, "report_template.html")
        with open(template_file, "w") as f:
            f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>403 Bypass Tool - Scan Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            color: #333;
            background-color: #f8f9fa;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: #fff;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            border-radius: 5px;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        .header {
            background-color: #3498db;
            color: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 5px;
            text-align: center;
        }
        .section {
            margin-bottom: 30px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 5px;
            border-left: 5px solid #3498db;
        }
        .chart-container {
            margin: 20px 0;
            text-align: center;
        }
        .chart {
            max-width: 100%;
            height: auto;
            border-radius: 5px;
            box-shadow: 0 0 5px rgba(0,0,0,0.2);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #3498db;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .success {
            color: green;
            font-weight: bold;
        }
        .failure {
            color: red;
        }
        .stats {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            margin-bottom: 20px;
        }
        .stat-box {
            flex: 1;
            min-width: 200px;
            margin: 10px;
            padding: 20px;
            background-color: #fff;
            border-radius: 5px;
            box-shadow: 0 0 5px rgba(0,0,0,0.1);
            text-align: center;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            margin: 10px 0;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #777;
        }
        pre {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        .technique-list {
            list-style-type: none;
            padding: 0;
        }
        .technique-item {
            padding: 10px;
            margin: 5px 0;
            background-color: #f8f9fa;
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
        }
        .technique-count {
            background-color: #3498db;
            color: white;
            padding: 2px 8px;
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 403 Bypass Tool - Scan Report</h1>
            <p>Target: {{ report.target }}</p>
            <p>Date: {{ report.date }}</p>
        </div>
        
        <div class="section">
            <h2>📊 Summary</h2>
            <div class="stats">
                <div class="stat-box">
                    <h3>Total Tests</h3>
                    <div class="stat-value">{{ report.total_tests }}</div>
                </div>
                <div class="stat-box">
                    <h3>Successful Bypasses</h3>
                    <div class="stat-value">{{ report.successful_bypasses }}</div>
                </div>
                <div class="stat-box">
                    <h3>Success Rate</h3>
                    <div class="stat-value">{{ "%.2f"|format(report.success_rate) }}%</div>
                </div>
                <div class="stat-box">
                    <h3>Total Time</h3>
                    <div class="stat-value">{{ "%.2f"|format(report.performance_metrics.total_time) }}s</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>📈 Performance Metrics</h2>
            <div class="stats">
                <div class="stat-box">
                    <h3>Cache Hit Rate</h3>
                    <div class="stat-value">{{ "%.2f"|format(report.performance_metrics.cache_hit_rate) }}%</div>
                </div>
                <div class="stat-box">
                    <h3>Avg Response Time</h3>
                    <div class="stat-value">{{ "%.3f"|format(report.performance_metrics.avg_response_time) }}s</div>
                </div>
                <div class="stat-box">
                    <h3>Min Response Time</h3>
                    <div class="stat-value">{{ "%.3f"|format(report.performance_metrics.min_response_time) }}s</div>
                </div>
                <div class="stat-box">
                    <h3>Max Response Time</h3>
                    <div class="stat-value">{{ "%.3f"|format(report.performance_metrics.max_response_time) }}s</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>🎯 Most Effective Techniques</h2>
            <ul class="technique-list">
                {% for technique, count in report.performance_metrics.most_effective_techniques.items() %}
                <li class="technique-item">
                    <span>{{ technique }}</span>
                    <span class="technique-count">{{ count }}</span>
                </li>
                {% endfor %}
            </ul>
        </div>
        
        <div class="section">
            <h2>📊 Charts</h2>
            
            <div class="chart-container">
                <h3>Success Rate</h3>
                <img src="{{ charts.success_rate }}" alt="Success Rate Chart" class="chart">
            </div>
            
            <div class="chart-container">
                <h3>Status Code Distribution</h3>
                <img src="{{ charts.status_code }}" alt="Status Code Chart" class="chart">
            </div>
            
            <div class="chart-container">
                <h3>Most Successful Techniques</h3>
                <img src="{{ charts.technique_success }}" alt="Technique Success Chart" class="chart">
            </div>
            
            <div class="chart-container">
                <h3>Response Time Distribution</h3>
                <img src="{{ charts.response_time }}" alt="Response Time Chart" class="chart">
            </div>
            
            <div class="chart-container">
                <h3>HTTP Method Distribution</h3>
                <img src="{{ charts.method }}" alt="Method Chart" class="chart">
            </div>
        </div>
        
        <div class="section">
            <h2>✅ Successful Bypasses</h2>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Technique</th>
                        <th>URL</th>
                        <th>Method</th>
                        <th>Status</th>
                        <th>Length</th>
                        <th>Time</th>
                    </tr>
                </thead>
                <tbody>
                    {% for result in report.successful_results %}
                    <tr>
                        <td>{{ loop.index }}</td>
                        <td>{{ result.technique }}</td>
                        <td>{{ result.url }}</td>
                        <td>{{ result.method }}</td>
                        <td>{{ result.status_code }}</td>
                        <td>{{ result.response_length }}</td>
                        <td>{{ "%.3f"|format(result.response_time) }}s</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>Generated by 403 Bypass Tool - Performance Edition</p>
            <p>Version 4.0.0 | Author: mrx-arafat</p>
            <p>Generated on: {{ now }}</p>
        </div>
    </div>
</body>
</html>""")
        
        # Create Jinja2 environment
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("report_template.html")
        
        # Render template
        html = template.render(
            report=self.report_data,
            charts={k: os.path.basename(v) for k, v in charts.items()},
            now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # Save HTML report
        if not output_file:
            output_file = f"report_{int(time.time())}.html"
        
        output_path = os.path.join(self.output_dir, output_file)
        with open(output_path, "w") as f:
            f.write(html)
        
        return output_path
    
    def generate_pdf_report(self, output_file: Optional[str] = None) -> str:
        """Generate PDF report with charts"""
        try:
            import weasyprint
        except ImportError:
            self.logger.error("weasyprint is not installed. Install with: pip install weasyprint")
            return ""
        
        # Generate HTML report first
        html_path = self.generate_html_report()
        
        if not html_path:
            return ""
        
        # Convert HTML to PDF
        if not output_file:
            output_file = f"report_{int(time.time())}.pdf"
        
        output_path = os.path.join(self.output_dir, output_file)
        
        try:
            html = weasyprint.HTML(filename=html_path)
            html.write_pdf(output_path)
            return output_path
        except Exception as e:
            self.logger.error(f"Error generating PDF report: {str(e)}")
            return ""
    
    def generate_csv_report(self, output_file: Optional[str] = None) -> str:
        """Generate CSV report of successful bypasses"""
        if not self.report_data:
            return ""
        
        # Create DataFrame from successful results
        successful_results = self.report_data.get("successful_results", [])
        
        if not successful_results:
            return ""
        
        df = pd.DataFrame(successful_results)
        
        # Save to CSV
        if not output_file:
            output_file = f"successful_bypasses_{int(time.time())}.csv"
        
        output_path = os.path.join(self.output_dir, output_file)
        df.to_csv(output_path, index=False)
        
        return output_path

def main():
    parser = argparse.ArgumentParser(description="403 Bypass Tool - Visualization Module")
    parser.add_argument("report_file", help="Path to the JSON report file")
    parser.add_argument("--output-dir", default="reports", help="Output directory for reports and charts")
    parser.add_argument("--format", choices=["html", "pdf", "csv", "all"], default="html", 
                       help="Output format (default: html)")
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
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
        
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())