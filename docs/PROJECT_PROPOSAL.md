# AI-Powered Data Quality Management Solution
## Project Proposal for Jäppinen Ltd.

**Prepared by:** PwC Digital Solutions Team
**Date:** January 2026
**Version:** 1.0

---

## Executive Summary

Jäppinen Ltd. seeks an AI-powered solution to enable non-technical users to interact with data and perform data quality management tasks without requiring SQL knowledge or technical expertise. This proposal outlines a comprehensive approach to building a proof-of-concept (PoC) and production-ready system that leverages Generative AI to transform natural language questions into SQL queries and analytical insights.

**Key Benefits:**
- **Democratized Data Access** - Business users can query data without IT dependency
- **Rapid Insights** - Get answers to data quality questions in seconds, not hours
- **Cost-Effective** - Leverages state-of-the-art AI at ~$0.0002 per query
- **Scalable Architecture** - Clear path from PoC to enterprise production deployment
- **Enhanced Data Quality** - Proactive identification of completeness, outliers, and anomalies

**Estimated Timeline:** 6-8 weeks from kickoff to production-ready solution
**Team Size:** 3-4 people
**Technology:** OpenAI GPT-4o-mini, Python, Streamlit, PostgreSQL

---

## 1. Problem Statement

### Current Challenges

1. **Technical Barrier** - Non-technical users cannot directly query databases, creating dependency on IT/Analytics teams
2. **Slow Turnaround** - Simple data quality questions require submitting tickets and waiting for analyst availability
3. **Limited Self-Service** - Business users lack tools to explore data independently
4. **Data Quality Blind Spots** - Manual data profiling is time-consuming and often incomplete

### Business Impact

- **Lost Productivity** - Analysts spend 40% of time on repetitive data queries
- **Delayed Decisions** - Business decisions delayed due to slow data access
- **Inconsistent Analysis** - Different analysts may interpret data requirements differently
- **Missed Data Issues** - Quality problems discovered late in the process

---

## 2. Proposed Solution

### Solution Overview

An **AI-powered Natural Language to SQL** system that enables business users to ask data quality questions in plain English and receive immediate, accurate answers. The system combines:

1. **Advanced Language Models** - GPT-4o-mini for natural language understanding
2. **Intelligent Query Generation** - Automatic SQL creation with safety validation
3. **Interactive Interface** - User-friendly web application
4. **Robust Security** - Multi-layer validation preventing dangerous operations

### How It Works

```
User Question (Natural Language)
        ↓
AI Understanding (GPT-4o-mini)
        ↓
SQL Query Generation
        ↓
Safety Validation
        ↓
Query Execution
        ↓
Results + Explanation
```

### Example Use Cases

- How many rows are in the dataset?
- What are the unique currencies?
- How many USD transactions?
- Show me top 5 rows by transaction value
- What is the average transaction value?
- Show me transaction count by currency
- What countries are in the dataset?
- How many transactions in fiscal year 2015?
- What is the total value by country?

---

## 3. Technical Design

### 3.1 Architecture Overview

#### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER LAYER                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          Web Browser (Desktop/Mobile)                 │   │
│  └────────────────────┬─────────────────────────────────┘   │
└───────────────────────┼──────────────────────────────────────┘
                        │ HTTPS
┌───────────────────────┼──────────────────────────────────────┐
│               PRESENTATION LAYER                             │
│  ┌────────────────────▼─────────────────────────────────┐   │
│  │         Streamlit Web Application                     │   │
│  │  • Interactive UI                                     │   │
│  │  • Session Management                                 │   │
│  │  • Result Visualization                               │   │
│  └────────────────────┬─────────────────────────────────┘   │
└───────────────────────┼──────────────────────────────────────┘
                        │ Internal API
