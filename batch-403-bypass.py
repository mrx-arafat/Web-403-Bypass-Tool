#!/usr/bin/env python3
"""
Batch 403 Bypass Tool
Test multiple paths against a target using the legendary bypass techniques
Author: OpenHands AI Assistant
Version: 1.0
"""

import argparse
import sys
import time
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess
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

class BatchBypass:
    def __init__(self, target_url, wordlist_file, threads=5, timeout=10, output_dir="results"):
        self.target_url = target_url.rstrip('/')
        self.wordlist_file = wordlist_file
        self.threads = threads
        self.timeout = timeout
        self.output_dir = output_dir
        self.results = []
        
        # Create output directory
        Path(self.output_dir).mkdir(exist_ok=True)

    def print_banner(self):
        banner = f"""
{Colors.CYAN}
██████╗  █████╗ ████████╗ ██████╗██╗  ██╗    ██╗  ██╗ ██████╗ ██████╗ 
██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║  ██║    ██║  ██║██╔═████╗╚════██╗
██████╔╝███████║   ██║   ██║     ███████║    ███████║██║██╔██║ █████╔╝
██╔══██╗██╔══██║   ██║   ██║     ██╔══██║    ╚════██║████╔╝██║ ╚═══██╗
██████╔╝██║  ██║   ██║   ╚██████╗██║  ██║         ██║╚██████╔╝██████╔╝
╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝         ╚═╝ ╚═════╝ ╚═════╝ 
{Colors.END}
{Colors.YELLOW}                    BATCH 403 BYPASS TOOL{Colors.END}
{Colors.GREEN}              Test Multiple Paths Simultaneously{Colors.END}
        """
        print(banner)

    def load_wordlist(self):
        """Load paths from wordlist file"""
        try:
            with open(self.wordlist_file, 'r') as f:
                paths = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            print(f"{Colors.GREEN}✅ Loaded {len(paths)} paths from {self.wordlist_file}{Colors.END}")
            return paths
        except FileNotFoundError:
            print(f"{Colors.RED}❌ Wordlist file not found: {self.wordlist_file}{Colors.END}")
            sys.exit(1)
        except Exception as e:
            print(f"{Colors.RED}❌ Error loading wordlist: {e}{Colors.END}")
            sys.exit(1)

    def test_single_path(self, path):
        """Test a single path using the legendary bypass script"""
        try:
            # Get the directory of this script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            bypass_script = os.path.join(script_dir, "legendary-403-bypass.py")
            
            # Check if the Python script exists, otherwise use the bash version
            if not os.path.exists(bypass_script):
                bypass_script = os.path.join(script_dir, "legendary-403-bypass.sh")
                cmd = ["bash", bypass_script, self.target_url, path, "--timeout", str(self.timeout)]
            else:
                cmd = ["python3", bypass_script, self.target_url, path, "--timeout", str(self.timeout)]
            
            # Run the bypass script
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout * 10  # Give extra time for the script to complete
            )
            
            # Parse output to find successful bypasses
            successful_bypasses = []
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if '✅' in line and '[200]' in line:
                        successful_bypasses.append(line.strip())
            
            return {
                'path': path,
                'successful_bypasses': successful_bypasses,
                'total_output': result.stdout,
                'error': result.stderr if result.returncode != 0 else None
            }
            
        except subprocess.TimeoutExpired:
            return {
                'path': path,
                'successful_bypasses': [],
                'total_output': '',
                'error': 'Timeout expired'
            }
        except Exception as e:
            return {
                'path': path,
                'successful_bypasses': [],
                'total_output': '',
                'error': str(e)
            }

    def run_batch_tests(self):
        """Run bypass tests on all paths"""
        paths = self.load_wordlist()
        
        print(f"\n{Colors.BOLD}🚀 Starting batch bypass tests{Colors.END}")
        print(f"{Colors.BOLD}🎯 Target: {Colors.CYAN}{self.target_url}{Colors.END}")
        print(f"{Colors.BOLD}📋 Paths to test: {len(paths)}{Colors.END}")
        print(f"{Colors.BOLD}⚡ Threads: {self.threads}{Colors.END}")
        print(f"{Colors.BOLD}⏱️  Timeout per path: {self.timeout}s{Colors.END}\n")
        
        successful_paths = []
        completed = 0
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            future_to_path = {executor.submit(self.test_single_path, path): path for path in paths}
            
            for future in as_completed(future_to_path):
                path = future_to_path[future]
                completed += 1
                
                try:
                    result = future.result()
                    self.results.append(result)
                    
                    if result['successful_bypasses']:
                        successful_paths.append(result)
                        print(f"{Colors.GREEN}✅ [{completed:3d}/{len(paths)}] {path} - {len(result['successful_bypasses'])} bypass(es) found!{Colors.END}")
                        
                        # Save individual result
                        self.save_individual_result(result)
                    else:
                        print(f"{Colors.RED}❌ [{completed:3d}/{len(paths)}] {path} - No bypasses found{Colors.END}")
                        
                    if result['error']:
                        print(f"{Colors.YELLOW}⚠️  Error for {path}: {result['error']}{Colors.END}")
                        
                except Exception as e:
                    print(f"{Colors.RED}❌ [{completed:3d}/{len(paths)}] {path} - Exception: {e}{Colors.END}")
        
        return successful_paths

    def save_individual_result(self, result):
        """Save individual successful result to file"""
        if result['successful_bypasses']:
            filename = f"{self.output_dir}/bypass_{result['path'].replace('/', '_').replace('.', '_')}.txt"
            with open(filename, 'w') as f:
                f.write(f"Target: {self.target_url}/{result['path']}\n")
                f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                f.write("SUCCESSFUL BYPASSES:\n")
                f.write("-" * 40 + "\n")
                for bypass in result['successful_bypasses']:
                    f.write(f"{bypass}\n")
                f.write("\n" + "=" * 80 + "\n\n")
                f.write("FULL OUTPUT:\n")
                f.write("-" * 40 + "\n")
                f.write(result['total_output'])

    def generate_summary_report(self, successful_paths):
        """Generate summary report"""
        print(f"\n{Colors.BOLD}📊 BATCH BYPASS SUMMARY{Colors.END}")
        print("=" * 80)
        
        total_paths = len(self.results)
        successful_count = len(successful_paths)
        failed_count = total_paths - successful_count
        
        print(f"{Colors.BOLD}Target:{Colors.END} {self.target_url}")
        print(f"{Colors.BOLD}Total Paths Tested:{Colors.END} {total_paths}")
        print(f"{Colors.GREEN}✅ Paths with Bypasses:{Colors.END} {successful_count}")
        print(f"{Colors.RED}❌ Paths without Bypasses:{Colors.END} {failed_count}")
        
        if successful_paths:
            print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 SUCCESSFUL PATHS:{Colors.END}")
            print("-" * 80)
            for i, result in enumerate(successful_paths, 1):
                print(f"{Colors.GREEN}{i:2d}. /{result['path']} - {len(result['successful_bypasses'])} bypass(es){Colors.END}")
        
        # Save summary to JSON
        summary_file = f"{self.output_dir}/batch_summary.json"
        summary_data = {
            'target': self.target_url,
            'timestamp': time.time(),
            'total_paths': total_paths,
            'successful_paths': successful_count,
            'failed_paths': failed_count,
            'successful_results': [
                {
                    'path': result['path'],
                    'bypass_count': len(result['successful_bypasses']),
                    'bypasses': result['successful_bypasses']
                }
                for result in successful_paths
            ]
        }
        
        with open(summary_file, 'w') as f:
            json.dump(summary_data, f, indent=2)
        
        print(f"\n{Colors.CYAN}💾 Summary saved to: {summary_file}{Colors.END}")
        print(f"{Colors.CYAN}💾 Individual results saved to: {self.output_dir}/bypass_*.txt{Colors.END}")

