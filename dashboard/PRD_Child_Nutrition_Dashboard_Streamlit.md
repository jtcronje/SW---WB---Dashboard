# Product Requirements Document (PRD)
# Child Nutrition Impact Dashboard - Streamlit Implementation

**Version:** 1.0  
**Date:** October 2024  
**Author:** BI Product Team  
**Status:** Ready for Development

---

## Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [Product Overview](#2-product-overview)
3. [User Personas](#3-user-personas)
4. [Functional Requirements](#4-functional-requirements)
5. [Technical Architecture](#5-technical-architecture)
6. [Database Schema](#6-database-schema)
7. [Page-by-Page Specifications](#7-page-by-page-specifications)
8. [AI Integration Requirements](#8-ai-integration-requirements)
9. [UI/UX Requirements](#9-uiux-requirements)
10. [Performance Requirements](#10-performance-requirements)
11. [Security & Privacy](#11-security--privacy)
12. [Testing Requirements](#12-testing-requirements)
13. [Deployment & Infrastructure](#13-deployment--infrastructure)
14. [Future Enhancements](#14-future-enhancements)

---

## 1. Executive Summary

### 1.1 Purpose
Build a comprehensive, AI-powered Streamlit dashboard to track and analyze child nutrition outcomes across multiple Early Childhood Development (ECD) sites in South Africa. The dashboard enables program managers, site coordinators, and stakeholders to monitor stunting rates, evaluate interventions, and make data-driven decisions to improve child nutrition outcomes.

### 1.2 Business Objectives
- **Transparency**: Provide clear visibility into nutrition program impact
- **Accountability**: Enable data-driven reporting to donors and stakeholders
- **Early Intervention**: Identify at-risk children requiring additional support
- **Resource Optimization**: Allocate resources based on site-specific needs
- **Impact Measurement**: Track progress toward WHO-aligned targets

### 1.3 Success Metrics
- Dashboard loads within 3 seconds for all pages
- 95%+ data accuracy from source systems
- AI interpretations generated within 2 seconds
- User satisfaction score of 4.5+/5.0
- Weekly active users: 50+ program staff

---

## 2. Product Overview

### 2.1 Product Description
A three-page Streamlit dashboard featuring:
1. **Overview Page**: Program-wide metrics and trends
2. **Location Analysis Page**: Site-specific deep dives
3. **Child Analysis Page**: Individual child growth tracking

### 2.2 Key Features
- Real-time data synchronization from Snowflake
- Interactive visualizations with Plotly/Altair
- AI-powered graph interpretations using Claude API
- Multi-level filtering (location, time period, child)
- Export capabilities (PDF reports, CSV data)
- Mobile-responsive design
- Role-based access control

### 2.3 Technology Stack
- **Frontend**: Streamlit 1.30+
- **Backend**: Python 3.10+
- **Database**: Snowflake
- **Visualization**: Plotly, Altair
- **AI**: Anthropic Claude API (Claude Sonnet 4)
- **Authentication**: Streamlit auth or Auth0
- **Deployment**: Streamlit Cloud or AWS ECS

---

## 3. User Personas

### 3.1 Primary Users

#### Persona 1: Program Manager
- **Name**: Sarah Mitchell
- **Role**: National Nutrition Program Manager
- **Needs**: 
  - High-level overview of program impact
  - Comparison across all sites
  - Data for donor reports
  - Trend analysis over time
- **Technical Proficiency**: Medium
- **Access Level**: Full access to all data

#### Persona 2: Site Coordinator
- **Name**: Thabo Ndlovu
- **Role**: ECD Site Coordinator (Sasolburg)
- **Needs**:
  - Site-specific performance metrics
  - Individual child tracking
  - Identification of at-risk children
  - Comparison to other sites
- **Technical Proficiency**: Low-Medium
- **Access Level**: Limited to assigned site(s)

#### Persona 3: Executive Stakeholder
- **Name**: Dr. Jane van der Berg
- **Role**: Board Member / Donor Representative
- **Needs**:
  - Executive summaries
  - Impact metrics
  - ROI justification
  - Trend visualizations
- **Technical Proficiency**: Low
- **Access Level**: Overview and aggregated data only

---

## 4. Functional Requirements

### 4.1 Core Functionality

#### FR-001: Multi-Page Navigation
- **Priority**: P0 (Must Have)
- **Description**: Sidebar navigation with 3 main pages
- **Acceptance Criteria**:
  - Sidebar always visible on left side
  - Active page clearly highlighted
  - Page transitions under 500ms
  - Navigation state persists during session

#### FR-002: Data Refresh
- **Priority**: P0
- **Description**: Automatic data synchronization from Snowflake
- **Acceptance Criteria**:
  - Data refreshed every 6 hours automatically
  - Manual refresh button available
  - Last refresh timestamp displayed
  - Loading indicators during refresh

#### FR-003: AI Interpretation
- **Priority**: P0
- **Description**: AI-generated insights for each visualization
- **Acceptance Criteria**:
  - "Get AI Interpretation" button below each chart
  - Interpretations generate within 2 seconds
  - Loading state displayed during generation
  - Interpretations persist during session
  - Error handling for API failures

#### FR-004: Export Functionality
- **Priority**: P1 (Should Have)
- **Description**: Export data and visualizations
- **Acceptance Criteria**:
  - Export charts as PNG/PDF
  - Export data tables as CSV/Excel
  - Include metadata (date, filters applied)
  - Preserve formatting in exports

#### FR-005: Responsive Design
- **Priority**: P1
- **Description**: Optimized viewing on multiple devices
- **Acceptance Criteria**:
  - Desktop (1920x1080): Full layout
  - Tablet (768x1024): Adapted layout
  - Mobile (375x667): Simplified layout
  - Charts remain readable on all devices

---

## 5. Technical Architecture

### 5.1 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Browser                         │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTPS
                      ↓
┌─────────────────────────────────────────────────────────────┐
│                   Streamlit Application                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Overview Page│  │Location Page │  │  Child Page  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Data Layer (Snowflake Connector)           │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         AI Service Layer (Claude API Client)         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────┬───────────────────────┘
                      │               │
                      ↓               ↓
            ┌──────────────┐  ┌──────────────┐
            │  Snowflake   │  │ Claude API   │
            │   Database   │  │  (Anthropic) │
            └──────────────┘  └──────────────┘
```

### 5.2 Application Structure

```
child-nutrition-dashboard/
├── app.py                          # Main Streamlit app entry point
├── requirements.txt                # Python dependencies
├── .streamlit/
│   ├── config.toml                # Streamlit configuration
│   └── secrets.toml               # API keys and credentials (gitignored)
├── pages/
│   ├── 1_📊_Overview.py           # Overview page
│   ├── 2_📍_Location_Analysis.py  # Location analysis page
│   └── 3_👶_Child_Analysis.py     # Child analysis page
├── utils/
│   ├── __init__.py
│   ├── database.py                # Snowflake connection & queries
│   ├── ai_service.py              # Claude API integration
│   ├── data_processing.py         # Data transformation functions
│   ├── visualizations.py          # Reusable chart components
│   └── styling.py                 # CSS and theme definitions
├── config/
│   ├── __init__.py
│   ├── database_config.py         # DB connection settings
│   └── app_config.py              # App-wide constants
├── assets/
│   ├── logo.png
│   └── custom.css
├── tests/
│   ├── test_database.py
│   ├── test_ai_service.py
│   └── test_data_processing.py
└── README.md
```

### 5.3 Key Dependencies

```txt
# Core
streamlit==1.30.0
pandas==2.1.0
numpy==1.24.0

# Database
snowflake-connector-python==3.5.0
snowflake-sqlalchemy==1.5.0

# Visualization
plotly==5.18.0
altair==5.2.0

# AI
anthropic==0.18.0

# Utilities
python-dotenv==1.0.0
pytz==2023.3
```

---

## 6. Database Schema

### 6.1 Snowflake Schema Overview

**Database**: `NUTRITION_DB`  
**Schema**: `IMPACT_TRACKING`

### 6.2 Core Tables

#### Table: `MEASUREMENTS`
Primary table storing all child height measurements.

```sql
CREATE TABLE NUTRITION_DB.IMPACT_TRACKING.MEASUREMENTS (
    -- Primary Key
    measurement_id              VARCHAR(50) PRIMARY KEY,
    
    -- Foreign Keys
    beneficiary_id              NUMBER(38,0) NOT NULL,
    site_id                     VARCHAR(50) NOT NULL,
    household_id                NUMBER(38,0),
    
    -- Measurement Data
    capture_date                TIMESTAMP_NTZ NOT NULL,
    height_cm                   FLOAT NOT NULL,
    who_z_score                 FLOAT NOT NULL,
    who_index_type              VARCHAR(10) DEFAULT 'z',
    
    -- Status & Classification
    status                      VARCHAR(30) NOT NULL,
    -- Values: 'Normal', 'At Risk', 'Stunted', 'Severely Stunted'
    
    measurement_type            VARCHAR(50) DEFAULT 'Height',
    
    -- Data Quality
    quality_score               FLOAT,
    flagged                     BOOLEAN DEFAULT FALSE,
    measured                    BOOLEAN DEFAULT TRUE,
    entry_number                INTEGER,
    is_duplicate                BOOLEAN DEFAULT FALSE,
    
    -- Metadata
    created_on                  TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_on                  TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    created_by                  VARCHAR(100),
    
    -- Constraints
    CONSTRAINT chk_height CHECK (height_cm BETWEEN 40 AND 200),
    CONSTRAINT chk_z_score CHECK (who_z_score BETWEEN -6 AND 6),
    CONSTRAINT chk_status CHECK (status IN ('Normal', 'At Risk', 'Stunted', 'Severely Stunted'))
);

-- Indexes
CREATE INDEX idx_measurements_beneficiary ON MEASUREMENTS(beneficiary_id);
CREATE INDEX idx_measurements_site ON MEASUREMENTS(site_id);
CREATE INDEX idx_measurements_date ON MEASUREMENTS(capture_date);
CREATE INDEX idx_measurements_status ON MEASUREMENTS(status);
```

#### Table: `BENEFICIARIES`
Child demographic and enrollment information.

```sql
CREATE TABLE NUTRITION_DB.IMPACT_TRACKING.BENEFICIARIES (
    -- Primary Key
    beneficiary_id              NUMBER(38,0) PRIMARY KEY,
    
    -- Personal Information
    first_names                 VARCHAR(200) NOT NULL,
    last_name                   VARCHAR(200),
    nick_name                   VARCHAR(200),
    date_of_birth               DATE,
    gender                      VARCHAR(10),
    -- Values: 'Male', 'Female', 'Other', 'Unknown'
    
    -- Location & Program
    site_id                     VARCHAR(50) NOT NULL,
    household_id                NUMBER(38,0),
    enrollment_date             DATE NOT NULL,
    exit_date                   DATE,
    is_active                   BOOLEAN DEFAULT TRUE,
    
    -- Metadata
    created_on                  TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_on                  TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    
    -- Constraints
    CONSTRAINT chk_gender CHECK (gender IN ('Male', 'Female', 'Other', 'Unknown'))
);

-- Indexes
CREATE INDEX idx_beneficiaries_site ON BENEFICIARIES(site_id);
CREATE INDEX idx_beneficiaries_household ON BENEFICIARIES(household_id);
CREATE INDEX idx_beneficiaries_active ON BENEFICIARIES(is_active);
```

#### Table: `SITES`
ECD center and location information.

```sql
CREATE TABLE NUTRITION_DB.IMPACT_TRACKING.SITES (
    -- Primary Key
    site_id                     VARCHAR(50) PRIMARY KEY,
    
    -- Site Information
    site_name                   VARCHAR(200) NOT NULL UNIQUE,
    site_group                  VARCHAR(200) NOT NULL,
    -- Examples: 'Safripol', 'Jannie Mouton', 'GROOT Swem'
    
    domain_name                 VARCHAR(200) DEFAULT 'Food & Nutrition',
    subdomain_name              VARCHAR(200) DEFAULT 'Growth & Nutrition',
    
    -- Geographic Information
    province                    VARCHAR(100),
    city                        VARCHAR(100),
    address                     VARCHAR(500),
    latitude                    FLOAT,
    longitude                   FLOAT,
    
    -- Site Details
    total_capacity              INTEGER,
    site_type                   VARCHAR(50),
    -- Values: 'ECD Center', 'Preschool', 'Community Center'
    
    -- Status
    is_active                   BOOLEAN DEFAULT TRUE,
    start_date                  DATE NOT NULL,
    end_date                    DATE,
    
    -- Metadata
    created_on                  TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_on                  TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Indexes
CREATE INDEX idx_sites_group ON SITES(site_group);
CREATE INDEX idx_sites_active ON SITES(is_active);
```

#### Table: `HOUSEHOLDS`
Household/ECD center grouping information.

```sql
CREATE TABLE NUTRITION_DB.IMPACT_TRACKING.HOUSEHOLDS (
    -- Primary Key
    household_id                NUMBER(38,0) PRIMARY KEY,
    
    -- Household Information
    household_name              VARCHAR(300) NOT NULL,
    site_id                     VARCHAR(50) NOT NULL,
    
    -- Contact Information
    primary_contact_name        VARCHAR(200),
    primary_contact_phone       VARCHAR(20),
    primary_contact_email       VARCHAR(200),
    
    -- Metadata
    created_on                  TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_on                  TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    
    -- Foreign Keys
    FOREIGN KEY (site_id) REFERENCES SITES(site_id)
);

-- Indexes
CREATE INDEX idx_households_site ON HOUSEHOLDS(site_id);
```

### 6.3 Supporting Tables

#### Table: `MEASUREMENT_CATEGORIES`
Classification thresholds and definitions.

```sql
CREATE TABLE NUTRITION_DB.IMPACT_TRACKING.MEASUREMENT_CATEGORIES (
    category_id                 INTEGER PRIMARY KEY,
    category_name               VARCHAR(50) NOT NULL UNIQUE,
    z_score_min                 FLOAT NOT NULL,
    z_score_max                 FLOAT NOT NULL,
    description                 TEXT,
    color_code                  VARCHAR(7),  -- Hex color for UI
    display_order               INTEGER,
    is_active                   BOOLEAN DEFAULT TRUE
);

-- Reference Data
INSERT INTO MEASUREMENT_CATEGORIES VALUES
(1, 'Severely Stunted', -6.0, -3.0, 'Height-for-age z-score below -3', '#E53E3E', 1, TRUE),
(2, 'Stunted', -3.0, -2.0, 'Height-for-age z-score between -3 and -2', '#FC8181', 2, TRUE),
(3, 'At Risk', -2.0, -1.0, 'Height-for-age z-score between -2 and -1', '#F6AD55', 3, TRUE),
(4, 'Normal', -1.0, 6.0, 'Height-for-age z-score above -1', '#68D391', 4, TRUE);
```

#### Table: `AI_INTERPRETATIONS`
Cache for AI-generated interpretations (optional optimization).

```sql
CREATE TABLE NUTRITION_DB.IMPACT_TRACKING.AI_INTERPRETATIONS (
    interpretation_id           VARCHAR(50) PRIMARY KEY,
    graph_type                  VARCHAR(100) NOT NULL,
    filter_params               VARIANT,  -- JSON of applied filters
    interpretation_text         TEXT NOT NULL,
    generated_at                TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    model_version               VARCHAR(50),
    cache_ttl_hours             INTEGER DEFAULT 24
);

-- Index
CREATE INDEX idx_ai_cache ON AI_INTERPRETATIONS(graph_type, generated_at);
```

### 6.4 Views for Dashboard Queries

#### View: `VW_MEASUREMENT_SUMMARY`
Pre-aggregated measurement statistics per child.

```sql
CREATE OR REPLACE VIEW NUTRITION_DB.IMPACT_TRACKING.VW_MEASUREMENT_SUMMARY AS
SELECT 
    b.beneficiary_id,
    b.first_names,
    b.last_name,
    b.gender,
    b.date_of_birth,
    b.site_id,
    s.site_name,
    s.site_group,
    b.household_id,
    h.household_name,
    
    -- First Measurement
    FIRST_VALUE(m.capture_date) 
        OVER (PARTITION BY b.beneficiary_id ORDER BY m.capture_date) AS first_measurement_date,
    FIRST_VALUE(m.height_cm) 
        OVER (PARTITION BY b.beneficiary_id ORDER BY m.capture_date) AS first_height_cm,
    FIRST_VALUE(m.who_z_score) 
        OVER (PARTITION BY b.beneficiary_id ORDER BY m.capture_date) AS first_z_score,
    FIRST_VALUE(m.status) 
        OVER (PARTITION BY b.beneficiary_id ORDER BY m.capture_date) AS first_status,
    
    -- Last Measurement
    FIRST_VALUE(m.capture_date) 
        OVER (PARTITION BY b.beneficiary_id ORDER BY m.capture_date DESC) AS last_measurement_date,
    FIRST_VALUE(m.height_cm) 
        OVER (PARTITION BY b.beneficiary_id ORDER BY m.capture_date DESC) AS last_height_cm,
    FIRST_VALUE(m.who_z_score) 
        OVER (PARTITION BY b.beneficiary_id ORDER BY m.capture_date DESC) AS last_z_score,
    FIRST_VALUE(m.status) 
        OVER (PARTITION BY b.beneficiary_id ORDER BY m.capture_date DESC) AS last_status,
    
    -- Aggregate Metrics
    COUNT(m.measurement_id) AS total_measurements,
    AVG(m.who_z_score) AS avg_z_score,
    MAX(m.height_cm) - MIN(m.height_cm) AS height_gain_cm,
    MAX(m.who_z_score) - MIN(m.who_z_score) AS z_score_improvement,
    
    -- Time Period
    DATEDIFF(day, MIN(m.capture_date), MAX(m.capture_date)) AS monitoring_days

FROM BENEFICIARIES b
LEFT JOIN MEASUREMENTS m ON b.beneficiary_id = m.beneficiary_id
LEFT JOIN SITES s ON b.site_id = s.site_id
LEFT JOIN HOUSEHOLDS h ON b.household_id = h.household_id
WHERE b.is_active = TRUE
    AND m.is_duplicate = FALSE
    AND m.flagged = FALSE
GROUP BY 
    b.beneficiary_id, b.first_names, b.last_name, b.gender, 
    b.date_of_birth, b.site_id, s.site_name, s.site_group,
    b.household_id, h.household_name;
```

#### View: `VW_SITE_METRICS`
Pre-aggregated site-level statistics.

```sql
CREATE OR REPLACE VIEW NUTRITION_DB.IMPACT_TRACKING.VW_SITE_METRICS AS
SELECT 
    s.site_id,
    s.site_name,
    s.site_group,
    s.province,
    
    COUNT(DISTINCT b.beneficiary_id) AS total_children,
    COUNT(DISTINCT b.household_id) AS total_households,
    COUNT(m.measurement_id) AS total_measurements,
    
    AVG(m.who_z_score) AS avg_z_score,
    
    -- Current Status Distribution
    SUM(CASE WHEN m.status = 'Normal' THEN 1 ELSE 0 END) AS count_normal,
    SUM(CASE WHEN m.status = 'At Risk' THEN 1 ELSE 0 END) AS count_at_risk,
    SUM(CASE WHEN m.status = 'Stunted' THEN 1 ELSE 0 END) AS count_stunted,
    SUM(CASE WHEN m.status = 'Severely Stunted' THEN 1 ELSE 0 END) AS count_severely_stunted,
    
    -- Percentages
    ROUND(100.0 * SUM(CASE WHEN m.status = 'At Risk' THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS pct_at_risk,
    ROUND(100.0 * SUM(CASE WHEN m.status = 'Stunted' THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS pct_stunted,
    ROUND(100.0 * SUM(CASE WHEN m.status = 'Severely Stunted' THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS pct_severely_stunted,
    
    MIN(m.capture_date) AS first_measurement_date,
    MAX(m.capture_date) AS last_measurement_date

FROM SITES s
LEFT JOIN BENEFICIARIES b ON s.site_id = b.site_id AND b.is_active = TRUE
LEFT JOIN MEASUREMENTS m ON b.beneficiary_id = m.beneficiary_id 
    AND m.is_duplicate = FALSE 
    AND m.flagged = FALSE
WHERE s.is_active = TRUE
GROUP BY s.site_id, s.site_name, s.site_group, s.province;
```

---

## 7. Page-by-Page Specifications

### 7.1 Overview Page

#### Layout Structure
```
┌─────────────────────────────────────────────────────────────┐
│                        Page Header                          │
│  Title: "Program Overview"                                  │
│  Subtitle: "Comprehensive child nutrition impact analysis"  │
│  Last Updated: [Timestamp] | [Manual Refresh Button]        │
└─────────────────────────────────────────────────────────────┘

┌───────────┬───────────┬───────────┬───────────┐
│  Metric   │  Metric   │  Metric   │  Metric   │  ← Key Metrics Row
│  Card 1   │  Card 2   │  Card 3   │  Card 4   │
└───────────┴───────────┴───────────┴───────────┘

┌─────────────────────────────────────────────────────────────┐
│  Chart 1: Stunting Category Progress (Bar Chart)            │
│  [AI Interpretation Button]                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Chart 2: Number of Children by Category (Bar Chart)        │
│  [AI Interpretation Button]                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Chart 3: Temporal Trends (Area + Line Chart)               │
│  [AI Interpretation Button]                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────┬─────────────────────────────────────┐
│  Chart 4: Top Sites │  Chart 5: Program Distribution      │
│  (Horizontal Bar)   │  (Pie Chart)                        │
│  [AI Button]        │  [AI Button]                        │
└─────────────────────┴─────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Chart 6: WHO Z-Score Distribution (Line Chart)             │
│  [AI Interpretation Button]                                 │
└─────────────────────────────────────────────────────────────┘
```

#### 7.1.1 Key Metrics Cards

**Card 1: Total Children Measured**
```python
# Query
SELECT 
    COUNT(DISTINCT beneficiary_id) AS total_children,
    COUNT(measurement_id) AS total_measurements
FROM MEASUREMENTS
WHERE is_duplicate = FALSE AND flagged = FALSE;

# Display
- Large number: 36,050
- Subtitle: "Across 5,725 unique children"
- Icon: Users icon
- Color: Blue (#4299E1)
```

**Card 2: Active Sites**
```python
# Query
SELECT COUNT(DISTINCT site_id) AS active_sites
FROM SITES
WHERE is_active = TRUE;

# Display
- Large number: 29
- Subtitle: "Across South Africa"
- Icon: MapPin icon
- Color: Purple (#9F7AEA)
```

**Card 3: Stunting Reduction**
```python
# Query
WITH first_last AS (
    SELECT 
        AVG(CASE WHEN is_first = TRUE THEN stunting_rate END) AS first_rate,
        AVG(CASE WHEN is_first = FALSE THEN stunting_rate END) AS last_rate
    FROM (
        SELECT 
            beneficiary_id,
            status = 'Stunted' AS is_stunted,
            ROW_NUMBER() OVER (PARTITION BY beneficiary_id ORDER BY capture_date) = 1 AS is_first,
            100.0 * AVG(CASE WHEN status IN ('Stunted', 'Severely Stunted') THEN 1 ELSE 0 END) 
                OVER (PARTITION BY capture_date) AS stunting_rate
        FROM MEASUREMENTS
    )
)
SELECT ROUND(((first_rate - last_rate) / first_rate) * 100, 1) AS reduction_pct
FROM first_last;

# Display
- Large number: 28%
- Subtitle: "First to last measurement"
- Icon: TrendingUp (down arrow)
- Trend indicator: Green with -28%
- Color: Green (#48BB78)
```

**Card 4: Avg WHO Z-Score**
```python
# Query
SELECT ROUND(AVG(who_z_score), 2) AS avg_z_score
FROM MEASUREMENTS
WHERE is_duplicate = FALSE AND flagged = FALSE;

# Display
- Large number: -0.64
- Subtitle: "Improving toward 0 target"
- Icon: Activity icon
- Color: Orange (#F6AD55)
```

#### 7.1.2 Chart 1: Stunting Category Progress

**Chart Type**: Grouped Bar Chart  
**Library**: Plotly (plotly.graph_objects.Bar)

**Data Query**:
```sql
WITH first_measurements AS (
    SELECT 
        beneficiary_id,
        status,
        ROW_NUMBER() OVER (PARTITION BY beneficiary_id ORDER BY capture_date) AS rn
    FROM MEASUREMENTS
    WHERE is_duplicate = FALSE AND flagged = FALSE
),
last_measurements AS (
    SELECT 
        beneficiary_id,
        status,
        ROW_NUMBER() OVER (PARTITION BY beneficiary_id ORDER BY capture_date DESC) AS rn
    FROM MEASUREMENTS
    WHERE is_duplicate = FALSE AND flagged = FALSE
),
totals AS (
    SELECT COUNT(DISTINCT beneficiary_id) AS total FROM MEASUREMENTS
)
SELECT 
    'First Measurement' AS measurement_period,
    ROUND(100.0 * SUM(CASE WHEN status = 'At Risk' THEN 1 ELSE 0 END) / total, 1) AS at_risk_pct,
    ROUND(100.0 * SUM(CASE WHEN status = 'Stunted' THEN 1 ELSE 0 END) / total, 1) AS stunted_pct,
    ROUND(100.0 * SUM(CASE WHEN status = 'Severely Stunted' THEN 1 ELSE 0 END) / total, 1) AS severely_stunted_pct
FROM first_measurements, totals
WHERE rn = 1
GROUP BY total

UNION ALL

SELECT 
    'Last Measurement' AS measurement_period,
    ROUND(100.0 * SUM(CASE WHEN status = 'At Risk' THEN 1 ELSE 0 END) / total, 1) AS at_risk_pct,
    ROUND(100.0 * SUM(CASE WHEN status = 'Stunted' THEN 1 ELSE 0 END) / total, 1) AS stunted_pct,
    ROUND(100.0 * SUM(CASE WHEN status = 'Severely Stunted' THEN 1 ELSE 0 END) / total, 1) AS severely_stunted_pct
FROM last_measurements, totals
WHERE rn = 1
GROUP BY total

UNION ALL

SELECT 
    'Target Goal' AS measurement_period,
    2.5 AS at_risk_pct,
    2.5 AS stunted_pct,
    0.15 AS severely_stunted_pct;
```

**Visualization Specifications**:
- X-axis: Categorical (First Measurement, Last Measurement, Target Goal)
- Y-axis: Percentage (0-25%)
- 3 bars per category: At Risk (Orange), Stunted (Coral), Severely Stunted (Red)
- Bar width: 0.8
- Corner radius: 8px top corners
- Grid: Light gray (#E2E8F0), dashed
- Tooltip: Show exact percentages on hover
- Legend: Top right, horizontal

**AI Interpretation Prompt Template**:
```
You are analyzing child nutrition data for a non-profit program in South Africa.

Chart: Stunting Category Progress
Data:
- First Measurement: {at_risk_pct}% At Risk, {stunted_pct}% Stunted, {severely_stunted_pct}% Severely Stunted
- Last Measurement: {at_risk_pct}% At Risk, {stunted_pct}% Stunted, {severely_stunted_pct}% Severely Stunted
- Target: 2.5% At Risk, 2.5% Stunted, 0.15% Severely Stunted

Provide a 3-4 sentence interpretation in plain language for non-technical program staff, covering:
1. Overall trend (improving/worsening)
2. Most significant changes
3. Progress toward targets
4. What this means for program effectiveness
```

#### 7.1.3 Chart 2: Number of Children by Category

**Chart Type**: Grouped Bar Chart  
**Library**: Plotly

**Data Query**:
```sql
-- Similar to Chart 1, but with absolute counts instead of percentages
WITH first_measurements AS (
    SELECT 
        beneficiary_id,
        status,
        ROW_NUMBER() OVER (PARTITION BY beneficiary_id ORDER BY capture_date) AS rn
    FROM MEASUREMENTS
    WHERE is_duplicate = FALSE AND flagged = FALSE
),
last_measurements AS (
    SELECT 
        beneficiary_id,
        status,
        ROW_NUMBER() OVER (PARTITION BY beneficiary_id ORDER BY capture_date DESC) AS rn
    FROM MEASUREMENTS
    WHERE is_duplicate = FALSE AND flagged = FALSE
),
totals AS (
    SELECT COUNT(DISTINCT beneficiary_id) AS total FROM MEASUREMENTS
)
SELECT 
    'First Measurement' AS measurement_period,
    SUM(CASE WHEN status = 'At Risk' THEN 1 ELSE 0 END) AS at_risk_count,
    SUM(CASE WHEN status = 'Stunted' THEN 1 ELSE 0 END) AS stunted_count,
    SUM(CASE WHEN status = 'Severely Stunted' THEN 1 ELSE 0 END) AS severely_stunted_count
FROM first_measurements
WHERE rn = 1

UNION ALL

SELECT 
    'Last Measurement' AS measurement_period,
    SUM(CASE WHEN status = 'At Risk' THEN 1 ELSE 0 END) AS at_risk_count,
    SUM(CASE WHEN status = 'Stunted' THEN 1 ELSE 0 END) AS stunted_count,
    SUM(CASE WHEN status = 'Severely Stunted' THEN 1 ELSE 0 END) AS severely_stunted_count
FROM last_measurements
WHERE rn = 1

UNION ALL

SELECT 
    'Target' AS measurement_period,
    CAST(total * 0.025 AS INTEGER) AS at_risk_count,
    CAST(total * 0.025 AS INTEGER) AS stunted_count,
    CAST(total * 0.0015 AS INTEGER) AS severely_stunted_count
FROM totals;
```

**Visualization Specifications**: Same as Chart 1, but Y-axis shows counts (0-1500)

#### 7.1.4 Chart 3: Temporal Trends

**Chart Type**: Dual-axis Area + Line Chart  
**Library**: Plotly

**Data Query**:
```sql
WITH quarterly_data AS (
    SELECT 
        DATE_TRUNC('quarter', capture_date) AS quarter,
        COUNT(measurement_id) AS measurement_count,
        AVG(who_z_score) AS avg_z_score,
        100.0 * SUM(CASE WHEN status IN ('Stunted', 'Severely Stunted') THEN 1 ELSE 0 END) 
            / COUNT(*) AS stunting_rate
    FROM MEASUREMENTS
    WHERE is_duplicate = FALSE 
        AND flagged = FALSE
        AND capture_date >= DATEADD(year, -5, CURRENT_DATE())
    GROUP BY DATE_TRUNC('quarter', capture_date)
    ORDER BY quarter
)
SELECT 
    TO_CHAR(quarter, 'Mon YYYY') AS period,
    measurement_count,
    ROUND(avg_z_score, 2) AS avg_z_score,
    ROUND(stunting_rate, 1) AS stunting_rate
FROM quarterly_data;
```

**Visualization Specifications**:
- X-axis: Time periods (quarterly)
- Y-axis Left: Measurement count (0-4000)
- Y-axis Right: Stunting percentage (0-30%)
- Area chart (blue, 30% opacity): Measurement volume
- Line chart (red, thick): Stunting rate
- Grid: Both axes
- Tooltips: Show all values
- Legend: Top right

#### 7.1.5 Chart 4: Top Sites by Children Measured

**Chart Type**: Horizontal Bar Chart  
**Library**: Plotly

**Data Query**:
```sql
SELECT 
    site_name,
    COUNT(DISTINCT beneficiary_id) AS children_count,
    ROUND(100.0 * COUNT(DISTINCT beneficiary_id) / SUM(COUNT(DISTINCT beneficiary_id)) OVER (), 1) AS percentage
FROM MEASUREMENTS m
JOIN SITES s ON m.site_id = s.site_id
WHERE m.is_duplicate = FALSE 
    AND m.flagged = FALSE
    AND s.is_active = TRUE
GROUP BY site_name
ORDER BY children_count DESC
LIMIT 10;
```

**Visualization Specifications**:
- Orientation: Horizontal
- Y-axis: Site names (truncate at 30 chars)
- X-axis: Children count
- Bar color: Blue (#4299E1)
- Height: 350px
- Sort: Descending by count

#### 7.1.6 Chart 5: Program Distribution

**Chart Type**: Pie Chart  
**Library**: Plotly

**Data Query**:
```sql
SELECT 
    site_group,
    COUNT(DISTINCT beneficiary_id) AS children_count,
    ROUND(100.0 * COUNT(DISTINCT beneficiary_id) / SUM(COUNT(DISTINCT beneficiary_id)) OVER (), 1) AS percentage
FROM MEASUREMENTS m
JOIN SITES s ON m.site_id = s.site_id
WHERE m.is_duplicate = FALSE 
    AND m.flagged = FALSE
    AND s.is_active = TRUE
GROUP BY site_group
ORDER BY children_count DESC;
```

**Visualization Specifications**:
- Labels: Show site group name + percentage
- Colors: Use consistent color palette
- Hole: 0 (full pie, not donut)
- Height: 350px
- Legend: Right side

#### 7.1.7 Chart 6: WHO Z-Score Distribution

**Chart Type**: Line Chart  
**Library**: Plotly

**Data Query**:
```sql
WITH z_score_bins AS (
    SELECT 
        FLOOR(who_z_score * 2) / 2 AS z_score_bin, -- 0.5 bin width
        COUNT(*) AS frequency
    FROM MEASUREMENTS
    WHERE is_duplicate = FALSE 
        AND flagged = FALSE
        AND who_z_score BETWEEN -6 AND 6
    GROUP BY FLOOR(who_z_score * 2) / 2
)
SELECT 
    z_score_bin,
    frequency
FROM z_score_bins
ORDER BY z_score_bin;
```

**Visualization Specifications**:
- X-axis: Z-score (-6 to +6)
- Y-axis: Frequency (count)
- Line: Blue, thick (3px)
- Markers: Visible (radius 5px)
- Reference lines:
  - Vertical at -3 (Severe stunting threshold, red, dashed)
  - Vertical at -2 (Stunting threshold, orange, dashed)
  - Vertical at 0 (WHO median, green, dashed)
- Annotation box: Show current mean z-score
- Height: 400px

---

### 7.2 Location Analysis Page

#### Layout Structure
```
┌─────────────────────────────────────────────────────────────┐
│                        Page Header                          │
│  Title: "Location Analysis"                                 │
│  Subtitle: "Deep dive into site-specific nutrition outcomes"│
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Location Dropdown Selector                                 │
│  [Select Location: ▼]                                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Location Summary Hero Card (Gradient Background)           │
│  Site Name | Site Group | Key Metrics                       │
└─────────────────────────────────────────────────────────────┘

┌───────────┬───────────┬───────────┬───────────┐
│Performance│Performance│Performance│Performance│  ← Ranking Cards
│  Metric 1 │  Metric 2 │  Metric 3 │  Metric 4 │
└───────────┴───────────┴───────────┴───────────┘

┌─────────────────────────────────────────────────────────────┐
│  Chart 1: Nutrition Outcomes Over Time (Multi-line)         │
│  [AI Interpretation Button]                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Chart 2: Number of Children by Category - Location         │
│  [AI Interpretation Button]                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Chart 3: Current Status Distribution (Bar)                 │
│  [AI Interpretation Button]                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Chart 4: Z-Score Comparison Across Locations (Horiz Bar)   │
│  [AI Interpretation Button]                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Chart 5: Stunting Rate Comparison (Horizontal Bar)         │
│  [AI Interpretation Button]                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Chart 6: Measurement Volume Over Time (Area)               │
│  [AI Interpretation Button]                                 │
└─────────────────────────────────────────────────────────────┘
```

#### 7.2.1 Location Selector

**Component**: Streamlit selectbox  
**Placement**: Top of page, below header

```python
# Query for dropdown options
SELECT DISTINCT 
    site_id,
    site_name,
    COUNT(DISTINCT beneficiary_id) AS child_count
FROM MEASUREMENTS m
JOIN SITES s ON m.site_id = s.site_id
WHERE m.is_duplicate = FALSE 
    AND m.flagged = FALSE
    AND s.is_active = TRUE
GROUP BY site_id, site_name
ORDER BY site_name;

# Display format
# "Sasolburg - 10,009 children measured"
```

**State Management**:
- Selected location stored in `st.session_state.selected_location`
- Default: First location alphabetically
- On change: Refresh all charts and metrics

#### 7.2.2 Location Summary Card

**Component**: Custom styled div with gradient background

**Data Query**:
```sql
SELECT 
    s.site_name,
    s.site_group,
    COUNT(DISTINCT m.beneficiary_id) AS total_children,
    COUNT(m.measurement_id) AS total_measurements,
    COUNT(DISTINCT m.household_id) AS total_households,
    ROUND(AVG(m.who_z_score), 2) AS avg_z_score,
    ROUND(100.0 * SUM(CASE WHEN m.status IN ('Stunted', 'Severely Stunted') THEN 1 ELSE 0 END) 
        / COUNT(*), 1) AS stunting_rate
FROM SITES s
JOIN MEASUREMENTS m ON s.site_id = m.site_id
WHERE s.site_id = :selected_site_id
    AND m.is_duplicate = FALSE
    AND m.flagged = FALSE
GROUP BY s.site_name, s.site_group;
```

**Display Elements**:
- Large site name (32px font)
- Site group with map pin icon
- 4 key metrics in grid:
  1. Unique Children
  2. Households/Centers
  3. Avg Z-Score
  4. Stunting Rate
- Gradient background: Purple gradient (#667EEA to #764BA2)
- White text for contrast

#### 7.2.3 Performance Ranking Cards

**Component**: 4 metric cards showing rank vs other locations

**Card 1: Children Measured Rank**
```sql
WITH ranked_sites AS (
    SELECT 
        site_id,
        COUNT(DISTINCT beneficiary_id) AS children_count,
        RANK() OVER (ORDER BY COUNT(DISTINCT beneficiary_id) DESC) AS rank
    FROM MEASUREMENTS
    WHERE is_duplicate = FALSE AND flagged = FALSE
    GROUP BY site_id
)
SELECT 
    children_count,
    rank,
    (SELECT COUNT(DISTINCT site_id) FROM MEASUREMENTS) AS total_sites
FROM ranked_sites
WHERE site_id = :selected_site_id;
```

**Display**: "10,009 children | Rank: 1 of 29"

**Card 2: Avg Z-Score Rank** (higher z-score = better rank)
```sql
-- Similar query with ORDER BY AVG(who_z_score) DESC
```

**Card 3: Stunting Rate Rank** (lower rate = better rank)
```sql
-- Similar query with ORDER BY stunting_rate ASC
```

**Card 4: Severe Stunting Rank** (lower rate = better rank)
```sql
-- Similar query for severe stunting
```

#### 7.2.4 Chart 1: Nutrition Outcomes Over Time

**Chart Type**: Multi-line Chart (3 lines)  
**Library**: Plotly

**Data Query**:
```sql
WITH quarterly_data AS (
    SELECT 
        DATE_TRUNC('quarter', capture_date) AS quarter,
        COUNT(measurement_id) AS measurement_count,
        AVG(who_z_score) AS avg_z_score,
        100.0 * SUM(CASE WHEN status = 'Stunted' THEN 1 ELSE 0 END) / COUNT(*) AS stunting_rate,
        100.0 * SUM(CASE WHEN status = 'Severely Stunted' THEN 1 ELSE 0 END) / COUNT(*) AS severe_stunting_rate
    FROM MEASUREMENTS
    WHERE site_id = :selected_site_id
        AND is_duplicate = FALSE 
        AND flagged = FALSE
        AND capture_date >= DATEADD(year, -5, CURRENT_DATE())
    GROUP BY DATE_TRUNC('quarter', capture_date)
    ORDER BY quarter
)
SELECT 
    TO_CHAR(quarter, 'Mon YYYY') AS period,
    ROUND(stunting_rate, 1) AS stunting_rate,
    ROUND(severe_stunting_rate, 1) AS severe_stunting_rate,
    ROUND(avg_z_score, 2) AS avg_z_score
FROM quarterly_data;
```

**Visualization Specifications**:
- Line 1 (Left Y-axis): Stunting Rate % (Coral color)
- Line 2 (Left Y-axis): Severe Stunting Rate % (Red color)
- Line 3 (Right Y-axis): Avg Z-Score (Blue color)
- Both lines thick (3px)
- Markers visible
- Dual Y-axes labeled
- Height: 400px

#### 7.2.5 Chart 2: Number of Children by Category

**Chart Type**: Grouped Bar Chart  
**Library**: Plotly

**Data Query**:
```sql
WITH site_totals AS (
    SELECT COUNT(DISTINCT beneficiary_id) AS total
    FROM MEASUREMENTS
    WHERE site_id = :selected_site_id
        AND is_duplicate = FALSE
        AND flagged = FALSE
),
first_measurements AS (
    SELECT 
        beneficiary_id,
        status,
        ROW_NUMBER() OVER (PARTITION BY beneficiary_id ORDER BY capture_date) AS rn
    FROM MEASUREMENTS
    WHERE site_id = :selected_site_id
        AND is_duplicate = FALSE
        AND flagged = FALSE
),
last_measurements AS (
    SELECT 
        beneficiary_id,
        status,
        ROW_NUMBER() OVER (PARTITION BY beneficiary_id ORDER BY capture_date DESC) AS rn
    FROM MEASUREMENTS
    WHERE site_id = :selected_site_id
        AND is_duplicate = FALSE
        AND flagged = FALSE
)
SELECT 
    'First Measurement' AS measurement_period,
    SUM(CASE WHEN status = 'At Risk' THEN 1 ELSE 0 END) AS at_risk,
    SUM(CASE WHEN status = 'Stunted' THEN 1 ELSE 0 END) AS stunted,
    SUM(CASE WHEN status = 'Severely Stunted' THEN 1 ELSE 0 END) AS severely_stunted
FROM first_measurements
WHERE rn = 1

UNION ALL

SELECT 
    'Last Measurement' AS measurement_period,
    SUM(CASE WHEN status = 'At Risk' THEN 1 ELSE 0 END) AS at_risk,
    SUM(CASE WHEN status = 'Stunted' THEN 1 ELSE 0 END) AS stunted,
    SUM(CASE WHEN status = 'Severely Stunted' THEN 1 ELSE 0 END) AS severely_stunted
FROM last_measurements
WHERE rn = 1

UNION ALL

SELECT 
    'Target' AS measurement_period,
    CAST(total * 0.025 AS INTEGER) AS at_risk,
    CAST(total * 0.025 AS INTEGER) AS stunted,
    CAST(total * 0.0015 AS INTEGER) AS severely_stunted
FROM site_totals;
```

**Visualization Specifications**: Same as Overview page Chart 2

#### 7.2.6 Chart 3: Current Status Distribution

**Chart Type**: Bar Chart with colored bars  
**Library**: Plotly

**Data Query**:
```sql
WITH latest_measurements AS (
    SELECT 
        beneficiary_id,
        status,
        ROW_NUMBER() OVER (PARTITION BY beneficiary_id ORDER BY capture_date DESC) AS rn
    FROM MEASUREMENTS
    WHERE site_id = :selected_site_id
        AND is_duplicate = FALSE
        AND flagged = FALSE
)
SELECT 
    status AS category,
    COUNT(*) AS count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS percentage
FROM latest_measurements
WHERE rn = 1
GROUP BY status
ORDER BY FIELD(status, 'Normal', 'At Risk', 'Stunted', 'Severely Stunted');
```

**Visualization Specifications**:
- Each bar colored by category (Normal=Green, At Risk=Orange, etc.)
- Show count + percentage in tooltip
- Height: 400px

#### 7.2.7 Charts 4 & 5: Cross-Location Comparisons

**Chart 4: Z-Score Comparison**

**Data Query**:
```sql
SELECT 
    s.site_name,
    COUNT(DISTINCT m.beneficiary_id) AS children_count,
    ROUND(AVG(m.who_z_score), 2) AS avg_z_score,
    CASE WHEN s.site_id = :selected_site_id THEN 1 ELSE 0 END AS is_current
FROM SITES s
JOIN MEASUREMENTS m ON s.site_id = m.site_id
WHERE m.is_duplicate = FALSE 
    AND m.flagged = FALSE
    AND s.is_active = TRUE
GROUP BY s.site_id, s.site_name
ORDER BY children_count DESC;
```

**Visualization Specifications**:
- Horizontal bars
- Current location: Highlighted in purple with higher opacity
- Other locations: Blue with 60% opacity
- Sort: By children count (descending)
- Height: 400px

**Chart 5: Stunting Rate Comparison**

Similar structure, but:
- X-axis: Stunting rate (%)
- Color: Coral/red
- Sort: Ascending (lower is better)

#### 7.2.8 Chart 6: Measurement Volume Over Time

**Chart Type**: Area Chart  
**Library**: Plotly

**Data Query**:
```sql
SELECT 
    DATE_TRUNC('quarter', capture_date) AS quarter,
    TO_CHAR(DATE_TRUNC('quarter', capture_date), 'Mon YYYY') AS period,
    COUNT(measurement_id) AS measurement_count
FROM MEASUREMENTS
WHERE site_id = :selected_site_id
    AND is_duplicate = FALSE 
    AND flagged = FALSE
    AND capture_date >= DATEADD(year, -5, CURRENT_DATE())
GROUP BY DATE_TRUNC('quarter', capture_date)
ORDER BY quarter;
```

**Visualization Specifications**:
- Area fill: Purple with 60% opacity
- Line: Purple, 2px
- Height: 350px

---

### 7.3 Child Analysis Page

#### Layout Structure
```
┌─────────────────────────────────────────────────────────────┐
│                        Page Header                          │
│  Title: "Individual Child Analysis"                         │
│  Subtitle: "Track individual child growth trajectories"     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────┬─────────────────────────────────────┐
│ Location Dropdown   │ Child Search & Select Dropdown      │
│ [Select ▼]          │ [Search...] [Select Child ▼]       │
└─────────────────────┴─────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Child Profile Hero Card (Gradient Background)              │
│  Name | ID | Demographics | Current Status                  │
└─────────────────────────────────────────────────────────────┘

┌───────────┬───────────┬───────────┬───────────┐
│  Progress │  Progress │  Progress │  Progress │  ← KPI Cards
│  Metric 1 │  Metric 2 │  Metric 3 │  Metric 4 │
└───────────┴───────────┴───────────┴───────────┘

┌─────────────────────────────────────────────────────────────┐
│  Alert Banner (if applicable)                               │
│  ✓ Success / ⚠ Warning / ℹ Info                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Chart 1: Height Growth Trajectory (Line)                   │
│  [AI Interpretation Button]                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Chart 2: WHO Z-Score Progression (Area + Reference Lines)  │
│  [AI Interpretation Button]                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Table: Measurement History                                 │
│  Date | Age | Height | Z-Score | Status | Change           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  AI-Generated Progress Summary                              │
│  [Generate Summary Button]                                  │
└─────────────────────────────────────────────────────────────┘
```

#### 7.3.1 Child Selection Interface

**Location Dropdown**:
```python
# Same query as Location Analysis page
```

**Child Search Input**:
```python
# Streamlit text_input with debouncing
# Search across: first_names, last_name, beneficiary_id
```

**Child Dropdown**:
```python
# Query
SELECT 
    beneficiary_id,
    first_names,
    last_name,
    COUNT(measurement_id) AS measurement_count
FROM BENEFICIARIES b
LEFT JOIN MEASUREMENTS m ON b.beneficiary_id = m.beneficiary_id
WHERE b.site_id = :selected_site_id
    AND b.is_active = TRUE
    AND (
        LOWER(b.first_names) LIKE LOWER('%' || :search_term || '%')
        OR LOWER(b.last_name) LIKE LOWER('%' || :search_term || '%')
        OR CAST(b.beneficiary_id AS VARCHAR) LIKE '%' || :search_term || '%'
    )
GROUP BY beneficiary_id, first_names, last_name
ORDER BY first_names, last_name;

# Display format
# "Onthatile Molefe (ID: 161592)"
```

#### 7.3.2 Child Profile Card

**Data Query**:
```sql
SELECT 
    b.beneficiary_id,
    b.first_names,
    b.last_name,
    b.gender,
    b.date_of_birth,
    DATEDIFF(year, b.date_of_birth, CURRENT_DATE()) AS age_years,
    h.household_name,
    s.site_name,
    COUNT(m.measurement_id) AS total_measurements,
    
    -- Latest measurement
    FIRST_VALUE(m.who_z_score) OVER (ORDER BY m.capture_date DESC) AS latest_z_score,
    FIRST_VALUE(m.status) OVER (ORDER BY m.capture_date DESC) AS latest_status

FROM BENEFICIARIES b
LEFT JOIN MEASUREMENTS m ON b.beneficiary_id = m.beneficiary_id 
    AND m.is_duplicate = FALSE
    AND m.flagged = FALSE
LEFT JOIN HOUSEHOLDS h ON b.household_id = h.household_id
LEFT JOIN SITES s ON b.site_id = s.site_id
WHERE b.beneficiary_id = :selected_beneficiary_id
GROUP BY 
    b.beneficiary_id, b.first_names, b.last_name, b.gender, 
    b.date_of_birth, h.household_name, s.site_name;
```

**Display Elements**:
- Beneficiary ID (small, top-left)
- Full name (large, 32px)
- Demographics: Age | Gender | Measurements count
- Household name with map pin icon
- Current status badge (right side)
- Latest z-score (right side)
- Purple gradient background

#### 7.3.3 Progress Metric Cards

**Card 1: Height Gain**
```sql
SELECT 
    MAX(height_cm) - MIN(height_cm) AS height_gain_cm
FROM MEASUREMENTS
WHERE beneficiary_id = :selected_beneficiary_id
    AND is_duplicate = FALSE
    AND flagged = FALSE;
```
Display: "+13.0 cm | ↑ First to Last"

**Card 2: Z-Score Improvement**
```sql
WITH first_last AS (
    SELECT 
        FIRST_VALUE(who_z_score) OVER (ORDER BY capture_date) AS first_z,
        FIRST_VALUE(who_z_score) OVER (ORDER BY capture_date DESC) AS last_z
    FROM MEASUREMENTS
    WHERE beneficiary_id = :selected_beneficiary_id
        AND is_duplicate = FALSE
        AND flagged = FALSE
)
SELECT last_z - first_z AS z_score_improvement
FROM first_last
LIMIT 1;
```
Display: "+1.2 | ↑ Positive Trend"

**Card 3: Average Z-Score**
```sql
SELECT ROUND(AVG(who_z_score), 2) AS avg_z_score
FROM MEASUREMENTS
WHERE beneficiary_id = :selected_beneficiary_id
    AND is_duplicate = FALSE
    AND flagged = FALSE;
```
Display: "-0.55 | Across all measurements"

**Card 4: Monitoring Period**
```sql
SELECT 
    DATEDIFF(month, MIN(capture_date), MAX(capture_date)) AS months,
    COUNT(measurement_id) AS measurement_count
FROM MEASUREMENTS
WHERE beneficiary_id = :selected_beneficiary_id
    AND is_duplicate = FALSE
    AND flagged = FALSE;
```
Display: "18 mo | 6 measurements"

#### 7.3.4 Alert Banners

**Logic**:
```python
if last_status == 'Normal' and first_status != 'Normal':
    show_success_alert(
        title="Excellent Progress!",
        message=f"{child_name} has successfully moved from '{first_status}' to 'Normal' status..."
    )
elif last_status == 'At Risk' and first_status == 'Stunted':
    show_warning_alert(
        title="Positive Trend, Continued Monitoring Needed",
        message=f"{child_name} has improved from 'Stunted' to 'At Risk' status..."
    )
elif last_status in ['Stunted', 'Severely Stunted']:
    show_warning_alert(
        title="Requires Attention",
        message=f"{child_name} is currently classified as '{last_status}'..."
    )
```

#### 7.3.5 Chart 1: Height Growth Trajectory

**Chart Type**: Line Chart  
**Library**: Plotly

**Data Query**:
```sql
SELECT 
    capture_date,
    TO_CHAR(capture_date, 'YYYY-MM-DD') AS date_formatted,
    height_cm,
    who_z_score,
    status,
    ROUND(DATEDIFF(day, date_of_birth, capture_date) / 365.25, 1) AS age_years
FROM MEASUREMENTS m
JOIN BENEFICIARIES b ON m.beneficiary_id = b.beneficiary_id
WHERE m.beneficiary_id = :selected_beneficiary_id
    AND m.is_duplicate = FALSE
    AND m.flagged = FALSE
ORDER BY capture_date;
```

**Visualization Specifications**:
- X-axis: Date (formatted)
- Y-axis: Height (cm)
- Line: Blue, thick (3px)
- Markers: Large (radius 6px), filled
- Grid: Light gray
- Tooltip: Show date, age, height, status
- Height: 400px

#### 7.3.6 Chart 2: Z-Score Progression

**Chart Type**: Area Chart with Reference Lines  
**Library**: Plotly

**Data Query**: Same as Chart 1

**Visualization Specifications**:
- X-axis: Date
- Y-axis: Z-score (-3 to 1)
- Area: Purple with 40% opacity
- Line: Purple, thick
- Reference lines (dashed):
  - Red at -3 (Severe stunting threshold)
  - Orange at -2 (Stunting threshold)
  - Green at 0 (WHO median)
- Legend for reference lines
- Info box: WHO Normal Range -2 to +2
- Height: 400px

#### 7.3.7 Measurement History Table

**Component**: Streamlit dataframe (st.dataframe)

**Data Query**:
```sql
WITH measurements_with_change AS (
    SELECT 
        capture_date,
        TO_CHAR(capture_date, 'YYYY-MM-DD') AS date_formatted,
        ROUND(DATEDIFF(day, b.date_of_birth, capture_date) / 365.25, 1) AS age_years,
        height_cm,
        who_z_score,
        status,
        LAG(height_cm) OVER (ORDER BY capture_date) AS prev_height,
        LAG(who_z_score) OVER (ORDER BY capture_date) AS prev_z_score,
        ROW_NUMBER() OVER (ORDER BY capture_date) AS row_num
    FROM MEASUREMENTS m
    JOIN BENEFICIARIES b ON m.beneficiary_id = b.beneficiary_id
    WHERE m.beneficiary_id = :selected_beneficiary_id
        AND m.is_duplicate = FALSE
        AND m.flagged = FALSE
)
SELECT 
    date_formatted AS "Date",
    age_years AS "Age (years)",
    height_cm AS "Height (cm)",
    who_z_score AS "Z-Score",
    status AS "Status",
    CASE 
        WHEN row_num = 1 THEN 'First measurement'
        ELSE CONCAT(
            '+', 
            ROUND(height_cm - prev_height, 1), 
            ' cm | ',
            CASE WHEN who_z_score >= prev_z_score THEN '+' ELSE '' END,
            ROUND(who_z_score - prev_z_score, 2),
            ' z'
        )
    END AS "Change"
FROM measurements_with_change
ORDER BY capture_date;
```

**Table Formatting**:
- Status column: Color-coded badges
- Change column: Green for positive, red for negative
- Striped rows for readability
- Sortable columns
- Export button (CSV)

#### 7.3.8 AI Progress Summary

**Button**: "Generate AI Progress Summary"

**Prompt Template**:
```
You are analyzing the nutrition progress for an individual child in South Africa.

Child: {child_name} (ID: {beneficiary_id})
Age: {age} years | Gender: {gender}

Measurement History:
- Total measurements: {total_measurements}
- First measurement: {first_date} - Height: {first_height}cm, Z-score: {first_z_score}, Status: {first_status}
- Last measurement: {last_date} - Height: {last_height}cm, Z-score: {last_z_score}, Status: {last_status}
- Monitoring period: {months} months

Progress:
- Height gain: {height_gain}cm
- Z-score improvement: {z_score_improvement}
- Average Z-score: {avg_z_score}

Complete measurement history:
{measurement_table}

Provide a comprehensive 4-6 sentence progress summary in plain language for program staff and caregivers, covering:
1. Overall trajectory (improving/stable/declining)
2. Most significant milestones or changes
3. Current status and what it means
4. Recommendations for continued care
5. Any concerns or areas requiring attention

Be specific, compassionate, and action-oriented.
```

---

## 8. AI Integration Requirements

### 8.1 Claude API Configuration

**API Provider**: Anthropic Claude  
**Model**: `claude-sonnet-4-20250514`  
**SDK**: `anthropic` Python package

**Configuration**:
```python
# utils/ai_service.py

from anthropic import Anthropic
import streamlit as st

def get_claude_client():
    """Initialize Claude API client"""
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    return Anthropic(api_key=api_key)

def generate_interpretation(
    prompt: str,
    max_tokens: int = 1000,
    temperature: float = 0.7
) -> str:
    """
    Generate AI interpretation for a graph
    
    Args:
        prompt: The formatted prompt with context
        max_tokens: Maximum response length
        temperature: Creativity (0-1, default 0.7)
    
    Returns:
        AI-generated interpretation text
    """
    client = get_claude_client()
    
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return message.content[0].text
        
    except Exception as e:
        st.error(f"AI interpretation failed: {str(e)}")
        return "Unable to generate interpretation at this time. Please try again later."
```

### 8.2 Prompt Engineering Guidelines

**General Structure**:
```
Context: You are analyzing {domain} data for {audience}

Chart: {chart_name}
Data Summary:
{key_metrics}

Historical Context:
{trends}

Request: Provide a {length} interpretation covering:
1. {aspect_1}
2. {aspect_2}
3. {aspect_3}

Tone: {tone_guidance}
Constraints: {constraints}
```

**Domain-Specific Context**:
- Non-profit child nutrition program in South Africa
- Target audience: Program staff with varying technical skills
- WHO standards as reference (z-scores, growth charts)
- Cultural sensitivity required

**Tone Requirements**:
- Professional but accessible
- Data-driven and evidence-based
- Solution-oriented
- Compassionate when discussing individual children
- Avoid jargon; explain technical terms

**Output Constraints**:
- 3-6 sentences (150-250 words)
- Plain language (reading level: Grade 10-12)
- Specific numbers cited from data
- Actionable insights where appropriate

### 8.3 Caching Strategy

**Objective**: Reduce API costs and latency by caching interpretations

**Implementation**:
```python
# utils/ai_service.py

import hashlib
import json
from datetime import datetime, timedelta

def get_cache_key(graph_type: str, filters: dict, data_hash: str) -> str:
    """Generate unique cache key for interpretation"""
    cache_input = {
        "graph_type": graph_type,
        "filters": filters,
        "data_hash": data_hash
    }
    return hashlib.md5(
        json.dumps(cache_input, sort_keys=True).encode()
    ).hexdigest()

def get_cached_interpretation(
    graph_type: str,
    filters: dict,
    data: pd.DataFrame,
    ttl_hours: int = 24
) -> str or None:
    """
    Retrieve cached interpretation if valid
    
    Args:
        graph_type: Type of graph (e.g., 'stunting_progress')
        filters: Applied filters (location, date range, etc.)
        data: DataFrame used for visualization
        ttl_hours: Cache validity period
    
    Returns:
        Cached interpretation or None if not found/expired
    """
    # Generate data hash
    data_hash = hashlib.md5(
        pd.util.hash_pandas_object(data).values
    ).hexdigest()
    
    cache_key = get_cache_key(graph_type, filters, data_hash)
    
    # Query cache table
    query = f"""
    SELECT interpretation_text, generated_at
    FROM AI_INTERPRETATIONS
    WHERE interpretation_id = '{cache_key}'
        AND generated_at > DATEADD(hour, -{ttl_hours}, CURRENT_TIMESTAMP())
    """
    
    result = execute_query(query)
    
    if not result.empty:
        return result.iloc[0]['interpretation_text']
    
    return None

def cache_interpretation(
    graph_type: str,
    filters: dict,
    data: pd.DataFrame,
    interpretation: str,
    model_version: str = "claude-sonnet-4"
):
    """Save interpretation to cache"""
    data_hash = hashlib.md5(
        pd.util.hash_pandas_object(data).values
    ).hexdigest()
    
    cache_key = get_cache_key(graph_type, filters, data_hash)
    
    insert_query = f"""
    INSERT INTO AI_INTERPRETATIONS (
        interpretation_id,
        graph_type,
        filter_params,
        interpretation_text,
        model_version
    ) VALUES (
        '{cache_key}',
        '{graph_type}',
        PARSE_JSON('{json.dumps(filters)}'),
        '{interpretation.replace("'", "''")}',
        '{model_version}'
    )
    ON CONFLICT (interpretation_id) DO UPDATE
    SET interpretation_text = EXCLUDED.interpretation_text,
        generated_at = CURRENT_TIMESTAMP();
    """
    
    execute_query(insert_query)
```

### 8.4 Error Handling

**Scenarios**:
1. API rate limit exceeded
2. Network timeout
3. Invalid API key
4. Model unavailable
5. Token limit exceeded

**Implementation**:
```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from anthropic import RateLimitError, APITimeoutError

@retry(
    retry=retry_if_exception_type((RateLimitError, APITimeoutError)),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def generate_interpretation_with_retry(prompt: str) -> str:
    """Generate interpretation with automatic retry logic"""
    return generate_interpretation(prompt)

def safe_generate_interpretation(prompt: str) -> str:
    """
    Safely generate interpretation with comprehensive error handling
    """
    try:
        # Check cache first
        # (implementation omitted for brevity)
        
        # Generate new interpretation
        interpretation = generate_interpretation_with_retry(prompt)
        
        # Cache result
        # (implementation omitted for brevity)
        
        return interpretation
        
    except RateLimitError:
        return ("⚠️ AI interpretation temporarily unavailable due to high demand. "
                "Please try again in a few minutes.")
    
    except APITimeoutError:
        return ("⚠️ AI interpretation request timed out. "
                "The system may be experiencing high load.")
    
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return ("❌ Unable to generate AI interpretation. "
                "Please contact support if this persists.")
```

### 8.5 UI Components for AI Features

**Button Component**:
```python
# utils/ai_components.py

def ai_interpretation_button(
    graph_type: str,
    filters: dict,
    data: pd.DataFrame,
    key: str
) -> str or None:
    """
    Render AI interpretation button and display result
    
    Args:
        graph_type: Type of visualization
        filters: Applied filters
        data: Visualization data
        key: Unique key for Streamlit component
    
    Returns:
        Interpretation text if generated, else None
    """
    # Button styling
    st.markdown("""
    <style>
    .ai-button {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
    }
    .ai-button:hover {
        opacity: 0.9;
    }
    .ai-interpretation {
        background: #F7FAFC;
        border-left: 4px solid #667EEA;
        padding: 16px;
        border-radius: 8px;
        margin-top: 16px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if f"interpretation_{key}" not in st.session_state:
        st.session_state[f"interpretation_{key}"] = None
    
    # Button
    if st.button(
        "🤖 Get AI Interpretation",
        key=f"btn_{key}",
        type="primary"
    ):
        with st.spinner("Generating interpretation..."):
            # Check cache
            cached = get_cached_interpretation(
                graph_type, filters, data
            )
            
            if cached:
                interpretation = cached
            else:
                # Generate prompt
                prompt = create_prompt(graph_type, filters, data)
                
                # Generate interpretation
                interpretation = safe_generate_interpretation(prompt)
                
                # Cache result
                cache_interpretation(
                    graph_type, filters, data, interpretation
                )
            
            st.session_state[f"interpretation_{key}"] = interpretation
    
    # Display interpretation
    if st.session_state[f"interpretation_{key}"]:
        st.markdown(
            f"""
            <div class="ai-interpretation">
                <strong>🤖 AI Analysis:</strong><br>
                {st.session_state[f"interpretation_{key}"]}
            </div>
            """,
            unsafe_allow_html=True
        )
        
        return st.session_state[f"interpretation_{key}"]
    
    return None
```

---

## 9. UI/UX Requirements

### 9.1 Design System

**Color Palette**:
```python
# config/app_config.py

COLORS = {
    # Status Colors
    "normal": "#68D391",         # Green
    "at_risk": "#F6AD55",        # Orange
    "stunted": "#FC8181",        # Coral
    "severely_stunted": "#E53E3E", # Red
    
    # Primary Colors
    "primary": "#4299E1",        # Blue
    "secondary": "#9F7AEA",      # Purple
    
    # Neutral Colors
    "text_primary": "#2D3748",
    "text_secondary": "#718096",
    "text_muted": "#A0AEC0",
    "border": "#E2E8F0",
    "background": "#F7FAFC",
    
    # Gradients
    "gradient_purple": "linear-gradient(135deg, #667EEA 0%, #764BA2 100%)",
    "gradient_blue": "linear-gradient(135deg, #4299E1 0%, #2B6CB0 100%)"
}
```

**Typography**:
```python
TYPOGRAPHY = {
    "font_family": "'Inter', 'Segoe UI', sans-serif",
    
    "font_sizes": {
        "h1": "32px",
        "h2": "24px",
        "h3": "18px",
        "body": "16px",
        "small": "14px",
        "tiny": "12px"
    },
    
    "font_weights": {
        "normal": 400,
        "medium": 500,
        "semibold": 600,
        "bold": 700
    }
}
```

**Spacing**:
```python
SPACING = {
    "xs": "4px",
    "sm": "8px",
    "md": "16px",
    "lg": "24px",
    "xl": "32px",
    "xxl": "48px"
}
```

### 9.2 Component Library

**Metric Card**:
```python
def metric_card(
    title: str,
    value: str,
    subtitle: str = None,
    icon: str = None,
    trend: float = None,
    color: str = COLORS["primary"]
):
    """
    Display a metric card
    
    Args:
        title: Metric name
        value: Main value to display
        subtitle: Optional subtitle text
        icon: Optional emoji/icon
        trend: Optional trend percentage (positive or negative)
        color: Accent color
    """
    trend_html = ""
    if trend is not None:
        trend_color = "#48BB78" if trend > 0 else "#F56565"
        trend_arrow = "↑" if trend > 0 else "↓"
        trend_html = f"""
        <div style="color: {trend_color}; font-size: 14px; font-weight: 600;">
            {trend_arrow} {abs(trend)}%
        </div>
        """
    
    st.markdown(f"""
    <div style="
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid {COLORS['border']};
    ">
        <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
            <div style="
                width: 48px;
                height: 48px;
                border-radius: 12px;
                background: {color}20;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
            ">
                {icon or ''}
            </div>
            {trend_html}
        </div>
        <div style="font-size: 28px; font-weight: bold; color: {COLORS['text_primary']}; margin-bottom: 4px;">
            {value}
        </div>
        <div style="font-size: 14px; color: {COLORS['text_secondary']}; margin-bottom: 4px;">
            {title}
        </div>
        {f'<div style="font-size: 12px; color: {COLORS["text_muted"]};">{subtitle}</div>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)
```

**Status Badge**:
```python
def status_badge(status: str):
    """Display a colored status badge"""
    colors = {
        "Normal": {"bg": "#C6F6D5", "text": "#22543D", "icon": "✓"},
        "At Risk": {"bg": "#FEEBC8", "text": "#7C2D12", "icon": "⚠"},
        "Stunted": {"bg": "#FED7D7", "text": "#742A2A", "icon": "⚠"},
        "Severely Stunted": {"bg": "#FED7D7", "text": "#742A2A", "icon": "⚠"}
    }
    
    style = colors.get(status, colors["Normal"])
    
    return f"""
    <span style="
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 4px 12px;
        background: {style['bg']};
        color: {style['text']};
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    ">
        {style['icon']} {status}
    </span>
    """
```

**Alert Banner**:
```python
def alert_banner(
    type: str,  # 'success', 'warning', 'info', 'error'
    title: str,
    message: str
):
    """Display an alert banner"""
    styles = {
        "success": {"bg": "#C6F6D5", "border": "#68D391", "icon": "✅"},
        "warning": {"bg": "#FEEBC8", "border": "#F6AD55", "icon": "⚠️"},
        "info": {"bg": "#BEE3F8", "border": "#4299E1", "icon": "ℹ️"},
        "error": {"bg": "#FED7D7", "border": "#FC8181", "icon": "❌"}
    }
    
    style = styles.get(type, styles["info"])
    
    st.markdown(f"""
    <div style="
        background: {style['bg']};
        border: 2px solid {style['border']};
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
    ">
        <div style="display: flex; gap: 12px; align-items: flex-start;">
            <span style="font-size: 24px;">{style['icon']}</span>
            <div>
                <div style="font-weight: 600; margin-bottom: 4px;">{title}</div>
                <div style="font-size: 14px; line-height: 1.5;">{message}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
```

### 9.3 Responsive Design

**Breakpoints**:
```python
BREAKPOINTS = {
    "mobile": 576,
    "tablet": 768,
    "desktop": 1024,
    "wide": 1440
}
```

**Layout Adaptations**:
- **Desktop (>1024px)**: Full 3-column layouts, side-by-side charts
- **Tablet (768-1024px)**: 2-column layouts, stacked charts
- **Mobile (<768px)**: Single column, simplified visualizations

**Implementation**:
```python
# Check viewport width
viewport_width = st.session_state.get('viewport_width', 1440)

if viewport_width < BREAKPOINTS['tablet']:
    # Mobile layout
    cols = [1]  # Single column
    chart_height = 300
else:
    # Desktop layout
    cols = st.columns([1, 1])
    chart_height = 400
```

### 9.4 Loading States

**Spinner for Data Queries**:
```python
with st.spinner("Loading data..."):
    data = fetch_data_from_snowflake(query)
```

**Progress Bar for Long Operations**:
```python
progress_bar = st.progress(0)
for i, item in enumerate(items):
    process_item(item)
    progress_bar.progress((i + 1) / len(items))
progress_bar.empty()
```

**Skeleton Screens for Charts**:
```python
if data is None:
    st.markdown("""
    <div style="
        height: 400px;
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: loading 1.5s ease-in-out infinite;
        border-radius: 8px;
    "></div>
    <style>
    @keyframes loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    </style>
    """, unsafe_allow_html=True)
else:
    render_chart(data)
```

### 9.5 Accessibility

**WCAG 2.1 AA Compliance**:
- Color contrast ratio ≥ 4.5:1 for normal text
- Color contrast ratio ≥ 3:1 for large text (18px+)
- All interactive elements keyboard accessible
- Screen reader support for charts (alt text)

**Implementation**:
```python
# Chart accessibility
fig = go.Figure(...)
fig.update_layout(
    title={
        'text': 'Chart Title',
        'accessible': 'Descriptive chart title for screen readers'
    }
)

# Button accessibility
st.button(
    "Get AI Interpretation",
    key="ai_btn",
    help="Generate an AI-powered interpretation of this chart"
)
```

---

## 10. Performance Requirements

### 10.1 Load Time Targets

| Metric | Target | Maximum |
|--------|--------|---------|
| Initial page load | < 2 seconds | < 3 seconds |
| Page navigation | < 500ms | < 1 second |
| Data refresh | < 3 seconds | < 5 seconds |
| AI interpretation | < 2 seconds | < 5 seconds |
| Chart rendering | < 1 second | < 2 seconds |

### 10.2 Data Optimization

**Query Optimization**:
```sql
-- Use materialized views for frequently accessed aggregations
CREATE MATERIALIZED VIEW MV_SITE_DAILY_METRICS AS
SELECT 
    site_id,
    DATE(capture_date) AS measurement_date,
    COUNT(DISTINCT beneficiary_id) AS daily_children,
    AVG(who_z_score) AS avg_z_score,
    -- ... other metrics
FROM MEASUREMENTS
GROUP BY site_id, DATE(capture_date);

-- Refresh daily
ALTER MATERIALIZED VIEW MV_SITE_DAILY_METRICS REFRESH;
```

**Caching Strategy**:
```python
import streamlit as st
from functools import lru_cache

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_overview_data():
    """Fetch overview page data with caching"""
    return execute_query(OVERVIEW_QUERY)

@st.cache_data(ttl=1800)  # Cache for 30 minutes
def fetch_location_data(site_id: str):
    """Fetch location-specific data with caching"""
    return execute_query(LOCATION_QUERY, {"site_id": site_id})

@st.cache_data(ttl=3600)
def fetch_child_data(beneficiary_id: int):
    """Fetch individual child data with caching"""
    return execute_query(CHILD_QUERY, {"beneficiary_id": beneficiary_id})
```

**Data Pagination**:
```python
# For large tables (measurement history)
def paginated_dataframe(df: pd.DataFrame, page_size: int = 50):
    """Display dataframe with pagination"""
    total_pages = len(df) // page_size + (1 if len(df) % page_size > 0 else 0)
    
    page = st.number_input(
        "Page",
        min_value=1,
        max_value=total_pages,
        value=1
    )
    
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    st.dataframe(df.iloc[start_idx:end_idx])
```

### 10.3 Chart Performance

**Plotly Configuration**:
```python
def create_optimized_chart(fig):
    """Apply performance optimizations to Plotly charts"""
    fig.update_layout(
        # Disable features that impact performance
        hovermode='closest',  # Instead of 'x' or 'y'
        
        # Reduce rendering complexity
        plot_bgcolor='white',
        
        # Optimize for speed
        autosize=True,
    )
    
    # Display with Streamlit
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            'displayModeBar': False,  # Hide toolbar
            'staticPlot': False,      # Allow interactivity
        }
    )
```

**Data Downsampling**:
```python
def downsample_temporal_data(df: pd.DataFrame, max_points: int = 100):
    """
    Downsample time series data for performance
    
    Args:
        df: DataFrame with datetime index
        max_points: Maximum number of data points to display
    
    Returns:
        Downsampled DataFrame
    """
    if len(df) <= max_points:
        return df
    
    # Use pandas resample for time series
    freq = f'{len(df) // max_points}D'  # Daily frequency
    return df.resample(freq).mean()
```

### 10.4 Concurrent Users

**Target**: Support 50+ concurrent users

**Snowflake Configuration**:
```python
# config/database_config.py

SNOWFLAKE_CONFIG = {
    "account": st.secrets["snowflake"]["account"],
    "user": st.secrets["snowflake"]["user"],
    "password": st.secrets["snowflake"]["password"],
    "warehouse": "NUTRITION_WH",  # Medium warehouse
    "database": "NUTRITION_DB",
    "schema": "IMPACT_TRACKING",
    
    # Connection pooling
    "session_parameters": {
        "QUERY_TAG": "streamlit_dashboard",
        "STATEMENT_TIMEOUT_IN_SECONDS": 120
    }
}
```

**Connection Pooling**:
```python
from snowflake.connector.connection import SnowflakeConnection
from queue import Queue
import threading

class SnowflakeConnectionPool:
    """Thread-safe connection pool for Snowflake"""
    
    def __init__(self, config: dict, pool_size: int = 5):
        self.config = config
        self.pool = Queue(maxsize=pool_size)
        self.lock = threading.Lock()
        
        # Initialize pool
        for _ in range(pool_size):
            conn = snowflake.connector.connect(**config)
            self.pool.put(conn)
    
    def get_connection(self) -> SnowflakeConnection:
        """Get a connection from the pool"""
        return self.pool.get()
    
    def return_connection(self, conn: SnowflakeConnection):
        """Return a connection to the pool"""
        self.pool.put(conn)
    
    def execute_query(self, query: str, params: dict = None):
        """Execute a query using a pooled connection"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or {})
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return pd.DataFrame(results, columns=columns)
        finally:
            self.return_connection(conn)

# Global pool instance
connection_pool = SnowflakeConnectionPool(SNOWFLAKE_CONFIG)
```

---

## 11. Security & Privacy

### 11.1 Authentication

**Requirement**: Role-based access control (RBAC)

**User Roles**:
1. **Admin**: Full access to all data and features
2. **Program Manager**: Access to all sites, read-only
3. **Site Coordinator**: Access to assigned site(s) only
4. **Viewer**: Limited access to aggregated data only

**Implementation Options**:

**Option A: Streamlit Built-in Auth** (Simple)
```python
# .streamlit/config.toml
[client]
showErrorDetails = false

# pages/login.py
import streamlit as st

def check_credentials(username: str, password: str) -> dict or None:
    """Validate credentials against user database"""
    query = """
    SELECT user_id, role, assigned_sites
    FROM USERS
    WHERE username = :username
        AND password_hash = SHA2(:password, 256)
        AND is_active = TRUE
    """
    
    result = execute_query(query, {
        "username": username,
        "password": password
    })
    
    if not result.empty:
        return result.iloc[0].to_dict()
    return None

def login_page():
    """Display login form"""
    st.title("Child Nutrition Dashboard")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            user = check_credentials(username, password)
            if user:
                st.session_state["user"] = user
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Invalid credentials")

# Main app
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login_page()
else:
    # Render main dashboard
    show_dashboard()
```

**Option B: Auth0 Integration** (Production-grade)
```python
from auth0 import Auth0

# config/auth_config.py
AUTH0_CONFIG = {
    "domain": st.secrets["auth0"]["domain"],
    "client_id": st.secrets["auth0"]["client_id"],
    "client_secret": st.secrets["auth0"]["client_secret"],
    "redirect_uri": st.secrets["auth0"]["redirect_uri"]
}

def get_auth0_client():
    """Initialize Auth0 client"""
    return Auth0(
        domain=AUTH0_CONFIG["domain"],
        client_id=AUTH0_CONFIG["client_id"],
        client_secret=AUTH0_CONFIG["client_secret"]
    )
```

### 11.2 Data Privacy

**PII Protection**:
- Child names: Display with option to anonymize
- Beneficiary IDs: Show only to authorized users
- Contact information: Restricted to Admin role

**Anonymization Function**:
```python
def anonymize_child_name(name: str, user_role: str) -> str:
    """
    Anonymize child names based on user role
    
    Args:
        name: Full child name
        user_role: Current user's role
    
    Returns:
        Anonymized or full name based on permissions
    """
    if user_role in ["Admin", "Site Coordinator"]:
        return name
    else:
        # Show only first initial + last name initial
        parts = name.split()
        if len(parts) >= 2:
            return f"{parts[0][0]}. {parts[-1][0]}."
        return f"{name[0]}."

# Usage in child table
df["Child Name"] = df["Child Name"].apply(
    lambda x: anonymize_child_name(x, st.session_state["user"]["role"])
)
```

**Data Filtering by Role**:
```python
def apply_role_based_filter(query: str, user: dict) -> str:
    """
    Modify query based on user role and permissions
    
    Args:
        query: Base SQL query
        user: User dict with role and assigned_sites
    
    Returns:
        Modified query with role-based filters
    """
    role = user["role"]
    
    if role == "Admin":
        # No filtering
        return query
    
    elif role == "Site Coordinator":
        # Filter to assigned sites only
        assigned_sites = user["assigned_sites"].split(",")
        site_filter = "', '".join(assigned_sites)
        return query + f" AND site_id IN ('{site_filter}')"
    
    elif role == "Viewer":
        # Aggregate data only, no individual children
        return query.replace(
            "SELECT *",
            "SELECT site_id, COUNT(*) as count, AVG(who_z_score) as avg_z_score"
        )
    
    return query
```

### 11.3 API Security

**Secrets Management**:
```toml
# .streamlit/secrets.toml (NOT committed to git)

[snowflake]
account = "xy12345.us-east-1"
user = "dashboard_user"
password = "secure_password_here"
warehouse = "NUTRITION_WH"
database = "NUTRITION_DB"
schema = "IMPACT_TRACKING"

[anthropic]
api_key = "sk-ant-api03-..."

[auth0]
domain = "nutrition-dashboard.auth0.com"
client_id = "abc123..."
client_secret = "xyz789..."
redirect_uri = "https://nutrition-dashboard.streamlit.app/callback"
```

**Environment Variables** (for deployment):
```bash
# Snowflake
export SNOWFLAKE_ACCOUNT="xy12345.us-east-1"
export SNOWFLAKE_USER="dashboard_user"
export SNOWFLAKE_PASSWORD="secure_password"

# Anthropic
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# Auth0
export AUTH0_DOMAIN="nutrition-dashboard.auth0.com"
export AUTH0_CLIENT_ID="abc123"
export AUTH0_CLIENT_SECRET="xyz789"
```

**API Rate Limiting**:
```python
from datetime import datetime, timedelta
import streamlit as st

def check_rate_limit(
    user_id: str,
    action: str,
    max_requests: int = 100,
    window_minutes: int = 60
) -> bool:
    """
    Check if user has exceeded rate limit
    
    Args:
        user_id: User identifier
        action: Action type (e.g., 'ai_interpretation')
        max_requests: Maximum requests in window
        window_minutes: Time window in minutes
    
    Returns:
        True if within limit, False if exceeded
    """
    key = f"rate_limit_{user_id}_{action}"
    
    if key not in st.session_state:
        st.session_state[key] = []
    
    # Clean old requests
    cutoff = datetime.now() - timedelta(minutes=window_minutes)
    st.session_state[key] = [
        req for req in st.session_state[key]
        if req > cutoff
    ]
    
    # Check limit
    if len(st.session_state[key]) >= max_requests:
        return False
    
    # Add current request
    st.session_state[key].append(datetime.now())
    return True

# Usage
if not check_rate_limit(user_id, "ai_interpretation", max_requests=50):
    st.error("Rate limit exceeded. Please try again later.")
else:
    generate_ai_interpretation()
```

### 11.4 Audit Logging

**Log Events**:
- User login/logout
- Data access (which pages, filters applied)
- AI interpretation requests
- Data exports
- Administrative actions

**Implementation**:
```python
def log_event(
    user_id: str,
    event_type: str,
    event_details: dict,
    ip_address: str = None
):
    """
    Log user activity for audit trail
    
    Args:
        user_id: User identifier
        event_type: Type of event (login, data_access, export, etc.)
        event_details: Additional event metadata
        ip_address: User's IP address
    """
    query = """
    INSERT INTO AUDIT_LOG (
        user_id,
        event_type,
        event_details,
        ip_address,
        timestamp
    ) VALUES (
        :user_id,
        :event_type,
        PARSE_JSON(:event_details),
        :ip_address,
        CURRENT_TIMESTAMP()
    )
    """
    
    execute_query(query, {
        "user_id": user_id,
        "event_type": event_type,
        "event_details": json.dumps(event_details),
        "ip_address": ip_address or "unknown"
    })

# Usage examples
log_event(
    user_id=st.session_state["user"]["user_id"],
    event_type="page_view",
    event_details={"page": "Overview"}
)

log_event(
    user_id=st.session_state["user"]["user_id"],
    event_type="data_export",
    event_details={
        "export_type": "csv",
        "page": "Child Analysis",
        "filters": {"site_id": "ABC123"}
    }
)
```

---

## 12. Testing Requirements

### 12.1 Unit Tests

**Coverage Target**: ≥ 80% code coverage

**Test Framework**: pytest

**Example Tests**:
```python
# tests/test_data_processing.py

import pytest
from utils.data_processing import calculate_z_score_improvement

def test_z_score_improvement_positive():
    """Test z-score improvement calculation with positive change"""
    first_z = -1.5
    last_z = -0.5
    
    improvement = calculate_z_score_improvement(first_z, last_z)
    
    assert improvement == 1.0

def test_z_score_improvement_negative():
    """Test z-score improvement calculation with negative change"""
    first_z = -0.5
    last_z = -1.5
    
    improvement = calculate_z_score_improvement(first_z, last_z)
    
    assert improvement == -1.0

def test_z_score_improvement_no_change():
    """Test z-score improvement when no change occurs"""
    first_z = -1.0
    last_z = -1.0
    
    improvement = calculate_z_score_improvement(first_z, last_z)
    
    assert improvement == 0.0

# tests/test_database.py

import pytest
from utils.database import sanitize_query_params

def test_sanitize_query_params_sql_injection():
    """Test SQL injection prevention"""
    malicious_input = "'; DROP TABLE measurements; --"
    
    sanitized = sanitize_query_params(malicious_input)
    
    assert "DROP" not in sanitized
    assert "--" not in sanitized

def test_sanitize_query_params_normal_input():
    """Test that normal input is preserved"""
    normal_input = "Sasolburg"
    
    sanitized = sanitize_query_params(normal_input)
    
    assert sanitized == normal_input
```

### 12.2 Integration Tests

**Test Database Connection**:
```python
# tests/test_integration.py

import pytest
from utils.database import get_connection, execute_query

def test_snowflake_connection():
    """Test Snowflake database connection"""
    conn = get_connection()
    assert conn is not None
    
    # Test simple query
    result = execute_query("SELECT 1 as test")
    assert not result.empty
    assert result.iloc[0]['test'] == 1

def test_overview_data_query():
    """Test overview page data query"""
    from pages.overview import fetch_overview_data
    
    data = fetch_overview_data()
    
    assert data is not None
    assert 'total_children' in data
    assert 'avg_z_score' in data
    assert data['total_children'] > 0
```

**Test AI Integration**:
```python
def test_ai_interpretation_generation():
    """Test AI interpretation generation"""
    from utils.ai_service import generate_interpretation
    
    prompt = "Interpret this test data: Stunting rate decreased from 21% to 15%."
    
    interpretation = generate_interpretation(prompt)
    
    assert interpretation is not None
    assert len(interpretation) > 50
    assert "15%" in interpretation or "21%" in interpretation

@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="API key not available"
)
def test_ai_interpretation_caching():
    """Test that AI interpretations are cached"""
    from utils.ai_service import get_cached_interpretation, cache_interpretation
    import pandas as pd
    
    graph_type = "test_graph"
    filters = {"site": "TestSite"}
    data = pd.DataFrame({"value": [1, 2, 3]})
    interpretation = "Test interpretation"
    
    # Cache interpretation
    cache_interpretation(graph_type, filters, data, interpretation)
    
    # Retrieve from cache
    cached = get_cached_interpretation(graph_type, filters, data)
    
    assert cached == interpretation
```

### 12.3 End-to-End Tests

**User Journey Tests**:
```python
# tests/test_e2e.py

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    """Initialize Selenium WebDriver"""
    driver = webdriver.Chrome()
    driver.get("http://localhost:8501")
    yield driver
    driver.quit()

def test_overview_page_loads(driver):
    """Test that overview page loads successfully"""
    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    
    # Check page title
    title = driver.find_element(By.TAG_NAME, "h1").text
    assert "Program Overview" in title
    
    # Check metric cards are present
    metrics = driver.find_elements(By.CLASS_NAME, "metric-card")
    assert len(metrics) == 4

def test_location_analysis_workflow(driver):
    """Test complete location analysis workflow"""
    # Navigate to Location Analysis
    location_link = driver.find_element(By.LINK_TEXT, "Location Analysis")
    location_link.click()
    
    # Wait for page load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "select"))
    )
    
    # Select a location
    location_dropdown = driver.find_element(By.TAG_NAME, "select")
    location_dropdown.send_keys("Sasolburg")
    
    # Wait for data to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "plotly"))
    )
    
    # Verify charts are displayed
    charts = driver.find_elements(By.CLASS_NAME, "plotly")
    assert len(charts) >= 6

def test_ai_interpretation_generation(driver):
    """Test AI interpretation button and response"""
    # Click AI interpretation button
    ai_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.TEXT, "🤖 Get AI Interpretation"))
    )
    ai_button.click()
    
    # Wait for interpretation to load
    interpretation = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ai-interpretation"))
    )
    
    # Verify interpretation is displayed
    assert len(interpretation.text) > 50
```

### 12.4 Performance Tests

**Load Testing**:
```python
# tests/test_performance.py

import pytest
import time
from locust import HttpUser, task, between

class DashboardUser(HttpUser):
    """Simulated dashboard user for load testing"""
    
    wait_time = between(2, 5)  # Wait 2-5 seconds between requests
    
    @task(3)
    def view_overview(self):
        """View overview page (most common action)"""
        self.client.get("/")
    
    @task(2)
    def view_location_analysis(self):
        """View location analysis page"""
        self.client.get("/Location_Analysis")
    
    @task(1)
    def view_child_analysis(self):
        """View child analysis page"""
        self.client.get("/Child_Analysis")
    
    @task(1)
    def generate_ai_interpretation(self):
        """Request AI interpretation"""
        self.client.post("/ai/interpret", json={
            "graph_type": "stunting_progress",
            "data": {}
        })

# Run with: locust -f tests/test_performance.py --host=http://localhost:8501
```

**Query Performance Tests**:
```python
def test_overview_query_performance():
    """Test that overview query completes in < 3 seconds"""
    import time
    from pages.overview import fetch_overview_data
    
    start = time.time()
    data = fetch_overview_data()
    duration = time.time() - start
    
    assert duration < 3.0, f"Query took {duration:.2f}s (target: < 3s)"
    assert data is not None

def test_location_query_performance():
    """Test that location-specific query completes in < 2 seconds"""
    import time
    from pages.location import fetch_location_data
    
    start = time.time()
    data = fetch_location_data("Sasolburg")
    duration = time.time() - start
    
    assert duration < 2.0, f"Query took {duration:.2f}s (target: < 2s)"
    assert data is not None
```

### 12.5 User Acceptance Testing (UAT)

**UAT Checklist**:

**Overview Page**:
- [ ] All metric cards display correct values
- [ ] Charts render without errors
- [ ] AI interpretations generate successfully
- [ ] Data refresh updates all visualizations
- [ ] Export functionality works
- [ ] Page loads within 3 seconds

**Location Analysis Page**:
- [ ] Location dropdown populates correctly
- [ ] Selecting location updates all charts
- [ ] Ranking cards show accurate comparisons
- [ ] Temporal trends display correctly
- [ ] Cross-location comparisons are accurate
- [ ] Page transitions smoothly from Overview

**Child Analysis Page**:
- [ ] Location and child dropdowns work
- [ ] Search functionality filters children correctly
- [ ] Child profile displays accurate information
- [ ] Growth charts render correctly
- [ ] Z-score chart shows WHO reference lines
- [ ] Measurement history table is complete
- [ ] AI progress summary is relevant and accurate

**Cross-Cutting Concerns**:
- [ ] Navigation works smoothly between pages
- [ ] Session state persists correctly
- [ ] Error messages are user-friendly
- [ ] Loading states display appropriately
- [ ] Mobile layout is functional
- [ ] Authentication works correctly
- [ ] Role-based access control enforced

---

## 13. Deployment & Infrastructure

### 13.1 Deployment Options

#### Option A: Streamlit Cloud (Recommended for MVP)

**Pros**:
- Easiest setup
- Free tier available
- Automatic scaling
- HTTPS included
- Git integration

**Setup**:
1. Push code to GitHub repository
2. Connect repository to Streamlit Cloud
3. Configure secrets in Streamlit Cloud dashboard
4. Deploy with one click

**Configuration**:
```toml
# .streamlit/config.toml

[theme]
primaryColor = "#4299E1"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F7FAFC"
textColor = "#2D3748"
font = "sans serif"

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 200

[browser]
gatherUsageStats = false

[runner]
magicEnabled = true
fastReruns = true
```

#### Option B: AWS ECS (Production)

**Architecture**:
```
┌─────────────────┐
│   Route 53 DNS  │
└────────┬────────┘
         │
┌────────▼────────┐
│  CloudFront CDN │
└────────┬────────┘
         │
┌────────▼────────┐
│  ALB (HTTPS)    │
└────────┬────────┘
         │
┌────────▼────────┐
│   ECS Cluster   │
│  ┌────────────┐ │
│  │ Streamlit  │ │ (Auto-scaling: 2-10 tasks)
│  │  Container │ │
│  └────────────┘ │
└─────────────────┘
         │
    ┌────▼─────┬────────────┐
    │          │            │
┌───▼───┐ ┌───▼───┐ ┌─────▼──────┐
│Snowfl.│ │Claude │ │  Secrets   │
│   DB  │ │  API  │ │  Manager   │
└───────┘ └───────┘ └────────────┘
```

**Dockerfile**:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**docker-compose.yml** (for local testing):
```yaml
version: '3.8'

services:
  dashboard:
    build: .
    ports:
      - "8501:8501"
    environment:
      - SNOWFLAKE_ACCOUNT=${SNOWFLAKE_ACCOUNT}
      - SNOWFLAKE_USER=${SNOWFLAKE_USER}
      - SNOWFLAKE_PASSWORD=${SNOWFLAKE_PASSWORD}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - .:/app
    restart: unless-stopped
```

**ECS Task Definition**:
```json
{
  "family": "nutrition-dashboard",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "streamlit-app",
      "image": "${ECR_REPO}:latest",
      "portMappings": [
        {
          "containerPort": 8501,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "SNOWFLAKE_ACCOUNT",
          "value": "${SNOWFLAKE_ACCOUNT}"
        }
      ],
      "secrets": [
        {
          "name": "SNOWFLAKE_PASSWORD",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:snowflake-password"
        },
        {
          "name": "ANTHROPIC_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:anthropic-api-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/nutrition-dashboard",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

**Auto-scaling Policy**:
```json
{
  "TargetTrackingScalingPolicyConfiguration": {
    "TargetValue": 75.0,
    "PredefinedMetricSpecification": {
      "PredefinedMetricType": "ECSServiceAverageCPUUtilization"
    },
    "ScaleInCooldown": 300,
    "ScaleOutCooldown": 60
  }
}
```

### 13.2 CI/CD Pipeline

**GitHub Actions Workflow**:
```yaml
# .github/workflows/deploy.yml

name: Deploy to Production

on:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: |
          pytest tests/ --cov=. --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
  
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
      
      - name: Build and push Docker image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: nutrition-dashboard
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          docker tag $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG $ECR_REGISTRY/$ECR_REPOSITORY:latest
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster nutrition-dashboard-cluster \
            --service nutrition-dashboard-service \
            --force-new-deployment
```

### 13.3 Monitoring & Logging

**CloudWatch Metrics**:
- CPU utilization
- Memory utilization
- Request count
- Response time
- Error rate

**Application Logging**:
```python
# utils/logging.py

import logging
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def log_event(event_type: str, details: dict):
    """Log structured event"""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "details": details
    }
    logger.info(json.dumps(log_entry))

# Usage
log_event("page_view", {"page": "Overview", "user_id": "user123"})
log_event("query_executed", {"query_type": "overview_data", "duration_ms": 1250})
log_event("ai_interpretation", {"graph_type": "stunting_progress", "success": True})
```

**Health Check Endpoint**:
```python
# app.py

import streamlit as st
from datetime import datetime

def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check database connection
        test_query = "SELECT 1"
        execute_query(test_query)
        
        # Check AI service
        test_prompt = "Test"
        generate_interpretation(test_prompt)
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "checks": {
                "database": "ok",
                "ai_service": "ok"
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }
```

### 13.4 Backup & Disaster Recovery

**Snowflake Backups**:
```sql
-- Create fail-safe backup (7-day retention)
ALTER ACCOUNT SET DATA_RETENTION_TIME_IN_DAYS = 7;

-- Create long-term backup
CREATE TABLE MEASUREMENTS_BACKUP AS
SELECT * FROM MEASUREMENTS;
```

**Application State Backup**:
```python
# Backup AI interpretation cache weekly
def backup_ai_cache():
    """Export AI interpretation cache to S3"""
    import boto3
    from datetime import datetime
    
    query = "SELECT * FROM AI_INTERPRETATIONS"
    cache_data = execute_query(query)
    
    # Save to S3
    s3 = boto3.client('s3')
    backup_key = f"backups/ai_cache_{datetime.now().strftime('%Y%m%d')}.csv"
    
    s3.put_object(
        Bucket='nutrition-dashboard-backups',
        Key=backup_key,
        Body=cache_data.to_csv(index=False)
    )
```

---

## 14. Future Enhancements

### Phase 2 Features (3-6 months)

**1. Advanced Filtering**
- Date range selector for all pages
- Multi-site comparison on Location Analysis
- Cohort analysis (children enrolled in same period)

**2. Predictive Analytics**
- ML model to predict stunting risk
- Forecast growth trajectories
- Identify children likely to fall behind

**3. Automated Reports**
- Scheduled PDF report generation
- Email delivery to stakeholders
- Custom report templates

**4. Mobile App**
- Native mobile application
- Offline data collection
- Photo capture for visual progress tracking

**5. Data Quality Dashboard**
- Flagged records review interface
- Data quality score trends
- Missing data alerts

### Phase 3 Features (6-12 months)

**1. Multi-Language Support**
- English, Afrikaans, Zulu, Xhosa
- Dynamic language switching
- Localized date/number formats

**2. Integration APIs**
- REST API for external systems
- Webhook notifications for critical events
- Data export automation

**3. Advanced AI Features**
- Natural language queries ("Show me children at risk in Sasolburg")
- Automated insight detection
- Recommendation engine for interventions

**4. Geospatial Analysis**
- Interactive maps
- Geographic clustering analysis
- Distance to healthcare facilities

**5. Weight & BMI Tracking**
- Expand beyond height measurements
- WHO BMI-for-age calculations
- Composite nutrition indicators

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **Beneficiary** | A child enrolled in the nutrition program |
| **ECD** | Early Childhood Development center or facility |
| **Stunting** | Height-for-age z-score below -2 standard deviations from WHO median |
| **Severe Stunting** | Height-for-age z-score below -3 standard deviations |
| **At Risk** | Height-for-age z-score between -2 and -1 standard deviations |
| **WHO Z-Score** | Standardized measure of child growth relative to WHO reference population |
| **Site Group** | Partner organization managing one or more measurement sites |
| **Measurement** | A single height recording for a child at a specific date |

---

## Appendix B: WHO Growth Standards Reference

**Height-for-Age Classifications**:

| Status | Z-Score Range | Interpretation |
|--------|---------------|----------------|
| Normal | -1 to +2 | Within normal growth range |
| At Risk | -2 to -1 | Below median but not stunted; requires monitoring |
| Stunted | -3 to -2 | Moderately stunted; immediate intervention needed |
| Severely Stunted | < -3 | Severely stunted; urgent intervention required |

**Reference**: WHO Child Growth Standards (2006)  
**Source**: https://www.who.int/tools/child-growth-standards

---

## Appendix C: Sample Queries

**Overview Page - Total Children**:
```sql
SELECT 
    COUNT(DISTINCT beneficiary_id) AS total_children,
    COUNT(measurement_id) AS total_measurements,
    COUNT(DISTINCT site_id) AS active_sites
FROM MEASUREMENTS
WHERE is_duplicate = FALSE
    AND flagged = FALSE;
```

**Location Analysis - Site Performance**:
```sql
SELECT 
    s.site_name,
    s.site_group,
    COUNT(DISTINCT m.beneficiary_id) AS children_count,
    AVG(m.who_z_score) AS avg_z_score,
    100.0 * SUM(CASE WHEN m.status IN ('Stunted', 'Severely Stunted') THEN 1 ELSE 0 END) 
        / COUNT(*) AS stunting_rate
FROM SITES s
JOIN MEASUREMENTS m ON s.site_id = m.site_id
WHERE m.is_duplicate = FALSE
    AND m.flagged = FALSE
    AND s.is_active = TRUE
GROUP BY s.site_name, s.site_group
ORDER BY children_count DESC;
```

**Child Analysis - Growth History**:
```sql
SELECT 
    m.capture_date,
    m.height_cm,
    m.who_z_score,
    m.status,
    DATEDIFF(day, b.date_of_birth, m.capture_date) / 365.25 AS age_years
FROM MEASUREMENTS m
JOIN BENEFICIARIES b ON m.beneficiary_id = b.beneficiary_id
WHERE m.beneficiary_id = :child_id
    AND m.is_duplicate = FALSE
    AND m.flagged = FALSE
ORDER BY m.capture_date;
```

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2024-10-22 | BI Product Team | Initial PRD |

**Approval**:
- [ ] Product Manager
- [ ] Technical Lead
- [ ] Program Manager
- [ ] Stakeholder Representative

**Next Review Date**: 2024-11-22

---

**END OF DOCUMENT**
