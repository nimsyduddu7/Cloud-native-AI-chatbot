#!/bin/bash

# Test script for API endpoints

BASE_URL="http://localhost:8000"
SESSION_ID="test-session-$(date +%s)"

echo "🧪 Testing AI Chatbot API..."
echo ""

# Test health endpoint
echo "1. Testing health endpoint..."
curl -s "$BASE_URL/health" | jq '.' || echo "❌ Health check failed"
echo ""

# Test chat endpoint
echo "2. Testing chat endpoint..."
curl -s -X POST "$BASE_URL/chat" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": \"Hello, how are you?\",
    \"session_id\": \"$SESSION_ID\",
    \"model\": \"gpt-3.5-turbo\"
  }" | jq '.' || echo "❌ Chat endpoint failed"
echo ""

# Test history endpoint
echo "3. Testing history endpoint..."
curl -s "$BASE_URL/sessions/$SESSION_ID/history" | jq '.' || echo "❌ History endpoint failed"
echo ""

# Test metrics endpoint
echo "4. Testing metrics endpoint..."
curl -s "$BASE_URL/metrics" | head -20 || echo "❌ Metrics endpoint failed"
echo ""

echo "✅ API tests complete!"
