# Epic 0: Project Setup & Placeholder Pages

## Epic Description
Set up the foundational Streamlit project structure, database connections, and placeholder pages for the Child Nutrition Dashboard. This epic establishes the technical foundation and basic navigation structure.

## Epic Goals
- Create a well-structured Streamlit project following PRD recommendations
- Establish secure Snowflake database connectivity
- Implement placeholder pages with navigation
- Set up development environment and dependencies

---

## Story 0.1: Initialize Streamlit Project Structure

### User Story
As a developer, I want to set up the basic Streamlit project structure so that I can begin building the dashboard with proper organization and dependencies.

### Acceptance Criteria
- [ ] Create folder structure following PRD recommendations:
  ```
  child-nutrition-dashboard/
  ├── app.py
  ├── requirements.txt
  ├── .streamlit/
  │   ├── config.toml
  │   └── secrets.toml.template
  ├── pages/
  ├── utils/
  ├── config/
  └── assets/
  ```
- [ ] Set up `requirements.txt` with all necessary dependencies:
  - streamlit==1.30.0
  - snowflake-connector-python==3.5.0
  - plotly==5.18.0
  - openai==1.0.0
  - pandas==2.1.0
  - python-dotenv==1.0.0
- [ ] Create `.streamlit/config.toml` with theme and configuration
- [ ] Create `.streamlit/secrets.toml.template` for credentials
- [ ] Set up main `app.py` entry point with basic structure

### Technical Implementation Notes
- Use the exact folder structure from the PRD
- Include all dependencies with specific versions for reproducibility
- Configure Streamlit theme to match PRD color palette
- Set up secrets template for secure credential management

### SQL Query Examples
N/A - This story focuses on project structure

### Component Specifications
- Main app entry point with sidebar navigation
- Basic page routing structure
- Configuration files for development and production

---

## Story 0.2: Create Database Connection Module

### User Story
As a developer, I want to establish secure database connectivity to Snowflake so that the dashboard can access nutrition data with proper error handling and connection pooling.

### Acceptance Criteria
- [ ] Create `utils/database.py` with Snowflake connection using uppercase column names
- [ ] Implement connection pooling for performance
- [ ] Create helper functions for query execution with error handling
- [ ] Add comprehensive logging for debugging
- [ ] Handle connection timeouts and retries
- [ ] Support parameterized queries to prevent SQL injection

### Technical Implementation Notes
- Use `snowflake-connector-python` for database connectivity
- Implement connection pooling with configurable pool size
- Create wrapper functions for common query patterns
- Add proper error handling for network issues and query failures
- Use uppercase column names matching the actual Snowflake schema:
  - `BENEFICIARY_ID`, `ANSWER`, `WHO_INDEX`, `CAPTURE_DATE`
  - `SITE`, `SITE_GROUP`, `FIRST_NAMES`, `LAST_NAME`
  - `HOUSEHOLD`, `HOUSEHOLD_ID`, `FLAGGED`, `DUPLICATE`

### SQL Query Examples
```sql
-- Test connection query
SELECT COUNT(*) as record_count FROM NUTRITION_DATA;

-- Basic data retrieval
SELECT 
    BENEFICIARY_ID,
    ANSWER,
    WHO_INDEX,
    CAPTURE_DATE,
    SITE,
    FIRST_NAMES
FROM NUTRITION_DATA 
WHERE FLAGGED = 0 AND DUPLICATE = 'False'
LIMIT 10;
```

### Component Specifications
- `get_connection()` - Get connection from pool
- `execute_query(query, params=None)` - Execute parameterized query
- `execute_query_with_retry(query, max_retries=3)` - Execute with retry logic
- `close_all_connections()` - Clean up connections

---

## Story 0.3: Create Placeholder Pages

### User Story
As a developer, I want to create placeholder pages for all three main sections so that I can test navigation and establish the page structure before implementing functionality.

### Acceptance Criteria
- [ ] Create `pages/1_📊_Overview.py` with placeholder content
- [ ] Create `pages/2_📍_Location_Analysis.py` with placeholder content
- [ ] Create `pages/3_👶_Child_Analysis.py` with placeholder content
- [ ] Add navigation sidebar to main app with page titles
- [ ] Test that all pages load and navigation works correctly
- [ ] Each placeholder page shows:
  - Page title and description
  - Placeholder for key metrics/charts
  - "Coming Soon" message for functionality

### Technical Implementation Notes
- Use Streamlit's automatic page routing with numbered prefixes
- Include emoji icons in page names for visual appeal
- Add basic page structure with headers and placeholders
- Implement session state management for page navigation
- Test navigation between all pages

### SQL Query Examples
N/A - Placeholder pages don't require database queries yet

### Component Specifications
- Main app sidebar with navigation links
- Page headers with titles and descriptions
- Placeholder containers for future charts and metrics
- Basic styling consistent with PRD design system

---

## Epic Success Criteria
- [ ] All three placeholder pages load without errors
- [ ] Navigation between pages works smoothly
- [ ] Database connection can be established and tested
- [ ] Project structure follows PRD recommendations
- [ ] Development environment is ready for feature implementation

## Dependencies
- Snowflake database access credentials
- Python 3.10+ environment
- Streamlit development server

## Risks & Mitigations
- **Risk**: Database connection issues
  - **Mitigation**: Implement comprehensive error handling and connection testing
- **Risk**: Dependency version conflicts
  - **Mitigation**: Pin specific versions in requirements.txt and test in clean environment