def main():
    parser = argparse.ArgumentParser(
        description="Batch 403 Bypass Tool - Test multiple paths simultaneously",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 batch-403-bypass.py https://example.com common-paths.txt
  python3 batch-403-bypass.py https://example.com wordlist.txt --threads 10 --timeout 15
  python3 batch-403-bypass.py https://example.com paths.txt --output results_dir
        """
    )
    
    parser.add_argument('url', help='Target URL (e.g., https://example.com)')
    parser.add_argument('wordlist', help='Path to wordlist file')
    parser.add_argument('--threads', '-t', type=int, default=5, help='Number of threads (default: 5)')
    parser.add_argument('--timeout', '-T', type=int, default=10, help='Timeout per path in seconds (default: 10)')
    parser.add_argument('--output', '-o', default='results', help='Output directory (default: results)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not os.path.exists(args.wordlist):
        print(f"{Colors.RED}❌ Wordlist file not found: {args.wordlist}{Colors.END}")
        sys.exit(1)
    
    if args.threads < 1 or args.threads > 20:
        print(f"{Colors.RED}❌ Thread count must be between 1 and 20{Colors.END}")
        sys.exit(1)
    
    if args.timeout < 5 or args.timeout > 60:
        print(f"{Colors.RED}❌ Timeout must be between 5 and 60 seconds{Colors.END}")
        sys.exit(1)
    
    # Initialize batch bypass tool
    batch_tool = BatchBypass(
        target_url=args.url,
        wordlist_file=args.wordlist,
        threads=args.threads,
        timeout=args.timeout,
        output_dir=args.output
    )
    
    # Print banner
    batch_tool.print_banner()
    
    try:
        # Run batch tests
        successful_paths = batch_tool.run_batch_tests()
        
        # Generate summary report
        batch_tool.generate_summary_report(successful_paths)
        
        if successful_paths:
            print(f"\n{Colors.BOLD}{Colors.GREEN}🎯 Found bypasses for {len(successful_paths)} path(s)!{Colors.END}")
        else:
            print(f"\n{Colors.BOLD}{Colors.YELLOW}😞 No successful bypasses found across all tested paths.{Colors.END}")
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Unexpected error: {e}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()