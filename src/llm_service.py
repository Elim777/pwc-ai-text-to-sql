"""
LLM Service Module
Handles communication with OpenAI API for SQL generation.
"""

import os
import time
import logging
from typing import Dict, Optional
from openai import OpenAI
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class LLMService:
    """Service for interacting with OpenAI LLM."""

    def __init__(self):
        """Initialize the LLM service with API credentials."""
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        self.client = OpenAI(api_key=self.api_key)
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        self.temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.0'))
        self.max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', '500'))
        self.max_retries = int(os.getenv('MAX_RETRIES', '2'))
        self.timeout = int(os.getenv('REQUEST_TIMEOUT', '30'))

        logger.info(f"LLM Service initialized with model: {self.model}")

    def generate_sql(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generate SQL query from prompts using OpenAI API.

        Args:
            system_prompt: System-level instructions for the model
            user_prompt: User's question and context

        Returns:
            Generated SQL query and explanation from the model

        Raises:
            Exception: If API call fails after retries
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        for attempt in range(self.max_retries + 1):
            try:
                logger.info(f"Calling OpenAI API (attempt {attempt + 1}/{self.max_retries + 1})")

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    timeout=self.timeout
                )

                # Extract the response content
                content = response.choices[0].message.content

                # Log usage statistics
                if hasattr(response, 'usage'):
                    logger.info(
                        f"Token usage - Prompt: {response.usage.prompt_tokens}, "
                        f"Completion: {response.usage.completion_tokens}, "
                        f"Total: {response.usage.total_tokens}"
                    )

                return content

            except Exception as e:
                logger.error(f"OpenAI API error on attempt {attempt + 1}: {str(e)}")

                if attempt < self.max_retries:
                    # Exponential backoff
                    wait_time = 2 ** attempt
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    # Final attempt failed
                    raise Exception(f"OpenAI API call failed after {self.max_retries + 1} attempts: {str(e)}")

    def generate_sql_with_retry(self, prompts: Dict[str, str]) -> str:
        """
        Generate SQL with automatic retry on failure.

        Args:
            prompts: Dictionary with 'system' and 'user' keys

        Returns:
            Generated response from the model
        """
        return self.generate_sql(
            system_prompt=prompts['system'],
            user_prompt=prompts['user']
        )
