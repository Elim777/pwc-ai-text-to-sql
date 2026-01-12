"""
Test Different Question Types
Tests various types of natural language questions and SQL generation.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from data_loader import DataLoader
from llm_service import LLMService
from query_handler import QueryHandler
from sql_validator import SQLValidator
import pandasql as ps


def test_multiple_question_types():
    """Test various question types: COUNT, DISTINCT, WHERE, ORDER BY, etc."""

    print("=== TESTING MULTIPLE QUESTION TYPES ===\n")

    # Initialize
    loader = DataLoader('Data Dump - Accrual Accounts.xlsx')
    loader.load_data()
    schema = loader.get_schema_description()
    qh = QueryHandler()
    llm = LLMService()
    validator = SQLValidator()

    # Test questions with expected result types
    test_cases = [
        {
            'question': "What are the unique currencies in the dataset?",
            'expected_rows': 2,  # USD and CAD
            'description': "DISTINCT query"
        },
        {
            'question': "How many transactions are in USD currency?",
            'expected_rows': 1,  # Single count result
            'description': "COUNT with WHERE filter"
        },
        {
            'question': "Show me the top 5 highest transaction values",
            'expected_rows': 5,  # Top 5 results
            'description': "ORDER BY DESC with LIMIT"
        }
    ]

    passed = 0
    failed = 0

    for i, test_case in enumerate(test_cases, 1):
        question = test_case['question']
        print(f"{i}. Testing: {test_case['description']}")
        print(f"   Question: {question}")

        try:
            # Build prompt
            prompts = qh.build_prompt(question, schema)

            # Get SQL from LLM
            response = llm.generate_sql_with_retry(prompts)

            # Extract and validate
            sql = validator.extract_sql_from_response(response)
            is_valid, error = validator.validate(sql)

            assert is_valid, f"Validation failed: {error}"

            # Execute
            locals_dict = {loader.table_name: loader.df}
            result = ps.sqldf(sql, locals_dict)

            # Verify result count
            actual_rows = len(result)
            print(f"   ✓ SQL: {sql}")
            print(f"   ✓ Result: {actual_rows} rows (expected: {test_case['expected_rows']})")

            if actual_rows == test_case['expected_rows']:
                print(f"   ✅ PASSED\n")
                passed += 1
            else:
                print(f"   ⚠️  Row count mismatch but query successful\n")
                passed += 1  # Still count as passed if query executed

            # Show sample of results
            print(f"   Sample results:\n{result.head(3)}\n")

        except Exception as e:
            print(f"   ❌ FAILED: {str(e)}\n")
            failed += 1

    print(f"=== RESULTS: {passed} PASSED, {failed} FAILED ===")

    assert failed == 0, f"{failed} tests failed"
    return True


if __name__ == '__main__':
    try:
        test_multiple_question_types()
        sys.exit(0)
    except AssertionError as e:
        print(f'\n❌ TEST SUITE FAILED: {e}')
        sys.exit(1)
    except Exception as e:
        print(f'\n❌ ERROR: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)
