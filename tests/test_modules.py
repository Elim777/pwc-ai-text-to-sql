"""
Module Unit Tests
Tests individual modules in isolation.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from data_loader import DataLoader
from query_handler import QueryHandler
from sql_validator import SQLValidator


def test_data_loader():
    """Test DataLoader module"""

    print("=== TESTING DATA LOADER MODULE ===\n")

    # Initialize and load data
    print("1. Testing data loading...")
    loader = DataLoader('Data Dump - Accrual Accounts.xlsx')
    loader.load_data()

    assert loader.df is not None, "DataFrame is None"
    assert len(loader.df) == 13152, f"Expected 13152 rows, got {len(loader.df)}"
    assert len(loader.df.columns) == 18, f"Expected 18 columns, got {len(loader.df.columns)}"
    print(f"   ✓ Loaded {len(loader.df)} rows, {len(loader.df.columns)} columns\n")

    # Test schema generation
    print("2. Testing schema generation...")
    schema = loader.get_schema_description()

    assert len(schema) > 0, "Schema description is empty"
    assert 'accrual_accounts' in schema, "Table name not in schema"
    assert 'Currency' in schema, "Column names not in schema"
    print(f"   ✓ Generated schema ({len(schema)} chars)\n")

    # Test column list
    print("3. Testing column list...")
    columns = loader.get_column_list()

    assert len(columns) == 18, f"Expected 18 columns, got {len(columns)}"
    assert 'Currency' in columns, "Currency column missing"
    assert 'Transaction_Value' in columns, "Transaction_Value column missing"
    print(f"   ✓ Got {len(columns)} columns\n")

    # Test data summary
    print("4. Testing data summary...")
    summary = loader.get_data_summary()

    assert 'row_count' in summary, "row_count missing from summary"
    assert summary['row_count'] == 13152, "Incorrect row count in summary"
    assert 'columns' in summary, "columns missing from summary"
    print(f"   ✓ Summary generated with {len(summary)} keys\n")

    print("✅ DATA LOADER TESTS PASSED\n")
    return True


def test_query_handler():
    """Test QueryHandler module"""

    print("=== TESTING QUERY HANDLER MODULE ===\n")

    qh = QueryHandler()

    # Test prompt building
    print("1. Testing prompt building...")
    schema = "Table: test_table\nColumns: id, name, value"
    question = "How many records are there?"

    prompts = qh.build_prompt(question, schema)

    assert 'system' in prompts, "system prompt missing"
    assert 'user' in prompts, "user prompt missing"
    assert len(prompts['system']) > 0, "system prompt is empty"
    assert len(prompts['user']) > 0, "user prompt is empty"
    assert question in prompts['user'], "Question not in user prompt"
    assert schema in prompts['user'], "Schema not in user prompt"
    print("   ✓ Prompt built successfully\n")

    # Test correction prompt
    print("2. Testing correction prompt...")
    failed_sql = "SELECT COUNT(*) FROM wrong_table;"
    error_msg = "Table 'wrong_table' does not exist"

    correction = qh.build_correction_prompt(question, schema, failed_sql, error_msg)

    assert 'system' in correction, "system prompt missing in correction"
    assert 'user' in correction, "user prompt missing in correction"
    assert failed_sql in correction['user'], "Failed SQL not in correction prompt"
    assert error_msg in correction['user'], "Error message not in correction prompt"
    print("   ✓ Correction prompt built successfully\n")

    print("✅ QUERY HANDLER TESTS PASSED\n")
    return True


def test_sql_validator():
    """Test SQLValidator module"""

    print("=== TESTING SQL VALIDATOR MODULE ===\n")

    validator = SQLValidator()

    # Test valid SELECT query
    print("1. Testing valid SELECT query...")
    sql = "SELECT COUNT(*) FROM accrual_accounts;"
    is_valid, error = validator.validate(sql)

    assert is_valid, f"Valid query marked as invalid: {error}"
    print("   ✓ Valid SELECT query accepted\n")

    # Test forbidden keyword
    print("2. Testing forbidden keyword detection...")
    sql = "DROP TABLE accrual_accounts;"
    is_valid, error = validator.validate(sql)

    assert not is_valid, "DROP query not blocked"
    assert 'DROP' in error, "Error message doesn't mention DROP"
    print(f"   ✓ DROP query blocked: {error}\n")

    # Test multiple statements
    print("3. Testing multiple statement detection...")
    sql = "SELECT * FROM accrual_accounts; SELECT * FROM users;"
    is_valid, error = validator.validate(sql)

    assert not is_valid, "Multiple statements not blocked"
    print(f"   ✓ Multiple statements blocked: {error}\n")

    # Test SQL extraction
    print("4. Testing SQL extraction...")
    response = """```sql
SELECT COUNT(*) FROM test;
```

Explanation: This counts records."""

    extracted = validator.extract_sql_from_response(response)

    assert 'SELECT COUNT(*)' in extracted, "SQL not extracted correctly"
    assert '```' not in extracted, "Code block markers not removed"
    print(f"   ✓ SQL extracted: {extracted}\n")

    print("✅ SQL VALIDATOR TESTS PASSED\n")
    return True


if __name__ == '__main__':
    try:
        print("="*60)
        print("RUNNING MODULE UNIT TESTS")
        print("="*60 + "\n")

        test_data_loader()
        test_query_handler()
        test_sql_validator()

        print("="*60)
        print("✅ ALL MODULE TESTS PASSED")
        print("="*60)
        sys.exit(0)

    except AssertionError as e:
        print(f'\n❌ MODULE TEST FAILED: {e}')
        sys.exit(1)
    except Exception as e:
        print(f'\n❌ ERROR: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)
