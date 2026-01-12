"""
SQL Validator Module
Validates and sanitizes SQL queries to prevent dangerous operations.
"""

import sqlparse
import re
import logging
from typing import Tuple, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SQLValidator:
    """Validates SQL queries for safety and correctness."""

    # Dangerous SQL keywords that should not be allowed
    FORBIDDEN_KEYWORDS = [
        'DROP', 'DELETE', 'TRUNCATE', 'INSERT', 'UPDATE',
        'ALTER', 'CREATE', 'REPLACE', 'EXEC', 'EXECUTE'
    ]

    def __init__(self):
        """Initialize the SQL validator."""
        pass

    def validate(self, sql: str) -> Tuple[bool, str]:
        """
        Validate a SQL query for safety and correctness.

        Args:
            sql: The SQL query string to validate

        Returns:
            Tuple of (is_valid, error_message)
            If valid, error_message will be empty string
        """
        # Check for empty query
        if not sql or not sql.strip():
            return False, "Empty SQL query"

        # Check for forbidden keywords
        is_safe, error = self._check_forbidden_keywords(sql)
        if not is_safe:
            return False, error

        # Check SQL syntax
        is_valid_syntax, syntax_error = self._check_syntax(sql)
        if not is_valid_syntax:
            return False, syntax_error

        # All checks passed
        return True, ""

    def _check_forbidden_keywords(self, sql: str) -> Tuple[bool, str]:
        """
        Check if SQL contains any forbidden keywords.

        Args:
            sql: SQL query string

        Returns:
            Tuple of (is_safe, error_message)
        """
        sql_upper = sql.upper()

        for keyword in self.FORBIDDEN_KEYWORDS:
            # Use word boundaries to avoid false positives
            # (e.g., "DELETED" column name shouldn't trigger "DELETE")
            pattern = r'\b' + keyword + r'\b'
            if re.search(pattern, sql_upper):
                return False, f"Forbidden SQL keyword detected: {keyword}"

        return True, ""

    def _check_syntax(self, sql: str) -> Tuple[bool, str]:
        """
        Check if SQL has valid syntax using sqlparse.

        Args:
            sql: SQL query string

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Parse the SQL
            parsed = sqlparse.parse(sql)

            if not parsed:
                return False, "Could not parse SQL query"

            # Check that we have exactly one statement
            if len(parsed) > 1:
                return False, "Multiple SQL statements detected. Only single SELECT queries are allowed."

            # Get the first statement
            statement = parsed[0]

            # Check that it's a SELECT statement
            if not self._is_select_statement(statement):
                return False, "Only SELECT queries are allowed"

            return True, ""

        except Exception as e:
            return False, f"SQL syntax error: {str(e)}"

    def _is_select_statement(self, statement) -> bool:
        """
        Check if a parsed statement is a SELECT query.

        Args:
            statement: Parsed SQL statement from sqlparse

        Returns:
            True if it's a SELECT statement
        """
        # Get the first meaningful token
        first_token = None
        for token in statement.tokens:
            if not token.is_whitespace:
                first_token = token
                break

        if first_token is None:
            return False

        # Check if it's SELECT or WITH (for CTEs)
        token_value = str(first_token).upper().strip()
        return token_value in ['SELECT', 'WITH']

    def extract_sql_from_response(self, llm_response: str) -> str:
        """
        Extract SQL code from LLM response (handles markdown code blocks).

        Args:
            llm_response: The raw response from the LLM

        Returns:
            Extracted SQL query string
        """
        # Try to extract from markdown code block first
        sql_pattern = r'```sql\s*(.*?)\s*```'
        match = re.search(sql_pattern, llm_response, re.DOTALL | re.IGNORECASE)

        if match:
            return match.group(1).strip()

        # Try generic code block
        code_pattern = r'```\s*(.*?)\s*```'
        match = re.search(code_pattern, llm_response, re.DOTALL)

        if match:
            return match.group(1).strip()

        # If no code blocks, try to find SELECT statement
        lines = llm_response.split('\n')
        sql_lines = []
        in_sql = False

        for line in lines:
            line_upper = line.strip().upper()
            if line_upper.startswith('SELECT') or line_upper.startswith('WITH'):
                in_sql = True

            if in_sql:
                sql_lines.append(line)

                # Stop at semicolon or empty line after SQL started
                if ';' in line:
                    break

        if sql_lines:
            return '\n'.join(sql_lines).strip()

        # Last resort: return the whole response
        return llm_response.strip()