┌───────────────────────┼──────────────────────────────────────┐
│                 APPLICATION LAYER                            │
│  ┌────────────────────▼─────────────────────────────────┐   │
│  │           Query Handler                               │   │
│  │  • Prompt Building                                    │   │
│  │  • Schema Management                                  │   │
│  └────────────────────┬─────────────────────────────────┘   │
│                       │                                       │
│  ┌────────────────────▼─────────────────────────────────┐   │
│  │           LLM Service                                 │   │
│  │  • OpenAI API Integration                             │   │
│  │  • Retry Logic                                        │   │
│  │  • Error Handling                                     │   │
│  └────────────────────┬─────────────────────────────────┘   │
│                       │                                       │
│  ┌────────────────────▼─────────────────────────────────┐   │
│  │           SQL Validator                               │   │
│  │  • Syntax Validation                                  │   │
│  │  • Security Checks                                    │   │
│  │  • Query Sanitization                                 │   │
│  └────────────────────┬─────────────────────────────────┘   │
└───────────────────────┼──────────────────────────────────────┘
                        │ SQL Query
┌───────────────────────┼──────────────────────────────────────┐
│                   DATA LAYER                                 │
│  ┌────────────────────▼─────────────────────────────────┐   │
│  │         PostgreSQL Database                           │   │
│  │  • Production Data                                    │   │
│  │  • Read-Only Access                                   │   │
│  │  • Row-Level Security                                 │   │
│  └───────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘

                    EXTERNAL SERVICES
        ┌──────────────────────────────────────┐
        │      OpenAI API (GPT-4o-mini)        │
        │  • Natural Language Processing       │
        │  • SQL Generation                    │
        └──────────────────────────────────────┘

                 OBSERVABILITY LAYER
        ┌──────────────────────────────────────┐
        │      Monitoring & Logging            │
        │  • LangFuse (LLM Tracing)           │
        │  • Application Logs                  │
        │  • Performance Metrics               │
        └──────────────────────────────────────┘
```

#### Component Descriptions

**1. Web Application (Streamlit)**
- User-facing interface
- Natural language input
- Results visualization (tables, charts)
- Download capabilities (CSV, Excel)

**2. Query Handler**
- Builds optimized prompts for the LLM
- Manages database schema information
- Handles query context and history

**3. LLM Service**
- Communicates with OpenAI API
- Implements retry logic and error handling
- Manages API rate limits
- Logs all AI interactions for audit

**4. SQL Validator**
- Validates generated SQL syntax
- Blocks dangerous operations (DROP, DELETE, UPDATE)
- Ensures read-only queries
- Prevents SQL injection attacks

**5. Database Layer**
- PostgreSQL for production data
- Read-only user permissions
- Row-level security for multi-tenant scenarios
- Query result limits to prevent resource exhaustion

**6. Observability**
- LangFuse for LLM request/response tracking
- Application performance monitoring
- Cost tracking (API usage)
- User activity audit logs

### 3.2 Security Architecture

```
┌────────────────────────────────────────────────────────┐
│                    Security Layers                     │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Layer 1: User Authentication                          │
│  ├─ SSO Integration (Azure AD / Okta)                  │
│  ├─ Multi-Factor Authentication                        │
│  └─ Session Management                                 │
│                                                        │
│  Layer 2: Authorization                                │
│  ├─ Role-Based Access Control (RBAC)                   │
│  ├─ Row-Level Security (RLS)                           │
│  └─ Data Access Policies                               │
│                                                        │
│  Layer 3: Input Validation                             │
│  ├─ Prompt Injection Prevention                        │
│  ├─ Input Sanitization                                 │
│  └─ Maximum Input Length Limits                        │
│                                                        │
│  Layer 4: SQL Validation                               │
│  ├─ Keyword Blacklist (DELETE, etc.)                   │
│  ├─ Syntax Validation                                  │
│  └─ Read-Only Query Enforcement                        │
│                                                        │
│  Layer 5: Output Filtering                             │
│  ├─ PII Detection & Masking                            │
│  ├─ Result Size Limits                                 │
│  └─ Sensitive Data Redaction                           │
│                                                        │
│  Layer 6: Network Security                             │
│  ├─ HTTPS Encryption                                   │
│  ├─ API Key Rotation                                   │
│  └─ VPC/Private Networking                             │
│                                                        │
│  Layer 7: Audit & Monitoring                           │
│  ├─ All Queries Logged                                 │
│  ├─ User Activity Tracking                             │
│  └─ Anomaly Detection                                  │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### 3.3 Technologies Used

