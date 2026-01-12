"""
Security Validation Tests
Tests SQL validation and security measures.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from sql_validator import SQLValidator


def test_dangerous_sql_blocked():
    """Test that dangerous SQL commands are blocked"""

    print("=== TESTING SECURITY VALIDATION ===\n")

    validator = SQLValidator()

    # Test dangerous SQL commands that should be BLOCKED
    dangerous_queries = [
        ("DROP TABLE accrual_accounts;", "DROP command"),
        ("DELETE FROM accrual_accounts WHERE Currency = 'USD';", "DELETE command"),
        ("UPDATE accrual_accounts SET Currency = 'EUR';", "UPDATE command"),
        ("INSERT INTO accrual_accounts VALUES (1, 2, 3);", "INSERT command"),
        ("TRUNCATE TABLE accrual_accounts;", "TRUNCATE command"),
        ("ALTER TABLE accrual_accounts ADD COLUMN test VARCHAR(50);", "ALTER command"),
        ("CREATE TABLE users (id INT);", "CREATE command"),
        ("SELECT * FROM accrual_accounts; DROP TABLE users;", "SQL injection attempt"),
        ("SELECT * FROM accrual_accounts WHERE 1=1; DELETE FROM users;", "Chained injection"),
    ]

    print("--- Testing Dangerous Queries (Should be BLOCKED) ---\n")

    blocked_count = 0
    failed_to_block = []

    for sql, description in dangerous_queries:
        is_valid, error = validator.validate(sql)

        if not is_valid:
            # Successfully blocked
            print(f"✓ BLOCKED: {description}")
            print(f"  SQL: {sql[:60]}...")
            print(f"  Reason: {error}\n")
            blocked_count += 1
        else:
            # FAILED to block - this is a security issue!
            print(f"✗ ALLOWED (SECURITY ISSUE!): {description}")
            print(f"  SQL: {sql[:60]}...\n")
            failed_to_block.append((description, sql))

    # Test safe queries that should be ALLOWED
    print("\n--- Testing Safe Queries (Should be ALLOWED) ---\n")

    safe_queries = [
        ("SELECT COUNT(*) FROM accrual_accounts;", "Simple COUNT"),
        ("SELECT Currency, COUNT(*) FROM accrual_accounts GROUP BY Currency;", "GROUP BY"),
        ("SELECT * FROM accrual_accounts WHERE Currency = 'USD' LIMIT 10;", "WHERE with LIMIT"),
        ("WITH temp AS (SELECT * FROM accrual_accounts) SELECT * FROM temp LIMIT 10;", "CTE (Common Table Expression)"),
        ("SELECT DISTINCT Currency FROM accrual_accounts;", "DISTINCT"),
        ("SELECT AVG(Transaction_Value) FROM accrual_accounts;", "Aggregate function"),
    ]

    allowed_count = 0
    failed_to_allow = []

    for sql, description in safe_queries:
        is_valid, error = validator.validate(sql)

        if is_valid:
            # Successfully allowed
            print(f"✓ ALLOWED: {description}")
            print(f"  SQL: {sql[:60]}...\n")
            allowed_count += 1
        else:
            # FAILED to allow - false positive
            print(f"✗ BLOCKED (FALSE POSITIVE!): {description}")
            print(f"  SQL: {sql[:60]}...")
            print(f"  Reason: {error}\n")
            failed_to_allow.append((description, sql, error))

    # Summary
    print("=== SECURITY TEST SUMMARY ===")
    print(f"Dangerous queries blocked: {blocked_count}/{len(dangerous_queries)}")
    print(f"Safe queries allowed: {allowed_count}/{len(safe_queries)}")

    if failed_to_block:
        print(f"\n❌ SECURITY FAILURES ({len(failed_to_block)}):")
        for desc, sql in failed_to_block:
            print(f"  - {desc}: {sql[:50]}...")

    if failed_to_allow:
        print(f"\n⚠️  FALSE POSITIVES ({len(failed_to_allow)}):")
        for desc, sql, error in failed_to_allow:
            print(f"  - {desc}: {error}")

    # Assertions
    assert len(failed_to_block) == 0, f"Security failure: {len(failed_to_block)} dangerous queries were not blocked"
    assert len(failed_to_allow) == 0, f"Usability issue: {len(failed_to_allow)} safe queries were incorrectly blocked"

    print("\n✅ ALL SECURITY TESTS PASSED")
    return True


def test_sql_extraction():
    """Test SQL extraction from various response formats"""

    print("\n=== TESTING SQL EXTRACTION ===\n")

    validator = SQLValidator()

    test_cases = [
        # Markdown code block with sql tag
        ("""```sql
SELECT COUNT(*) FROM accrual_accounts;
```

Explanation: This counts all records.""",
         "SELECT COUNT(*) FROM accrual_accounts;"),

        # Generic code block
        ("""```
SELECT * FROM accrual_accounts LIMIT 5;
```""",
         "SELECT * FROM accrual_accounts LIMIT 5;"),

        # Plain SQL without code block
        ("""Here's the query:

SELECT DISTINCT Currency FROM accrual_accounts;

This will show unique currencies.""",
         "SELECT DISTINCT Currency FROM accrual_accounts;"),

        # SQL with semicolon
        ("""SELECT AVG(Transaction_Value) FROM accrual_accounts;""",
         "SELECT AVG(Transaction_Value) FROM accrual_accounts;"),
    ]

    passed = 0
    for i, (response, expected_sql) in enumerate(test_cases, 1):
        extracted = validator.extract_sql_from_response(response)
        extracted_clean = extracted.strip().rstrip(';')
        expected_clean = expected_sql.strip().rstrip(';')

        if extracted_clean == expected_clean:
            print(f"✓ Test {i}: Extraction successful")
            passed += 1
        else:
            print(f"✗ Test {i}: Extraction failed")
            print(f"  Expected: {expected_clean}")
            print(f"  Got: {extracted_clean}")

    print(f"\nExtraction tests: {passed}/{len(test_cases)} passed")

    assert passed == len(test_cases), "SQL extraction tests failed"

    print("✅ SQL EXTRACTION TESTS PASSED")
    return True


if __name__ == '__main__':
    try:
        test_dangerous_sql_blocked()
        test_sql_extraction()
        print("\n" + "="*50)
        print("✅ ALL SECURITY TESTS PASSED")
        print("="*50)
        sys.exit(0)
    except AssertionError as e:
        print(f'\n❌ SECURITY TEST FAILED: {e}')
        sys.exit(1)
    except Exception as e:
        print(f'\n❌ ERROR: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)
