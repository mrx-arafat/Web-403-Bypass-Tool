#!/usr/bin/env python3
"""
Demo script for the Legendary 403 Bypass Tool Suite
Shows the tools in action with example usage
"""

import subprocess
import sys
import time
import os

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_banner():
    banner = f"""
{Colors.CYAN}
██████╗ ███████╗███╗   ███╗ ██████╗ 
██╔══██╗██╔════╝████╗ ████║██╔═══██╗
██║  ██║█████╗  ██╔████╔██║██║   ██║
██║  ██║██╔══╝  ██║╚██╔╝██║██║   ██║
██████╔╝███████╗██║ ╚═╝ ██║╚██████╔╝
╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝ 
{Colors.END}
{Colors.YELLOW}    LEGENDARY 403 BYPASS DEMO{Colors.END}
{Colors.GREEN}   Showcasing the Tool Suite{Colors.END}
    """
    print(banner)

def run_command(cmd, description):
    """Run a command and display the output"""
    print(f"\n{Colors.BOLD}🚀 {description}{Colors.END}")
    print(f"{Colors.CYAN}Command: {' '.join(cmd)}{Colors.END}")
    print("-" * 80)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print(f"{Colors.YELLOW}Stderr: {result.stderr}{Colors.END}")
            
        if result.returncode != 0:
            print(f"{Colors.RED}Command failed with exit code: {result.returncode}{Colors.END}")
        else:
            print(f"{Colors.GREEN}✅ Command completed successfully{Colors.END}")
            
    except subprocess.TimeoutExpired:
        print(f"{Colors.YELLOW}⚠️  Command timed out after 30 seconds{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}❌ Error running command: {e}{Colors.END}")

def demo_help_commands():
    """Demo the help commands"""
    print(f"\n{Colors.BOLD}📚 HELP COMMANDS DEMO{Colors.END}")
    
    # Python tool help
    run_command(
        ["python3", "legendary-403-bypass.py", "--help"],
        "Python Tool Help"
    )
    
    # Bash tool help
    run_command(
        ["bash", "legendary-403-bypass.sh", "--help"],
        "Bash Tool Help"
    )
    
    # Batch tool help
    run_command(
        ["python3", "batch-403-bypass.py", "--help"],
        "Batch Tool Help"
    )

def demo_single_path_testing():
    """Demo single path testing"""
    print(f"\n{Colors.BOLD}🎯 SINGLE PATH TESTING DEMO{Colors.END}")
    
    # Test against httpbin.org (safe testing target)
    test_url = "https://httpbin.org"
    test_path = "status/403"
    
    print(f"{Colors.CYAN}Testing against: {test_url}/{test_path}{Colors.END}")
    print(f"{Colors.YELLOW}Note: This is a safe testing target that returns 403 status{Colors.END}")
    
    # Python version with limited techniques for demo
    run_command(
        ["python3", "legendary-403-bypass.py", test_url, test_path, "--timeout", "10", "--threads", "5"],
        "Python Tool - Single Path Test"
    )

def demo_wordlist_info():
    """Demo wordlist information"""
    print(f"\n{Colors.BOLD}📋 WORDLIST INFORMATION{Colors.END}")
    
    # Show wordlist stats
    try:
        with open("common-paths.txt", "r") as f:
            lines = f.readlines()
            total_paths = len([line for line in lines if line.strip() and not line.startswith('#')])
            
        print(f"{Colors.GREEN}✅ Wordlist loaded: common-paths.txt{Colors.END}")
        print(f"{Colors.CYAN}📊 Total paths: {total_paths}{Colors.END}")
        
        # Show first 10 paths
        print(f"\n{Colors.BOLD}First 10 paths in wordlist:{Colors.END}")
        with open("common-paths.txt", "r") as f:
            for i, line in enumerate(f):
                if i >= 10:
                    break
                if line.strip() and not line.startswith('#'):
                    print(f"  {i+1:2d}. {line.strip()}")
        
        print(f"  ... and {total_paths - 10} more paths")
        
    except Exception as e:
        print(f"{Colors.RED}❌ Error reading wordlist: {e}{Colors.END}")