#### Core Stack - PoC vs Production

| Component | PoC Technology | Production Technology | Purpose |
|-----------|---------------|---------------------|---------|
| **Language Model** | OpenAI GPT-4o-mini | OpenAI GPT-4o-mini | Natural language to SQL conversion |
| **Programming Language** | Python 3.11+ | Python 3.11+ | Backend logic and integrations |
| **Frontend** | Streamlit 1.30+ | React/Vue.js SPA | User interface and visualization |
| **Backend Framework** | Embedded in Streamlit | FastAPI 0.100+ (async) | REST API and business logic |
| **OpenAI Client** | `openai.OpenAI` (sync) | `openai.AsyncOpenAI` (async) | Non-blocking LLM calls |
| **Data Processing** | Pandas 2.2+ | Pandas 2.2+ | Data manipulation |
| **SQL Engine** | PandasSQL 0.7+ (in-memory) | PostgreSQL 14+ | SQL execution and data storage |
| **Database Driver** | N/A | asyncpg 0.29+ | Async PostgreSQL connection |
| **Validation** | sqlparse 0.5+ | sqlparse 0.5+ | SQL syntax validation |
| **Environment** | python-dotenv 1.0+ | Azure Key Vault | Configuration management |

**Why Async for Production:**
- Non-blocking OpenAI API calls (handle 100+ concurrent users)
- Improved response times under load (UI remains responsive)
- Better resource utilization (CPU not waiting idle)
- Scalable architecture (horizontal scaling with load balancers)

#### Supporting Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Observability** | LangFuse | LLM request tracing and monitoring |
| **Cost Tracking** | Helicone | API usage and cost analytics |
| **Containerization** | Docker | Consistent deployment environments |
| **CI/CD** | GitHub Actions | Automated testing and deployment |
| **Hosting** | Azure App Service | Scalable cloud infrastructure |
| **Secret Management** | Azure Key Vault | Secure API key storage |

#### Why These Technologies?

**OpenAI GPT-4o-mini:**
- Industry-leading natural language understanding
- Specialized in code generation (including SQL)
- 20× more cost-effective than GPT-4 ($0.15/1M input tokens)
- Excellent accuracy for text-to-SQL tasks (85-95% on benchmarks)

**Streamlit (PoC) → FastAPI + React (Production):**
- **PoC:** Streamlit enables rapid prototyping (build in days, not weeks)
- **PoC:** Python-native = low learning curve for data teams
- **Production:** FastAPI provides async REST API (handles concurrent users)
- **Production:** React/Vue SPA = enterprise-grade UI/UX
- **Migration Path:** Modular src/ architecture enables smooth transition

**PostgreSQL + asyncpg:**
- Enterprise-grade reliability and ACID compliance
- Advanced security features (RLS, SSL, encryption at rest)
- Excellent performance for analytical queries
- **asyncpg:** Fastest PostgreSQL driver for Python (3-5× faster than psycopg2)
- **asyncpg:** Native async support for non-blocking queries

**Direct API Integration (No Heavy Frameworks):**
- Full control over prompts and logic
- Minimal dependencies = easier maintenance
- No vendor lock-in to specific AI frameworks
- Better debugging and troubleshooting

### 3.4 Data Flow

#### Query Processing Flow

```
1. User Input
   ↓
   "How many customers have incomplete profiles?"

2. Schema Retrieval
   ↓
   System loads database schema (tables, columns, types)

3. Prompt Construction
   ↓
   System Prompt: "You are an SQL expert..."
   User Prompt: "Schema: [tables]... Question: [user question]"

4. AI Processing (GPT-4o-mini)
   ↓
   ```sql
   SELECT COUNT(*) FROM customers
   WHERE email IS NULL OR phone IS NULL
   ```

5. SQL Validation
   ↓
   ✓ Syntax check (sqlparse)
   ✓ Security check (no DELETE/DROP/UPDATE)
   ✓ Query complexity check

6. Query Execution
   ↓
   Execute on read-only database connection

7. Result Formatting
   ↓
   Convert to user-friendly format (table, chart)

8. Response Delivery
   ↓
   Display results + SQL + explanation to user
```

