"""
AI Data Quality Assistant - Streamlit Application
Text-to-SQL interface for data quality management and analysis.
"""

import streamlit as st
import pandas as pd
import pandasql as ps
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_loader import DataLoader
from llm_service import LLMService
from query_handler import QueryHandler
from sql_validator import SQLValidator


# Page configuration
st.set_page_config(
    page_title="AI Data Quality Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 600;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .stTextInput > div > div > input {
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def init_services():
    """Initialize all services (cached to avoid re-initialization)."""
    data_loader = DataLoader("Data Dump - Accrual Accounts.xlsx")
    data_loader.load_data()

    llm_service = LLMService()
    query_handler = QueryHandler()
    sql_validator = SQLValidator()

    return data_loader, llm_service, query_handler, sql_validator


def execute_sql_query(sql: str, df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    """Execute SQL query on DataFrame using pandasql."""
    try:
        # Create a local namespace with the dataframe
        locals_dict = {table_name: df}
        result = ps.sqldf(sql, locals_dict)
        return result
    except Exception as e:
        raise Exception(f"Query execution error: {str(e)}")


def main():
    """Main application function."""

    # Header
    st.markdown('<p class="main-header">🤖 AI Data Quality Assistant</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Ask questions about your data in natural language</p>',
        unsafe_allow_html=True
    )

    # Initialize services
    try:
        data_loader, llm_service, query_handler, sql_validator = init_services()
    except Exception as e:
        st.error(f"Failed to initialize services: {str(e)}")
        st.info("Please ensure OPENAI_API_KEY is set in .env file")
        return

    # Sidebar with information
    with st.sidebar:
        st.header("📊 Dataset Information")
        summary = data_loader.get_data_summary()

        st.metric("Total Rows", f"{summary['row_count']:,}")
        st.metric("Columns", summary['column_count'])

        with st.expander("📋 Column Names"):
            for col in summary['columns']:
                st.text(f"• {col}")

        with st.expander("ℹ️ About"):
            st.markdown("""
            This tool uses **AI** to convert your questions into SQL queries.

            **Example Questions:**
            - How many rows are in the dataset?
            - What are the unique currencies?
            - How many USD transactions?
            - Show me top 5 rows by transaction value
            - What is the average transaction value?
            - Show me transaction count by currency
            - What countries are in the dataset?
            - How many transactions in fiscal year 2015?
            - What is the total value by country?
            """)

        st.divider()
        st.caption("Powered by GPT-4o-mini")

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        # Input form
        with st.form("query_form"):
            user_question = st.text_input(
                "Ask a question about the data:",
                placeholder="e.g., How many transactions are in USD currency?",
                help="Type your question in natural language"
            )

            submit_button = st.form_submit_button("🔍 Analyze", use_container_width=True)

        if submit_button and user_question:
            with st.spinner("🤖 Generating SQL query..."):
                try:
                    # Build prompts
                    schema = data_loader.get_schema_description()
                    prompts = query_handler.build_prompt(user_question, schema)

                    # Get SQL from LLM
                    llm_response = llm_service.generate_sql_with_retry(prompts)

                    # Extract SQL from response
                    sql_query = sql_validator.extract_sql_from_response(llm_response)

                    # Validate SQL
                    is_valid, error_message = sql_validator.validate(sql_query)

                    if not is_valid:
                        # Try to correct the query
                        st.warning(f"First attempt failed: {error_message}. Trying to correct...")

                        correction_prompts = query_handler.build_correction_prompt(
                            user_question, schema, sql_query, error_message
                        )

                        llm_response = llm_service.generate_sql_with_retry(correction_prompts)
                        sql_query = sql_validator.extract_sql_from_response(llm_response)

                        is_valid, error_message = sql_validator.validate(sql_query)

                        if not is_valid:
                            st.error(f"❌ Could not generate valid SQL: {error_message}")
                            st.code(sql_query, language="sql")
                            return

                    # Display generated SQL
                    with st.expander("📝 Generated SQL Query", expanded=True):
                        st.code(sql_query, language="sql")

                    # Execute query
                    with st.spinner("⚙️ Executing query..."):
                        result_df = execute_sql_query(
                            sql_query,
                            data_loader.df,
                            data_loader.table_name
                        )

                    # Display results
                    st.success("✅ Query executed successfully!")

                    st.subheader("📊 Results")

                    # Show result metrics
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Rows Returned", len(result_df))
                    with col_b:
                        st.metric("Columns", len(result_df.columns))
                    with col_c:
                        if len(result_df) > 0 and len(result_df.columns) == 1:
                            # Single value result (e.g., COUNT)
                            st.metric("Value", result_df.iloc[0, 0])

                    # Display dataframe
                    st.dataframe(
                        result_df,
                        use_container_width=True,
                        height=400
                    )

                    # Download button
                    csv = result_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results (CSV)",
                        data=csv,
                        file_name="query_results.csv",
                        mime="text/csv"
                    )

                    # Extract explanation from LLM response
                    if "Explanation:" in llm_response:
                        explanation = llm_response.split("Explanation:")[1].strip()
                        st.info(f"💡 **Explanation:** {explanation}")

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.exception(e)

    with col2:
        # Quick stats
        st.subheader("📈 Quick Stats")

        if data_loader.df is not None:
            df = data_loader.df

            # Currency breakdown
            if 'Currency' in df.columns:
                st.write("**Currencies:**")
                currency_counts = df['Currency'].value_counts()
                st.bar_chart(currency_counts)

            # Missing values
            st.write("**Data Completeness:**")
            total_cells = len(df) * len(df.columns)
            missing_cells = df.isnull().sum().sum()
            completeness = ((total_cells - missing_cells) / total_cells) * 100

            st.progress(completeness / 100)
            st.caption(f"{completeness:.1f}% complete")


if __name__ == "__main__":
    main()
