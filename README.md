# 🤖 AI Data Quality Assistant

An intelligent Text-to-SQL system that enables non-technical users to query and analyze data using natural language questions. Built as a proof-of-concept for AI-powered data quality management.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Example Questions](#example-questions)
- [Development](#development)
- [Production Considerations](#production-considerations)
- [License](#license)

## 🎯 Overview

This application demonstrates how AI can democratize data access by allowing business users to ask questions about their data in plain English, without needing to know SQL or database structures. The system automatically:

1. Interprets natural language questions
2. Generates appropriate SQL queries
3. Validates queries for safety and correctness
4. Executes queries on the dataset
5. Presents results in an intuitive interface

**Use Case:** Data quality management and profiling for financial/accounting datasets.

## ✨ Features

### Core Functionality
- 🗣️ **Natural Language Interface** - Ask questions in plain English
- 🤖 **AI-Powered SQL Generation** - GPT-4o-mini converts questions to SQL
- 🛡️ **Security Validation** - Prevents dangerous SQL operations (DROP, DELETE, etc.)
- 📊 **Interactive Results** - View data in tables, download as CSV
- 🔄 **Self-Correction** - Automatically retries failed queries with corrections

### Data Quality Features
- 📈 **Completeness Analysis** - "How many fields are empty?"
- 🔍 **Outlier Detection** - "Show me unusual transaction values"
- 📉 **Distribution Queries** - "How many transactions per currency?"
- 🎯 **Filtering** - "Show records with missing clearing dates"

### Technical Features
- ⚡ **Fast Response Times** - Optimized prompts and caching
- 🔒 **Safe SQL Execution** - Read-only queries on in-memory data
- 📝 **Query Logging** - Track all AI-generated SQL
- 🎨 **User-Friendly UI** - Built with Streamlit

## 🏗️ Architecture

```
┌─────────────┐
│    User     │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│   Streamlit UI      │
│   (app.py)          │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Query Handler      │
│  (Prompt Builder)   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│   OpenAI API        │
│   (GPT-4o-mini)     │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  SQL Validator      │
│  (Safety Check)     │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│   PandasSQL         │
│   (Query Engine)    │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Results Display    │
└─────────────────────┘
```

## 🚀 Installation

### Prerequisites

- Python 3.11 or higher
- OpenAI API key

### Step 1: Clone the Repository

```bash
git clone https://github.com/Elim777/pwc-ai-text-to-sql.git
cd pwc-ai-text-to-sql
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=your_api_key_here
```

## 💻 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Asking Questions

Simply type your question in natural language:

- "How many records are there?"
- "What currencies are in the dataset?"
- "Show me the top 10 transactions by value"
- "How many records have missing clearing dates?"
- "What's the average transaction value in USD?"

### Viewing Results

- **SQL Query** - See the generated SQL (expandable section)
- **Results Table** - Interactive data grid
- **Download** - Export results as CSV
- **Explanation** - AI-generated explanation of what the query does

## 📁 Project Structure

```
PwC/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .env                           # Your API keys (gitignored)
├── .gitignore                     # Git ignore rules
│
├── src/                           # Source code modules
│   ├── data_loader.py             # Excel data loading and schema generation
│   ├── llm_service.py             # OpenAI API integration
│   ├── query_handler.py           # Prompt building and management
│   └── sql_validator.py           # SQL validation and safety checks
│
├── tests/                         # Unit tests (future)
│
├── docs/                          # Documentation
│
├── Data Dump - Accrual Accounts.xlsx  # Sample dataset
└── README.md                      # This file
```

## 🛠️ Technology Stack

### Core Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **LLM** | OpenAI GPT-4o-mini | Natural language understanding & SQL generation |
| **Data Processing** | Pandas | Data manipulation and management |
| **SQL Engine** | PandasSQL | Execute SQL queries on DataFrames |
| **UI Framework** | Streamlit | Interactive web interface |
| **Validation** | sqlparse | SQL syntax validation |

### Why This Stack?

- **OpenAI GPT-4o-mini**: 20× cheaper than GPT-4, excellent for text-to-SQL tasks
- **Pandas + PandasSQL**: No database setup needed for PoC, easy transition to production DB
- **Streamlit**: Rapid development, Python-native, perfect for data applications
- **Direct API Integration**: Full control, no framework overhead, minimal dependencies

## 🔧 Development

### Running Tests

```bash
python -m pytest tests/
```

### Code Structure

**Modular Design:**
- Each component has a single responsibility
- Easy to test and maintain
- Clear separation of concerns

**Key Modules:**

1. **DataLoader** - Handles all data loading and schema generation
2. **LLMService** - Manages OpenAI API calls with retry logic
3. **QueryHandler** - Builds optimized prompts for the LLM
4. **SQLValidator** - Ensures query safety and correctness

### Adding New Features

**Example: Add visualization**

1. Modify `app.py` to detect chart requests
2. Use Streamlit's charting capabilities
3. Add prompt instructions to `query_handler.py`

## 🏭 Production Considerations

### Roadmap to Production

This PoC can be upgraded to production with these enhancements:

#### 1. **Real Database Integration**
- Replace PandasSQL with PostgreSQL/Snowflake connector
- Add connection pooling
- Implement row-level security

#### 2. **Authentication & Authorization**
- SSO integration (Azure AD, Okta)
- Role-based access control (RBAC)
- User audit logs

#### 3. **Observability**
- Integrate LangFuse for LLM tracing
- Add Helicone for cost tracking
- Implement error monitoring (Sentry)

#### 4. **Performance Optimization**
- Query result caching (Redis)
- Prompt caching
- Async query execution

#### 5. **Enhanced Security**
- PII detection and masking
- Query approval workflows for sensitive data
- Rate limiting per user

#### 6. **Multi-tenancy**
- Data segregation
- Per-tenant customization
- Tenant-level analytics

### Cost Estimates

**GPT-4o-mini Pricing:**
- Input: $0.15 / 1M tokens
- Output: $0.60 / 1M tokens

**Estimated Cost:**
- ~$0.0002 per query
- 1,000 queries/day = ~$6/month
- Very cost-effective for PoC and production

### Scalability

**Current Capacity:**
- Handles 13K+ rows efficiently
- Sub-second query generation
- Can scale to 100K+ rows with optimizations

**For Larger Datasets:**
- Migrate to DuckDB (10-100× faster than Pandas)
- Use distributed processing (Dask)
- Implement query optimization

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For questions or issues, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ for PwC - Demonstrating AI's potential in democratizing data access**
