"""
Integration Test - End-to-End Flow
Tests the complete application flow from question to result.
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


def test_end_to_end_flow():
    """Test complete flow: Question → SQL → Execution → Results"""

    print('=== INTEGRATION TEST: END-TO-END FLOW ===\n')

    # 1. Load data
    print('1. Loading data...')
    loader = DataLoader('Data Dump - Accrual Accounts.xlsx')
    loader.load_data()
    assert len(loader.df) == 13152, "Data not loaded correctly"
    print(f'   ✓ Loaded {len(loader.df)} rows\n')

    # 2. Get schema
    print('2. Getting schema...')
    schema = loader.get_schema_description()
    assert len(schema) > 0, "Schema is empty"
    print(f'   ✓ Schema: {len(schema)} chars\n')

    # 3. Build prompt
    print('3. Building prompt...')
    qh = QueryHandler()
    question = 'How many records are there in total?'
    prompts = qh.build_prompt(question, schema)
    assert 'system' in prompts and 'user' in prompts, "Prompt structure invalid"
    print(f'   ✓ Prompt built for: {question}\n')

    # 4. Call LLM
    print('4. Calling OpenAI API...')
    llm = LLMService()
    response = llm.generate_sql_with_retry(prompts)
    assert len(response) > 0, "LLM returned empty response"
    print(f'   ✓ Got response ({len(response)} chars)')
    print(f'   Response preview: {response[:200]}...\n')

    # 5. Extract and validate SQL
    print('5. Validating SQL...')
    validator = SQLValidator()
    sql = validator.extract_sql_from_response(response)
    print(f'   Extracted SQL: {sql}')

    is_valid, error = validator.validate(sql)
    assert is_valid, f"SQL validation failed: {error}"
    print(f'   ✓ SQL is valid\n')

    # 6. Execute query
    print('6. Executing query...')
    locals_dict = {loader.table_name: loader.df}
    result = ps.sqldf(sql, locals_dict)
    assert len(result) > 0, "Query returned no results"
    print(f'   ✓ Query executed successfully')
    print(f'   Result:\n{result}\n')

    # Verify result
    assert result.iloc[0, 0] == 13152, "Result count doesn't match expected"

    print('=== ✅ ALL INTEGRATION TESTS PASSED ===')
    return True


if __name__ == '__main__':
    try:
        test_end_to_end_flow()
        sys.exit(0)
    except AssertionError as e:
        print(f'\n❌ TEST FAILED: {e}')
        sys.exit(1)
    except Exception as e:
        print(f'\n❌ ERROR: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)
