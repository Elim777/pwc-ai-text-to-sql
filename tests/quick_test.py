#!/usr/bin/env python3
"""
Quick Test - Fast validation of core functionality
Run this for a quick health check without API calls.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))


def quick_test():
    """Run quick tests without API calls"""

    print("🚀 QUICK TEST - Core Functionality Check\n")
    print("="*60)

    tests_passed = 0
    tests_total = 0

    # Test 1: Imports
    print("\n1️⃣  Testing imports...")
    tests_total += 1
    try:
        from data_loader import DataLoader
        from query_handler import QueryHandler
        from sql_validator import SQLValidator
        import pandas as pd
        import pandasql as ps
        print("   ✅ All imports successful")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Import failed: {e}")

    # Test 2: Data Loading
    print("\n2️⃣  Testing data loading...")
    tests_total += 1
    try:
        loader = DataLoader('Data Dump - Accrual Accounts.xlsx')
        loader.load_data()
        assert len(loader.df) == 13152
        print(f"   ✅ Data loaded: {len(loader.df)} rows")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Data loading failed: {e}")

    # Test 3: Schema Generation
    print("\n3️⃣  Testing schema generation...")
    tests_total += 1
    try:
        schema = loader.get_schema_description()
        assert len(schema) > 1000
        assert 'Currency' in schema
        print(f"   ✅ Schema generated: {len(schema)} chars")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Schema generation failed: {e}")

    # Test 4: Prompt Building
    print("\n4️⃣  Testing prompt builder...")
    tests_total += 1
    try:
        qh = QueryHandler()
        prompts = qh.build_prompt("Test question", schema)
        assert 'system' in prompts
        assert 'user' in prompts
        print("   ✅ Prompts built successfully")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Prompt building failed: {e}")

    # Test 5: SQL Validation (Safe query)
    print("\n5️⃣  Testing SQL validation (safe query)...")
    tests_total += 1
    try:
        validator = SQLValidator()
        is_valid, error = validator.validate("SELECT COUNT(*) FROM test;")
        assert is_valid
        print("   ✅ Safe query validated")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Validation failed: {e}")

    # Test 6: SQL Validation (dangerous query)
    print("\n6️⃣  Testing SQL validation (dangerous query)...")
    tests_total += 1
    try:
        is_valid, error = validator.validate("DROP TABLE test;")
        assert not is_valid
        assert 'DROP' in error
        print("   ✅ Dangerous query blocked")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Security check failed: {e}")

    # Test 7: SQL Extraction
    print("\n7️⃣  Testing SQL extraction...")
    tests_total += 1
    try:
        response = "```sql\nSELECT * FROM test;\n```"
        extracted = validator.extract_sql_from_response(response)
        assert 'SELECT' in extracted
        assert '```' not in extracted
        print("   ✅ SQL extracted correctly")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Extraction failed: {e}")

    # Test 8: PandasSQL
    print("\n8️⃣  Testing PandasSQL execution...")
    tests_total += 1
    try:
        sql = "SELECT COUNT(*) as total FROM accrual_accounts"
        locals_dict = {'accrual_accounts': loader.df}
        result = ps.sqldf(sql, locals_dict)
        assert len(result) == 1
        assert result.iloc[0, 0] == 13152
        print(f"   ✅ Query executed: {result.iloc[0, 0]} records")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Query execution failed: {e}")

    # Summary
    print("\n" + "="*60)
    print(f"📊 RESULTS: {tests_passed}/{tests_total} tests passed")
    print("="*60)

    if tests_passed == tests_total:
        print("\n✅ ALL QUICK TESTS PASSED")
        print("   Core functionality is working correctly")
        print("   Ready to run full test suite\n")
        return 0
    else:
        print(f"\n⚠️  {tests_total - tests_passed} TEST(S) FAILED")
        print("   Please fix issues before proceeding\n")
        return 1


if __name__ == '__main__':
    sys.exit(quick_test())
