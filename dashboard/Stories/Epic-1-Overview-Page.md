# Epic 1: Overview Page Implementation

## Epic Description
Build the comprehensive Overview page that provides program-wide metrics and trends for the Child Nutrition Dashboard. This page serves as the main landing page and gives stakeholders a high-level view of program impact.

## Epic Goals
- Display key program metrics in visually appealing cards
- Show stunting progress through interactive charts
- Provide temporal trends and geographic distribution
- Enable AI-powered insights for all visualizations
- Support data export and refresh functionality

---

## Story 1.1: Overview Page - Key Metrics Cards

### User Story
As a program manager, I want to see key program metrics at a glance so that I can quickly understand the overall impact and scope of the nutrition program.

### Acceptance Criteria
- [ ] Implement 4 metric cards at the top of the page:
  - **Total Children Measured**: Count of unique BENEFICIARY_ID
  - **Active Sites**: Count of distinct SITE values
  - **Stunting Reduction**: Percentage improvement from first to last measurements
  - **Avg WHO Z-Score**: Average WHO_INDEX across all measurements
- [ ] Create reusable `MetricCard` component in `utils/components.py`
- [ ] Style cards with icons, colors, and trend indicators
- [ ] Add data refresh functionality with loading states
- [ ] Display last updated timestamp

### Technical Implementation Notes
- Use Streamlit columns for card layout (4 columns on desktop, 2x2 on mobile)
- Implement caching for expensive calculations
- Add trend indicators (up/down arrows) for metrics that can be compared over time
- Use color coding: Blue for total counts, Green for improvements, Orange for averages

### SQL Query Examples
```sql
-- Total Children Measured
SELECT COUNT(DISTINCT BENEFICIARY_ID) as total_children
FROM NUTRITION_DATA 
WHERE FLAGGED = 0 AND DUPLICATE = 'False';

-- Active Sites
SELECT COUNT(DISTINCT SITE) as active_sites
FROM NUTRITION_DATA 
WHERE FLAGGED = 0 AND DUPLICATE = 'False';

-- Average WHO Z-Score
SELECT ROUND(AVG(WHO_INDEX), 2) as avg_z_score
FROM NUTRITION_DATA 
WHERE FLAGGED = 0 AND DUPLICATE = 'False';

-- Stunting Reduction (first vs last measurement)
WITH first_measurements AS (
    SELECT BENEFICIARY_ID, WHO_INDEX,
           ROW_NUMBER() OVER (PARTITION BY BENEFICIARY_ID ORDER BY CAPTURE_DATE) as rn
    FROM NUTRITION_DATA 
    WHERE FLAGGED = 0 AND DUPLICATE = 'False'
),
last_measurements AS (
    SELECT BENEFICIARY_ID, WHO_INDEX,
           ROW_NUMBER() OVER (PARTITION BY BENEFICIARY_ID ORDER BY CAPTURE_DATE DESC) as rn
    FROM NUTRITION_DATA 
    WHERE FLAGGED = 0 AND DUPLICATE = 'False'
),
stunting_rates AS (
    SELECT 
        AVG(CASE WHEN f.WHO_INDEX < -2 THEN 1.0 ELSE 0.0 END) as first_stunting_rate,
        AVG(CASE WHEN l.WHO_INDEX < -2 THEN 1.0 ELSE 0.0 END) as last_stunting_rate
    FROM first_measurements f
    JOIN last_measurements l ON f.BENEFICIARY_ID = l.BENEFICIARY_ID
    WHERE f.rn = 1 AND l.rn = 1
)
SELECT ROUND((first_stunting_rate - last_stunting_rate) * 100, 1) as stunting_reduction
FROM stunting_rates;
```

### Component Specifications
- `MetricCard(title, value, subtitle, icon, trend, color)` - Reusable metric card
- `refresh_data_button()` - Manual refresh with loading state
- `last_updated_timestamp()` - Display last data refresh time

---

## Story 1.2: Overview Page - Primary Charts (Charts 1-3)

### User Story
As a program manager, I want to see detailed visualizations of stunting progress and temporal trends so that I can understand program effectiveness and identify patterns.