def demo_features():
    """Demo key features"""
    print(f"\n{Colors.BOLD}⭐ KEY FEATURES SHOWCASE{Colors.END}")
    
    features = [
        "🔥 50+ Advanced Bypass Techniques",
        "🚀 Multi-threaded Concurrent Testing",
        "📊 Comprehensive JSON Reporting",
        "🕰️  Wayback Machine Integration",
        "🎨 Colorized Output for Easy Reading",
        "🔧 Both Python and Bash Implementations",
        "📁 Batch Testing with Custom Wordlists",
        "⚡ Configurable Timeouts and Thread Counts",
        "🛡️  Safe Testing with Error Handling",
        "📈 Progress Tracking and Statistics"
    ]
    
    for feature in features:
        print(f"  {feature}")
        time.sleep(0.2)

def demo_bypass_techniques():
    """Demo bypass technique categories"""
    print(f"\n{Colors.BOLD}🎯 BYPASS TECHNIQUE CATEGORIES{Colors.END}")
    
    categories = {
        "Path Manipulation": [
            "URL encoding variations",
            "Path traversal (../, ./)",
            "Case manipulation",
            "Special character injection",
            "File extension testing"
        ],
        "Header Injection": [
            "IP spoofing headers",
            "URL rewrite headers", 
            "Authorization bypasses",
            "CDN-specific headers",
            "Content-type manipulation"
        ],
        "HTTP Methods": [
            "Method variation testing",
            "Method override headers",
            "Content-Length manipulation"
        ],
        "Advanced Encoding": [
            "Unicode normalization",
            "Overlong UTF-8 encoding",
            "Double/triple URL encoding"
        ]
    }
    
    for category, techniques in categories.items():
        print(f"\n{Colors.CYAN}📂 {category}:{Colors.END}")
        for technique in techniques:
            print(f"  • {technique}")

def main():
    """Main demo function"""
    print_banner()
    
    # Check if we're in the right directory
    if not os.path.exists("legendary-403-bypass.py"):
        print(f"{Colors.RED}❌ Please run this demo from the tool directory{Colors.END}")
        sys.exit(1)
    
    print(f"{Colors.BOLD}Welcome to the Legendary 403 Bypass Tool Suite Demo!{Colors.END}")
    print(f"{Colors.YELLOW}This demo will showcase the capabilities of our bypass tools.{Colors.END}")
    
    try:
        # Demo sections
        demo_features()
        demo_bypass_techniques()
        demo_wordlist_info()
        demo_help_commands()
        
        # Ask user if they want to run a live test
        print(f"\n{Colors.BOLD}🔴 LIVE TESTING DEMO{Colors.END}")
        print(f"{Colors.YELLOW}Would you like to run a live test against httpbin.org?{Colors.END}")
        print(f"{Colors.CYAN}This is a safe testing target that simulates 403 responses.{Colors.END}")
        
        response = input(f"\n{Colors.BOLD}Run live test? (y/N): {Colors.END}").lower().strip()
        
        if response in ['y', 'yes']:
            demo_single_path_testing()
        else:
            print(f"{Colors.CYAN}Skipping live test demo.{Colors.END}")
        
        # Final message
        print(f"\n{Colors.BOLD}🎉 DEMO COMPLETE!{Colors.END}")
        print(f"{Colors.GREEN}✅ You've seen the Legendary 403 Bypass Tool Suite in action!{Colors.END}")
        print(f"\n{Colors.CYAN}Next steps:{Colors.END}")
        print(f"  1. Read the README_LEGENDARY.md for detailed usage")
        print(f"  2. Test against your authorized targets")
        print(f"  3. Customize wordlists for your specific needs")
        print(f"  4. Report any bugs or suggest improvements")
        
        print(f"\n{Colors.YELLOW}Remember: Always use these tools ethically and with proper authorization!{Colors.END}")
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Demo interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Demo error: {e}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()