#### Error Handling & Self-Correction

```
Query Generation Failed?
   ↓
   ┌─────────────────┐
   │ Attempt 1 Failed │
   │ Error: "Unknown  │
   │ column 'email'"  │
   └────────┬─────────┘
            │
            ▼
   ┌─────────────────────────┐
   │ Send Error to LLM       │
   │ "Your query failed      │
   │ because column 'email'  │
   │ doesn't exist.          │
   │ Available columns: ..." │
   └────────┬────────────────┘
            │
            ▼
   ┌─────────────────┐
   │ Attempt 2       │
   │ Corrected Query │
   └────────┬────────┘
            │
            ▼
      ✓ Success
```

Success Rate: ~95% after 2 attempts (based on research)

---

## 4. Deployment Plan

### 4.1 Infrastructure Requirements

#### PoC/Demo Environment

| Resource | Specification | Purpose |
|----------|--------------|---------|
| **Compute** | 2 vCPU, 4 GB RAM | Application server |
| **Storage** | 10 GB SSD | Application and logs |
| **Database** | N/A (In-memory Pandas) | Data storage |
| **Network** | Standard bandwidth | User access |

**Estimated Cost:** ~$30-50/month (Azure App Service Basic tier)

#### Production Environment

| Resource | Specification | Purpose |
|----------|--------------|---------|
| **App Service** | 4 vCPU, 8 GB RAM | FastAPI backend (2+ instances, async) |
| **Frontend** | Static Web App / CDN | React/Vue SPA hosting |
| **Load Balancer** | Azure Application Gateway | Traffic distribution |
| **Database** | PostgreSQL Flexible Server (4 vCPU, 16 GB) | Production data (asyncpg driver) |
| **Storage** | 100 GB Premium SSD | Database storage |
| **Monitoring** | Application Insights + LangFuse | Performance tracking & LLM observability |
| **Backup** | Automated daily backups | Disaster recovery |

**Estimated Cost:** ~$500-700/month (includes async infrastructure)

**Plus OpenAI API Costs:**
- PoC (100 queries/day): ~$6/month
- Production (1,000 queries/day): ~$60/month
- Enterprise (10,000 queries/day): ~$600/month

### 4.2 Deployment Strategy

#### Phase 1: PoC Deployment (Week 4-5)

1. **Local Development**
   - Developers run on localhost
   - Test with sample data

2. **Internal Staging**
   - Deploy to Azure App Service (Development tier)
   - Internal team testing
   - Collect feedback

3. **Client Demo**
   - Dedicated demo environment
   - Sample dataset (anonymized)
   - Controlled access

#### Phase 2: Pilot Production (Week 6-8)

1. **Production Infrastructure Setup**
   - Provision Azure resources
   - Configure PostgreSQL database
   - Set up monitoring and alerts

2. **Data Migration**
   - Connect to client's data sources
   - Set up data synchronization
   - Validate data integrity

3. **User Onboarding**
   - Train initial user group (5-10 users)
   - Gather feedback
   - Iterate on UX

4. **Go-Live**
   - Gradual rollout to broader user base
   - 24/7 monitoring
   - Support team on standby

#### Phase 3: Full Production (Week 9+)

1. **Scale & Optimize**
   - Monitor usage patterns
   - Optimize costs (caching, batching)
   - Scale infrastructure as needed

2. **Feature Enhancements**
   - Add visualizations
   - Support additional data sources
   - Implement advanced analytics

### 4.3 DevOps & CI/CD