### Acceptance Criteria
- [ ] **Chart 1**: Stunting Category Progress (Grouped Bar Chart)
  - Show first measurement vs last measurement vs target goals
  - 3 categories: At Risk, Stunted, Severely Stunted
  - Use Plotly grouped bar chart with proper styling
  - Add target goal bars for comparison
- [ ] **Chart 2**: Number of Children by Category (Grouped Bar Chart)
  - Similar to Chart 1 but with absolute counts instead of percentages
  - Show actual numbers of children in each category
- [ ] **Chart 3**: Temporal Trends (Dual-axis Area + Line Chart)
  - Query quarterly aggregated data
  - Show measurement volume (area chart) and stunting rate (line chart)
  - Dual Y-axes for different metrics
- [ ] Add AI interpretation button placeholders for each chart
- [ ] Implement chart export functionality (PNG/PDF)

### Technical Implementation Notes
- Use Plotly for all visualizations with consistent styling
- Implement quarterly aggregation for temporal data
- Add proper axis labels and legends
- Use color palette from PRD: Orange for At Risk, Coral for Stunted, Red for Severely Stunted
- Add loading states during data processing

### SQL Query Examples
```sql
-- Chart 1: Stunting Category Progress
WITH first_measurements AS (
    SELECT BENEFICIARY_ID, WHO_INDEX,
           ROW_NUMBER() OVER (PARTITION BY BENEFICIARY_ID ORDER BY CAPTURE_DATE) as rn
    FROM NUTRITION_DATA 
    WHERE FLAGGED = 0 AND DUPLICATE = 'False'
),
last_measurements AS (
    SELECT BENEFICIARY_ID, WHO_INDEX,
           ROW_NUMBER() OVER (PARTITION BY BENEFICIARY_ID ORDER BY CAPTURE_DATE DESC) as rn
    FROM NUTRITION_DATA 
    WHERE FLAGGED = 0 AND DUPLICATE = 'False'
),
category_classification AS (
    SELECT 
        'First Measurement' as period,
        SUM(CASE WHEN WHO_INDEX BETWEEN -2 AND -1 THEN 1 ELSE 0 END) as at_risk,
        SUM(CASE WHEN WHO_INDEX BETWEEN -3 AND -2 THEN 1 ELSE 0 END) as stunted,
        SUM(CASE WHEN WHO_INDEX < -3 THEN 1 ELSE 0 END) as severely_stunted
    FROM first_measurements WHERE rn = 1
    UNION ALL
    SELECT 
        'Last Measurement' as period,
        SUM(CASE WHEN WHO_INDEX BETWEEN -2 AND -1 THEN 1 ELSE 0 END) as at_risk,
        SUM(CASE WHEN WHO_INDEX BETWEEN -3 AND -2 THEN 1 ELSE 0 END) as stunted,
        SUM(CASE WHEN WHO_INDEX < -3 THEN 1 ELSE 0 END) as severely_stunted
    FROM last_measurements WHERE rn = 1
)
SELECT * FROM category_classification;

-- Chart 3: Temporal Trends
SELECT 
    DATE_TRUNC('quarter', CAPTURE_DATE) as quarter,
    COUNT(*) as measurement_count,
    AVG(WHO_INDEX) as avg_z_score,
    SUM(CASE WHEN WHO_INDEX < -2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as stunting_rate
FROM NUTRITION_DATA 
WHERE FLAGGED = 0 AND DUPLICATE = 'False'
    AND CAPTURE_DATE >= DATEADD(year, -5, CURRENT_DATE())
GROUP BY DATE_TRUNC('quarter', CAPTURE_DATE)
ORDER BY quarter;
```

### Component Specifications
- `create_stunting_progress_chart(data)` - Grouped bar chart for stunting categories
- `create_temporal_trends_chart(data)` - Dual-axis area and line chart
- `ai_interpretation_button(chart_id, chart_title)` - AI analysis button
- `export_chart_button(fig, filename)` - Chart export functionality

---

## Story 1.3: Overview Page - Secondary Charts (Charts 4-6)

