# 📋 Test Manifest

Complete listing of all tests in the test suite.

## Test Files Overview

| File | Type | API Required | Duration | Tests | Status |
|------|------|--------------|----------|-------|--------|
| `quick_test.py` | Health Check | No | ~1s | 8 | ✅ |
| `test_modules.py` | Unit | No | ~0.8s | 10 | ✅ |
| `test_security.py` | Security | No | ~0.3s | 19 | ✅ |
| `test_integration.py` | Integration | Yes | ~1.8s | 1 | ✅ |
| `test_question_types.py` | Functional | Yes | ~4.2s | 3 | ✅ |
| **TOTAL** | | | **~8.2s** | **41** | ✅ |

## Detailed Test Inventory

### quick_test.py (8 tests)

**Quick Health Check - No API calls required**

1. ✅ Import validation
2. ✅ Data loading (13,152 rows)
3. ✅ Schema generation (1,639 chars)
4. ✅ Prompt building
5. ✅ SQL validation (safe query)
6. ✅ SQL validation (dangerous query)
7. ✅ SQL extraction
8. ✅ PandasSQL execution

---

### test_modules.py (10 tests)

**Unit Tests - Module isolation**

#### DataLoader Module (4 tests)
1. ✅ Load Excel data
2. ✅ Generate schema description
3. ✅ Get column list
4. ✅ Create data summary

#### QueryHandler Module (2 tests)
5. ✅ Build prompt
6. ✅ Build correction prompt

#### SQLValidator Module (4 tests)
7. ✅ Validate safe SELECT query
8. ✅ Block forbidden keywords
9. ✅ Detect multiple statements
10. ✅ Extract SQL from response

---

### test_security.py (19 tests)

**Security Validation - SQL injection & dangerous commands**

#### Dangerous Queries Blocked (9 tests)
1. ✅ Block DROP TABLE
2. ✅ Block DELETE FROM
3. ✅ Block UPDATE SET
4. ✅ Block INSERT INTO
5. ✅ Block TRUNCATE TABLE
6. ✅ Block ALTER TABLE
7. ✅ Block CREATE TABLE
8. ✅ Block SQL injection (SELECT; DROP)
9. ✅ Block chained injection (WHERE; DELETE)

#### Safe Queries Allowed (6 tests)
10. ✅ Allow simple COUNT
11. ✅ Allow GROUP BY
12. ✅ Allow WHERE with LIMIT
13. ✅ Allow CTE (WITH statement)
14. ✅ Allow DISTINCT
15. ✅ Allow aggregate functions

#### SQL Extraction (4 tests)
16. ✅ Extract from markdown ```sql block
17. ✅ Extract from generic ``` block
18. ✅ Extract plain SQL
19. ✅ Extract SQL with semicolon

---

### test_integration.py (1 test)

**End-to-End Integration - Requires OpenAI API**

1. ✅ Complete flow test
   - Data loading
   - Schema generation
   - Prompt building
   - OpenAI API call
   - SQL validation
   - Query execution
   - Result verification

---

### test_question_types.py (3 tests)

**Functional Tests - Various question types - Requires OpenAI API**

1. ✅ DISTINCT query
   - Question: "What are the unique currencies?"
   - Expected: 2 rows (USD, CAD)

2. ✅ COUNT with WHERE
   - Question: "How many USD transactions?"
   - Expected: 13,102 count

3. ✅ ORDER BY with LIMIT
   - Question: "Top 5 highest values?"
   - Expected: 5 rows, descending order

---

## Test Coverage Matrix

### By Module

| Module | Unit Tests | Integration Tests | Security Tests | Total |
|--------|-----------|-------------------|----------------|-------|
| data_loader.py | 4 | 1 | 0 | 5 |
| query_handler.py | 2 | 1 | 0 | 3 |
| sql_validator.py | 4 | 1 | 19 | 24 |
| llm_service.py | 0 | 4 | 0 | 4 |
| app.py | 1 | 0 | 0 | 1 |
| **TOTAL** | **11** | **7** | **19** | **37** |

### By Test Type

| Type | Count | Percentage |
|------|-------|------------|
| Unit Tests | 10 | 27% |
| Security Tests | 19 | 51% |
| Integration Tests | 4 | 11% |
| Health Checks | 8 | 22% |
| **TOTAL** | **41** | **100%** |

### By API Requirement

| API Required | Tests | Percentage | Duration |
|--------------|-------|------------|----------|
| No | 37 | 90% | ~2.1s |
| Yes | 4 | 10% | ~6.0s |
| **TOTAL** | **41** | **100%** | **~8.1s** |

---

## Test Execution Strategies

### 1. Quick Validation (1 second)
```bash
./tests/quick_test.py
```
**Use when:** Before commits, quick sanity check

### 2. Offline Testing (2 seconds)
```bash
python tests/test_modules.py
python tests/test_security.py
```
**Use when:** No internet, working offline

### 3. Full Suite (8 seconds)
```bash
./tests/run_all_tests.sh
```
**Use when:** Before deployment, comprehensive validation

### 4. Integration Only (6 seconds)
```bash
python tests/test_integration.py
python tests/test_question_types.py
```
**Use when:** Testing OpenAI integration specifically

---

## Success Criteria

### For Passing
- ✅ All 41 tests must pass
- ✅ No security vulnerabilities detected
- ✅ SQL accuracy 100%
- ✅ All dangerous queries blocked
- ✅ All safe queries allowed

### For Production Readiness
- ✅ All tests passing
- ✅ Test coverage >80%
- ✅ Security tests 100% pass rate
- ✅ Integration tests stable
- ✅ Performance within targets (<3s E2E)

---

## Maintenance

### Adding New Tests

1. **Unit Test:** Add to `test_modules.py`
2. **Security Test:** Add to `test_security.py`
3. **Integration Test:** Add to `test_integration.py`
4. **New Feature:** Create new `test_feature.py`
5. **Update:** This manifest and `README.md`

### Test Naming Convention

```python
def test_<module>_<functionality>():
    """Test <what it does>"""
    # Arrange
    # Act
    # Assert
```

### Assertion Standards

```python
# Good
assert actual == expected, "Descriptive error message"

# Bad
assert actual == expected
```

---

**Manifest Version:** 1.0
**Last Updated:** January 10, 2026
**Total Tests:** 41
**Pass Rate:** 100%
**Status:** ✅ All Systems Operational
