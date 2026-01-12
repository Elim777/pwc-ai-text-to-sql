"""
Data Loader Module
Handles loading and preparing data from Excel files for SQL querying.
"""

import pandas as pd
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Loads and manages data from Excel files."""

    def __init__(self, excel_path: str):
        """
        Initialize the DataLoader with path to Excel file.

        Args:
            excel_path: Path to the Excel file containing the data
        """
        self.excel_path = excel_path
        self.df = None
        self.table_name = "accrual_accounts"  # Default table name for PandasSQL

    def load_data(self) -> pd.DataFrame:
        """
        Load data from Excel file into a Pandas DataFrame.

        Returns:
            Loaded DataFrame
        """
        try:
            logger.info(f"Loading data from {self.excel_path}")
            self.df = pd.read_excel(self.excel_path)

            # Drop the first unnamed column if it exists (index column from Excel)
            if 'Unnamed: 0' in self.df.columns:
                self.df = self.df.drop('Unnamed: 0', axis=1)

            # Clean column names - replace spaces and special characters
            self.df.columns = self.df.columns.str.replace(' ', '_')
            self.df.columns = self.df.columns.str.replace('.', '_')
            self.df.columns = self.df.columns.str.replace('-', '_')  # Replace hyphens
            self.df.columns = self.df.columns.str.replace('/', '_')  # Replace slashes

            logger.info(f"Loaded {len(self.df)} rows and {len(self.df.columns)} columns")
            return self.df
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def get_schema_description(self) -> str:
        """
        Generate a natural language description of the database schema for the LLM.

        Returns:
            Schema description string
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        schema_parts = []
        schema_parts.append(f"Table name: {self.table_name}")
        schema_parts.append("\nColumns:")

        for col in self.df.columns:
            dtype = str(self.df[col].dtype)

            # Get sample values (non-null)
            sample_values = self.df[col].dropna().unique()[:3]
            sample_str = ", ".join([str(v) for v in sample_values])

            # Count nulls
            null_count = self.df[col].isnull().sum()
            null_pct = (null_count / len(self.df)) * 100

            schema_parts.append(
                f"  - {col} ({dtype})"
                f" | Sample values: [{sample_str}]"
                f" | Nulls: {null_count} ({null_pct:.1f}%)"
            )

        schema_parts.append(f"\nTotal rows: {len(self.df)}")

        return "\n".join(schema_parts)

    def get_column_list(self) -> List[str]:
        """Get list of all column names."""
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        return self.df.columns.tolist()

    def get_data_summary(self) -> Dict:
        """
        Get summary statistics about the loaded data.

        Returns:
            Dictionary with summary information
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        return {
            "row_count": len(self.df),
            "column_count": len(self.df.columns),
            "columns": self.df.columns.tolist(),
            "dtypes": {col: str(dtype) for col, dtype in self.df.dtypes.items()},
            "missing_values": {
                col: int(count)
                for col, count in self.df.isnull().sum().items()
                if count > 0
            }
        }
