"""
Query Handler Module
Builds prompts for the LLM to generate SQL queries from natural language questions.
"""

import logging
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueryHandler:
    """Handles building prompts for SQL generation."""

    SYSTEM_PROMPT = """You are an expert SQL assistant specializing in data quality analysis.
Your task is to convert natural language questions into SQL queries.

STRICT RULES:
1. Generate ONLY SELECT queries (no INSERT, UPDATE, DELETE, DROP, or any data modification)
2. Use the exact column names provided in the schema
3. Return only valid SQL that can run on the given table
4. Format your response with the SQL in a markdown code block
5. Add a brief explanation after the SQL

RESPONSE FORMAT:
```sql
[Your SQL query here]
```

Explanation: [Brief 1-sentence explanation of what the query does]
"""

    USER_PROMPT_TEMPLATE = """Database Schema:
{schema}

User Question: {question}

Generate a SQL query to answer this question. Remember to use only SELECT statements and exact column names from the schema above."""

    def __init__(self):
        """Initialize the Query Handler."""
        pass

    def build_prompt(self, question: str, schema: str) -> Dict[str, str]:
        """
        Build a prompt for the LLM.

        Args:
            question: The user's natural language question
            schema: The database schema description

        Returns:
            Dictionary with 'system' and 'user' prompts
        """
        user_prompt = self.USER_PROMPT_TEMPLATE.format(
            schema=schema,
            question=question
        )

        return {
            "system": self.SYSTEM_PROMPT,
            "user": user_prompt
        }

    def build_correction_prompt(self, original_question: str, schema: str,
                                failed_sql: str, error_message: str) -> Dict[str, str]:
        """
        Build a prompt for correcting a failed SQL query.

        Args:
            original_question: The original user question
            schema: The database schema description
            failed_sql: The SQL that failed
            error_message: The error message from validation/execution

        Returns:
            Dictionary with 'system' and 'user' prompts
        """
        correction_prompt = f"""Database Schema:
{schema}

Original Question: {original_question}

Your previous SQL query failed:
```sql
{failed_sql}
```

Error: {error_message}

Please correct the SQL query to fix this error. Use only the column names from the schema above."""

        return {
            "system": self.SYSTEM_PROMPT,
            "user": correction_prompt
        }