```
┌──────────────┐
│  Developer   │
│  Commits Code│
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│  GitHub          │
│  (Version Control│
└──────┬───────────┘
       │
       ▼
┌────────────────────────┐
│  GitHub Actions        │
│  1. Run Unit Tests     │
│  2. Run Linters        │
│  3. Security Scan      │
│  4. Build Docker Image │
└──────┬─────────────────┘
       │
       ▼
┌────────────────────────┐
│  Azure Container       │
│  Registry              │
└──────┬─────────────────┘
       │
       ▼
┌────────────────────────┐
│  Azure App Service     │
│  (Auto-deploy)         │
└────────────────────────┘
```

**Automated Pipeline:**
- Code push triggers tests
- All tests must pass before deployment
- Automatic deployment to staging
- Manual approval for production
- Rollback capability

### 4.4 Security & Compliance

**Data Security:**
- All data encrypted in transit (TLS 1.3)
- Data encrypted at rest (AES-256)
- No data stored in application layer
- Audit logs retained for 1 year

**API Security:**
- API keys stored in Azure Key Vault
- Key rotation every 90 days
- Rate limiting per user
- Anomaly detection

**Compliance:**
- GDPR-compliant (no PII in prompts sent to OpenAI)
- SOC 2 Type II (Azure infrastructure)
- Regular security audits
- Penetration testing (annual)

---

## 5. Project Planning

### 5.1 Development Timeline (8 Weeks)

#### Week 1: Project Initiation & Discovery
**Objectives:**
- Finalize requirements
- Set up development environment
- Data schema analysis

**Deliverables:**
- Project kickoff meeting
- Detailed technical specifications
- Development environment configured
- Sample dataset prepared

**Team Activities:**
- Requirements gathering sessions with stakeholders
- Database schema documentation
- Development tools setup

---

#### Week 2: Core Backend Development
**Objectives:**
- Build data layer
- Implement LLM integration (sync for PoC, async-ready architecture)
- Create prompt templates

**Deliverables:**
- Data loader module (Excel/CSV/Database)
- OpenAI API integration (sync `openai.OpenAI` for PoC)
- Query handler with optimized prompts
- SQL validator with security checks
- Modular architecture enabling async migration

**Milestones:**
- ✓ Successfully load sample data
- ✓ Generate first SQL query from natural language
- ✓ Validate SQL safety checks
- ✓ Code structure supports future async conversion

---

#### Week 3: UI Development & Integration
**Objectives:**
- Build user interface
- Integrate frontend with backend
- Implement result visualization

**Deliverables:**
- Streamlit web application
- Query input interface
- Results display (tables, charts)
- Download functionality

**Milestones:**
- ✓ End-to-end user flow working
- ✓ UI mockups approved by stakeholders
- ✓ Responsive design for mobile/tablet

---

#### Week 4: Testing & Refinement
**Objectives:**
- Comprehensive testing
- Bug fixes
- Performance optimization

**Deliverables:**
- Unit tests (80%+ coverage)
- Integration tests
- User acceptance test plan
- Performance benchmarks

**Testing Focus:**
- SQL validation edge cases
- Error handling scenarios
- Prompt optimization for accuracy
- Load testing (concurrent users)

---

#### Week 5: PoC Demo & Feedback
**Objectives:**
- Internal demo
- Stakeholder presentation
- Gather feedback

**Deliverables:**
- PoC demo environment
- Demo script with example queries
- Feedback collection
- Iteration plan

**Demo Scenarios:**
- Data completeness analysis
- Outlier detection
- Distribution queries
- Time-series analysis

---

#### Week 6: Production Preparation & Async Migration
**Objectives:**
- Set up production infrastructure
- Migrate to async architecture (FastAPI + AsyncOpenAI)
- Implement monitoring
- Security hardening

**Deliverables:**
- Production Azure environment
- PostgreSQL database setup with asyncpg driver
- **Async backend migration:**
  - FastAPI REST API implementation
  - AsyncOpenAI client integration
  - Async database queries (asyncpg)
  - Load testing with concurrent users (100+)
- Monitoring dashboards (LangFuse, Application Insights)
- Security audit completed

**Infrastructure Tasks:**
- Provision cloud resources (load balancer, app instances)
- Configure SSL certificates
- Set up backups and disaster recovery
- Implement authentication (SSO)

