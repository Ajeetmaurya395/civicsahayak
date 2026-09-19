#!/bin/bash
# Bootstrap OpenSearch index for CivicOS
# Creates the government_schemes index with proper mappings

OPENSEARCH_URL="${OPENSEARCH_URL:-http://localhost:9200}"
INDEX_NAME="government_schemes"
MAPPING_FILE="$(dirname "$0")/../mappings/schemes-index-mapping.json"

echo "Creating OpenSearch index: ${INDEX_NAME}"
echo "OpenSearch URL: ${OPENSEARCH_URL}"

# Check if OpenSearch is available
curl -s "${OPENSEARCH_URL}" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: OpenSearch is not available at ${OPENSEARCH_URL}"
    exit 1
fi

# Delete existing index if it exists
curl -s -X DELETE "${OPENSEARCH_URL}/${INDEX_NAME}" > /dev/null 2>&1

# Create index with mappings
curl -s -X PUT "${OPENSEARCH_URL}/${INDEX_NAME}" \
    -H "Content-Type: application/json" \
    -d @"${MAPPING_FILE}"

echo ""
echo "Index ${INDEX_NAME} created successfully."

# Verify
echo ""
echo "Verifying index..."
curl -s "${OPENSEARCH_URL}/${INDEX_NAME}/_mapping" | python3 -m json.tool 2>/dev/null || echo "(python3 not available for pretty printing)"

echo ""
echo "Done. OpenSearch is ready for CivicOS."