### User Story
As a program manager, I want to see geographic distribution and program performance across sites so that I can identify top-performing locations and program distribution.

### Acceptance Criteria
- [ ] **Chart 4**: Top Sites by Children Measured (Horizontal Bar Chart)
  - Show top 10 sites by number of children measured
  - Sort by children count in descending order
  - Use horizontal bar chart for better readability
- [ ] **Chart 5**: Program Distribution (Pie Chart)
  - Show distribution by SITE_GROUP with percentages
  - Use consistent color palette
  - Display labels with percentages
- [ ] **Chart 6**: WHO Z-Score Distribution (Line Chart)
  - Create histogram bins of WHO_INDEX values
  - Add reference lines at -3, -2, and 0 (WHO thresholds)
  - Show distribution curve with markers
- [ ] Style all charts consistently with PRD color palette
- [ ] Add export functionality for all charts
- [ ] Implement responsive design for mobile devices

### Technical Implementation Notes
- Use Plotly for consistent styling across all charts
- Implement proper binning for histogram data
- Add reference lines for WHO standards
- Ensure charts are responsive and readable on all devices
- Add tooltips with detailed information

### SQL Query Examples
```sql
-- Chart 4: Top Sites by Children Measured
SELECT 
    SITE,
    COUNT(DISTINCT BENEFICIARY_ID) as children_count,
    ROUND(COUNT(DISTINCT BENEFICIARY_ID) * 100.0 / SUM(COUNT(DISTINCT BENEFICIARY_ID)) OVER (), 1) as percentage
FROM NUTRITION_DATA 
WHERE FLAGGED = 0 AND DUPLICATE = 'False'
GROUP BY SITE
ORDER BY children_count DESC
LIMIT 10;

-- Chart 5: Program Distribution
SELECT 
    SITE_GROUP,
    COUNT(DISTINCT BENEFICIARY_ID) as children_count,
    ROUND(COUNT(DISTINCT BENEFICIARY_ID) * 100.0 / SUM(COUNT(DISTINCT BENEFICIARY_ID)) OVER (), 1) as percentage
FROM NUTRITION_DATA 
WHERE FLAGGED = 0 AND DUPLICATE = 'False'
GROUP BY SITE_GROUP
ORDER BY children_count DESC;

-- Chart 6: WHO Z-Score Distribution
WITH z_score_bins AS (
    SELECT 
        FLOOR(WHO_INDEX * 2) / 2 as z_score_bin,
        COUNT(*) as frequency
    FROM NUTRITION_DATA 
    WHERE FLAGGED = 0 AND DUPLICATE = 'False'
        AND WHO_INDEX BETWEEN -6 AND 6
    GROUP BY FLOOR(WHO_INDEX * 2) / 2
)
SELECT z_score_bin, frequency
FROM z_score_bins
ORDER BY z_score_bin;
```

### Component Specifications
- `create_sites_chart(data)` - Horizontal bar chart for top sites
- `create_program_distribution_chart(data)` - Pie chart for site groups
- `create_z_score_distribution_chart(data)` - Line chart with reference lines
- `add_reference_lines(fig)` - Add WHO standard reference lines
- `responsive_chart_container(fig)` - Responsive chart wrapper

---

## Epic Success Criteria
- [ ] All 4 metric cards display accurate data with proper styling
- [ ] All 6 charts render correctly with proper data
- [ ] Charts are interactive and responsive
- [ ] AI interpretation buttons are present (functionality in Epic 4)
- [ ] Export functionality works for all charts
- [ ] Page loads within 3 seconds
- [ ] Mobile layout is functional

## Dependencies
- Epic 0 (Project Setup) must be completed
- Snowflake database with NUTRITION_DATA table
- Plotly and Streamlit dependencies installed

## Risks & Mitigations
- **Risk**: Large dataset causing slow queries
  - **Mitigation**: Implement query optimization and caching
- **Risk**: Complex aggregations causing timeouts
  - **Mitigation**: Use materialized views or pre-aggregated data
- **Risk**: Mobile responsiveness issues
  - **Mitigation**: Test on multiple devices and implement responsive design patterns