**Technical Migration:**
- Replace `openai.OpenAI` → `openai.AsyncOpenAI`
- Replace PandasSQL → PostgreSQL + asyncpg
- Create FastAPI endpoints (async def)
- Implement async connection pooling

---

#### Week 7: Data Migration & Integration
**Objectives:**
- Connect to production data sources
- Data validation
- User training

**Deliverables:**
- Production data pipeline
- Data validation reports
- User training materials
- Administrator documentation

**Activities:**
- Connect to client databases
- Data synchronization setup
- Train initial user group (5-10 people)
- Create video tutorials

---

#### Week 8: Go-Live & Support
**Objectives:**
- Production deployment
- User onboarding
- Stabilization

**Deliverables:**
- Production system live
- User onboarding complete
- Support runbook
- Handover documentation

**Go-Live Checklist:**
- ✓ All tests passing
- ✓ Security review approved
- ✓ Monitoring active
- ✓ Support team trained
- ✓ Rollback plan ready

---

### 5.2 Weekly Breakdown Summary

| Week | Focus Area | Key Deliverable | Status Gate |
|------|-----------|-----------------|-------------|
| 1 | Initiation | Technical Specs | Requirements sign-off |
| 2 | Backend | LLM Integration | First SQL generation |
| 3 | Frontend | UI Application | End-to-end flow |
| 4 | Testing | Test Suite | 80% test coverage |
| 5 | Demo | PoC Presentation | Stakeholder approval |
| 6 | Infrastructure | Prod Environment | Security audit pass |
| 7 | Integration | Data Pipeline | Data validation |
| 8 | Deployment | Production System | Go-live approval |

---

### 5.3 Resources Needed

#### Team Composition

**Core Team (4 people):**

1. **AI/ML Engineer** (1 person, full-time)
   - **Responsibilities:**
     - LLM integration and optimization
     - Prompt engineering
     - Model performance monitoring
     - Cost optimization
     - Migration from sync to async OpenAI clients
   - **Skills Required:**
     - Python expertise (asyncio, async/await)
     - OpenAI API experience (OpenAI, AsyncOpenAI)
     - Natural Language Processing knowledge
     - SQL proficiency
     - Performance optimization for async workflows
   - **Seniority:** Senior (5+ years)

2. **Full-Stack Developer** (1 person, full-time)
   - **Responsibilities:**
     - Streamlit application development (PoC)
     - FastAPI backend development (Production)
     - Async/await implementation for concurrent requests
     - Database integration (asyncpg, SQLAlchemy)
     - UI/UX implementation (React/Vue migration)
   - **Skills Required:**
     - Python (Streamlit, FastAPI, asyncio)
     - Async programming (async/await, AsyncOpenAI)
     - Frontend (React/Vue.js, HTML/CSS/JavaScript)
     - PostgreSQL + asyncpg
     - REST API design
   - **Seniority:** Mid-Senior (3-5 years)

3. **Data Engineer** (1 person, full-time weeks 1-7, part-time week 8)
   - **Responsibilities:**
     - Data pipeline development
     - Database schema design
     - ETL processes
     - Data validation
   - **Skills Required:**
     - SQL expertise (PostgreSQL)
     - Data modeling
     - ETL tools
     - Python (Pandas)
   - **Seniority:** Mid-level (3-4 years)

4. **DevOps Engineer** (1 person, part-time weeks 1-5, full-time weeks 6-8)
   - **Responsibilities:**
     - Infrastructure setup (Azure)
     - CI/CD pipeline
     - Monitoring and logging
     - Security implementation
   - **Skills Required:**
     - Azure cloud services
     - Docker/Kubernetes
     - GitHub Actions
     - Security best practices
   - **Seniority:** Mid-Senior (4+ years)

**Extended Team (Part-time/Advisory):**

5. **Product Manager** (part-time, ~25% allocation)
   - Requirements gathering
   - Stakeholder management
   - User acceptance testing coordination

6. **UX Designer** (part-time, weeks 2-3)
   - UI mockups
   - User flow design
   - Usability testing

