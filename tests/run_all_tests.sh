#!/bin/bash

# Run All Tests Script
# Executes all test files in the correct order

echo "================================================"
echo "🧪 RUNNING COMPLETE TEST SUITE"
echo "================================================"
echo ""

# Change to project root directory
cd "$(dirname "$0")/.." || exit

# Activate virtual environment
source venv/bin/activate

# Track results
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to run a test
run_test() {
    local test_file=$1
    local test_name=$2

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📋 Running: $test_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    if python "$test_file"; then
        PASSED_TESTS=$((PASSED_TESTS + 1))
        echo ""
        echo "✅ $test_name PASSED"
    else
        FAILED_TESTS=$((FAILED_TESTS + 1))
        echo ""
        echo "❌ $test_name FAILED"
        return 1
    fi

    echo ""
}

# Run tests in order (fastest to slowest, API-free first)
echo "🔹 Phase 1: Unit Tests (No API required)"
echo ""

run_test "tests/test_modules.py" "Module Unit Tests" || true
run_test "tests/test_security.py" "Security Tests" || true

echo ""
echo "🔹 Phase 2: Integration Tests (Requires OpenAI API)"
echo ""

# Check if API key is set
if [ -z "$OPENAI_API_KEY" ] && ! grep -q "OPENAI_API_KEY" .env 2>/dev/null; then
    echo "⚠️  WARNING: OPENAI_API_KEY not found"
    echo "   Integration tests will be skipped"
    echo "   Set API key in .env file to run these tests"
    echo ""
else
    run_test "tests/test_integration.py" "Integration Test" || true
    run_test "tests/test_question_types.py" "Question Types Test" || true
fi

# Summary
echo ""
echo "================================================"
echo "📊 TEST SUMMARY"
echo "================================================"
echo ""
echo "Total Tests:  $TOTAL_TESTS"
echo "✅ Passed:     $PASSED_TESTS"
echo "❌ Failed:     $FAILED_TESTS"
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo "🎉 ALL TESTS PASSED!"
    echo "================================================"
    exit 0
else
    echo "⚠️  SOME TESTS FAILED"
    echo "================================================"
    exit 1
fi