7. **Security Specialist** (advisory, week 6)
   - Security audit
   - Penetration testing
   - Compliance review

#### Total Team Effort

| Role | Weeks | FTE | Total Person-Weeks |
|------|-------|-----|-------------------|
| AI/ML Engineer | 8 | 1.0 | 8 |
| Full-Stack Developer | 8 | 1.0 | 8 |
| Data Engineer | 8 | 0.75 | 6 |
| DevOps Engineer | 8 | 0.625 | 5 |
| Product Manager | 8 | 0.25 | 2 |
| UX Designer | 2 | 0.5 | 1 |
| Security Specialist | 1 | 0.25 | 0.25 |
| **TOTAL** | | | **30.25 person-weeks** |

---

### 5.4 Cost Estimates

#### Development Costs

| Role | Rate (EUR/hour) | Hours | Cost (EUR) |
|------|----------------|-------|------------|
| AI/ML Engineer (Senior) | 120 | 320 | 38,400 |
| Full-Stack Developer | 100 | 320 | 32,000 |
| Data Engineer | 90 | 240 | 21,600 |
| DevOps Engineer | 100 | 200 | 20,000 |
| Product Manager | 110 | 80 | 8,800 |
| UX Designer | 95 | 40 | 3,800 |
| Security Specialist | 130 | 10 | 1,300 |
| **Subtotal Development** | | | **125,900** |

#### Infrastructure & Operational Costs (First 3 Months)

| Item | Monthly Cost (EUR) | 3 Months (EUR) |
|------|-------------------|----------------|
| Azure App Service (Production) | 450 | 1,350 |
| PostgreSQL Database | 350 | 1,050 |
| Monitoring & Logging | 100 | 300 |
| OpenAI API (1,000 queries/day) | 55 | 165 |
| Backup & Storage | 50 | 150 |
| SSL Certificates | 15 | 45 |
| **Subtotal Infrastructure** | | **3,060** |

#### Total Project Cost (8 Weeks + 3 Months Operation)

| Category | Cost (EUR) |
|----------|-----------|
| Development | 125,900 |
| Infrastructure (3 months) | 3,060 |
| Contingency (10%) | 12,896 |
| **TOTAL** | **141,856** |

**Rounded Total: €142,000**

---

## 6. UI Mockup

### Main Application Screen

```
┌────────────────────────────────────────────────────────────────────┐
│  🤖 AI Data Quality Assistant                    [User] [Settings] │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Ask a question about your data                                    │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ How many records have missing email addresses?               │ │
│  │                                                        [Ask 🔍]│ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  Example questions:                                                 │
│  • What percentage of records are complete?                        │
│  • Show me top 10 customers by transaction value                  │
│  • How many orders per country?                                    │
│                                                                     │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  📝 Generated SQL Query                                [Expand ▼]  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ SELECT COUNT(*) as incomplete_records                         │ │
│  │ FROM customers                                                 │ │
│  │ WHERE email IS NULL OR email = ''                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  💡 Explanation: This query counts customer records where the      │
│     email field is either NULL or empty.                           │
│                                                                     │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  📊 Results                                [Download CSV 📥]        │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ incomplete_records                                            │ │
│  ├───────────────────────────────────────────────────────────────┤ │
│  │           1,247                                                │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ⏱ Query time: 0.3s  |  📊 Rows: 1  |  💰 Cost: $0.0002           │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘

Sidebar:
┌─────────────────────────┐
│ 📊 Dataset Info         │
├─────────────────────────┤
│ Total Records: 45,231   │
│ Columns: 18             │
│ Last Updated: 2h ago    │
│                         │
│ 📋 Quick Stats          │
│ ┌─────────────────────┐ │
│ │ Completeness: 87%   │ │
│ │ ▓▓▓▓▓▓▓▓▓▓▓░░░░     │ │
│ └─────────────────────┘ │
│                         │
│ 🌍 Countries: 23        │
│ 💰 Currencies: 5        │
│                         │
│ ℹ About                 │
│ Powered by GPT-4o-mini  │
└─────────────────────────┘
```

### Key UI Features

1. **Natural Language Input**
   - Large, prominent text box
   - Auto-suggest based on common queries
   - Voice input support (future)

2. **SQL Transparency**
   - Expandable SQL section (optional visibility)
   - Syntax highlighting
   - Copy-to-clipboard button

3. **Clear Results**
   - Table view for multiple rows
   - Single metric display for aggregates
   - Chart visualization for distributions

4. **Quick Actions**
   - Download results (CSV, Excel)
   - Share query link
   - Save to favorites

5. **Dataset Context**
   - Summary statistics in sidebar
   - Data freshness indicator
   - Quick links to common queries

---

## 7. Risk Assessment & Mitigation

### Technical Risks

| Risk | Probability | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| **LLM generates incorrect SQL** | Medium | High | Multi-layer validation, self-correction loop, testing with diverse queries |
| **API rate limits exceeded** | Low | Medium | Implement caching, request queuing, upgrade API tier if needed |
| **Poor query performance** | Medium | Medium | Query optimization, result caching, database indexing |
| **Security vulnerability** | Low | Critical | Security audit, penetration testing, regular updates |

### Business Risks

| Risk | Probability | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| **User adoption resistance** | Medium | High | Comprehensive training, demonstrate value early, gather feedback |
| **Data quality issues** | Medium | Medium | Data validation layer, clear error messages, data profiling |
| **Cost overruns** | Low | Medium | Monthly cost monitoring, set alerts, optimize prompts |

---

## 8. Success Metrics

### Technical KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| **SQL Accuracy** | >90% | Queries that execute successfully without correction |
| **Response Time** | <3 seconds | P95 time from question to result |
| **Uptime** | 99.5% | Monthly uptime percentage |
| **Error Rate** | <5% | Failed queries / total queries |

### Business KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| **User Adoption** | 70% of target users | Active users / invited users (30 days) |
| **Query Volume** | 500/day | Daily query count after 3 months |
| **Time Savings** | 60% reduction | Time to answer vs. manual SQL |
| **User Satisfaction** | >4.0/5.0 | NPS or satisfaction survey |

---

## 9. Next Steps

### Immediate Actions (Week 1)

1. **Contract Approval**
   - Review and sign proposal
   - Finalize budget
   - Define success criteria

2. **Team Mobilization**
   - Assign project team
   - Schedule kickoff meeting
   - Set up communication channels

3. **Environment Setup**
   - Provision Azure resources
   - Create development environments
   - Configure access and permissions

4. **Discovery Sessions**
   - Database schema review
   - Sample data collection
   - User interviews (5-10 potential users)

### Long-term Roadmap (Post Go-Live)

**Quarter 1:**
- Stabilization and optimization
- Feature enhancements based on feedback
- Expand to additional data sources

**Quarter 2:**
- Advanced visualizations
- Export to BI tools (Power BI, Tableau)
- Scheduled/automated queries

**Quarter 3:**
- Predictive analytics integration
- Natural language data upload
- Mobile app development

---

## 10. Conclusion

This AI-powered data quality management solution represents a significant step forward in democratizing data access within Jäppinen Ltd. By leveraging state-of-the-art language models and robust engineering practices, we can deliver a system that:

✓ **Empowers business users** to self-serve data insights
✓ **Reduces dependency** on IT and analytics teams
✓ **Improves data quality** through proactive monitoring
✓ **Scales efficiently** from PoC to enterprise deployment

We are confident that this solution will deliver measurable business value within the proposed 8-week timeline and budget.

---

## Appendices

### Appendix A: Sample Queries & Expected Results

Available in demo environment.

### Appendix B: Security Compliance Documentation

To be provided during Week 6 security audit.

### Appendix C: Detailed Cost Breakdown

See Section 5.4 above.

---

**Prepared by:**
PwC Digital Solutions Team
AI & Data Analytics Practice

**Contact:**
[Project Lead Name]
[Email]
[Phone]

**Document Version:** 1.0
**Last Updated:** January 10, 2026
