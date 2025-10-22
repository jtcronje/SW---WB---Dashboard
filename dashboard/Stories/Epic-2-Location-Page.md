# Epic 2: Location Analysis Page Implementation

## Epic Description
Build the Location Analysis page that provides deep-dive insights into site-specific nutrition outcomes. This page enables program managers and site coordinators to analyze individual site performance and compare outcomes across locations.

## Epic Goals
- Enable site selection and filtering
- Display site-specific performance metrics and rankings
- Show temporal trends for selected locations
- Provide cross-site comparison capabilities
- Support AI-powered insights for location-specific data

---

## Story 2.1: Location Page - Selection & Summary

### User Story
As a site coordinator, I want to select my specific site and see a comprehensive summary of its performance so that I can understand how my site is performing compared to others.

### Acceptance Criteria
- [ ] Create location dropdown selector populated from `SELECT DISTINCT SITE`
- [ ] Implement location summary hero card with gradient background showing:
  - Site name and site group
  - Total children, households, average z-score, stunting rate
- [ ] Create 4 performance ranking cards comparing selected site to all sites:
  - Children measured rank (out of total sites)
  - Average z-score rank (higher is better)
  - Stunting rate rank (lower is better)
  - Severe stunting rank (lower is better)
- [ ] Implement session state management for selected location
- [ ] Add loading states during site selection

### Technical Implementation Notes
- Use Streamlit selectbox for location dropdown
- Implement session state to persist selected location
- Create gradient hero card with site information
- Use ranking calculations with proper sorting
- Add visual indicators for ranking (1st, 2nd, 3rd place badges)

### SQL Query Examples
```sql
-- Get all available sites
SELECT DISTINCT SITE, COUNT(DISTINCT BENEFICIARY_ID) as child_count
FROM NUTRITION_DATA 
WHERE FLAGGED = 0 AND DUPLICATE = 'False'
GROUP BY SITE
ORDER BY SITE;

-- Site summary information
SELECT 
    SITE,
    SITE_GROUP,
    COUNT(DISTINCT BENEFICIARY_ID) as total_children,
    COUNT(DISTINCT HOUSEHOLD_ID) as total_households,
    ROUND(AVG(WHO_INDEX), 2) as avg_z_score,
    ROUND(SUM(CASE WHEN WHO_INDEX < -2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as stunting_rate
FROM NUTRITION_DATA 
WHERE SITE = :selected_site
    AND FLAGGED = 0 AND DUPLICATE = 'False'
GROUP BY SITE, SITE_GROUP;

-- Site ranking for children measured
WITH site_rankings AS (
    SELECT 
        SITE,
        COUNT(DISTINCT BENEFICIARY_ID) as children_count,
        RANK() OVER (ORDER BY COUNT(DISTINCT BENEFICIARY_ID) DESC) as rank,
        COUNT(*) OVER () as total_sites
    FROM NUTRITION_DATA 
    WHERE FLAGGED = 0 AND DUPLICATE = 'False'
    GROUP BY SITE
)
SELECT children_count, rank, total_sites
FROM site_rankings 
WHERE SITE = :selected_site;

-- Site ranking for average z-score
WITH site_rankings AS (
    SELECT 
        SITE,
        AVG(WHO_INDEX) as avg_z_score,
        RANK() OVER (ORDER BY AVG(WHO_INDEX) DESC) as rank,
        COUNT(*) OVER () as total_sites
    FROM NUTRITION_DATA 
    WHERE FLAGGED = 0 AND DUPLICATE = 'False'
    GROUP BY SITE
)
SELECT ROUND(avg_z_score, 2) as avg_z_score, rank, total_sites
FROM site_rankings 
WHERE SITE = :selected_site;
```

### Component Specifications
- `location_selector()` - Dropdown for site selection
- `site_summary_card(site_data)` - Hero card with site information
- `ranking_card(title, value, rank, total)` - Performance ranking card
- `session_state_manager()` - Handle selected location state

---

## Story 2.2: Location Page - Site-Specific Charts (Charts 1-3)

### User Story
As a site coordinator, I want to see detailed charts showing my site's nutrition outcomes over time and current status distribution so that I can track progress and identify areas for improvement.

### Acceptance Criteria
- [ ] **Chart 1**: Nutrition Outcomes Over Time (Multi-line Chart)
  - Query quarterly data filtered by selected site
  - Show 3 lines: stunting rate, severe stunting rate, average z-score
  - Use dual Y-axes for percentages and z-scores
  - Add markers and tooltips for data points
- [ ] **Chart 2**: Number of Children by Category - Location
  - First/last/target comparison for selected site only
  - Use grouped bar chart similar to Overview page
  - Show absolute counts for the specific site
- [ ] **Chart 3**: Current Status Distribution (Bar Chart)
  - Latest measurement status for each child at selected site
  - Color-coded bars by status category
  - Show both counts and percentages
- [ ] Add AI interpretation buttons for each chart
- [ ] Implement chart filtering and interactivity

### Technical Implementation Notes
- Filter all queries by selected site
- Use consistent chart styling with Overview page
- Implement quarterly aggregation for temporal data
- Add proper axis labels and legends
- Use color coding consistent with status categories

### SQL Query Examples
```sql
-- Chart 1: Nutrition Outcomes Over Time
SELECT 
    DATE_TRUNC('quarter', CAPTURE_DATE) as quarter,
    ROUND(SUM(CASE WHEN WHO_INDEX BETWEEN -3 AND -2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as stunting_rate,
    ROUND(SUM(CASE WHEN WHO_INDEX < -3 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as severe_stunting_rate,
    ROUND(AVG(WHO_INDEX), 2) as avg_z_score
FROM NUTRITION_DATA 
WHERE SITE = :selected_site
    AND FLAGGED = 0 AND DUPLICATE = 'False'
    AND CAPTURE_DATE >= DATEADD(year, -5, CURRENT_DATE())
GROUP BY DATE_TRUNC('quarter', CAPTURE_DATE)
ORDER BY quarter;

-- Chart 2: Children by Category for Selected Site
WITH first_measurements AS (
    SELECT BENEFICIARY_ID, WHO_INDEX,
           ROW_NUMBER() OVER (PARTITION BY BENEFICIARY_ID ORDER BY CAPTURE_DATE) as rn
    FROM NUTRITION_DATA 
    WHERE SITE = :selected_site AND FLAGGED = 0 AND DUPLICATE = 'False'
),
last_measurements AS (
    SELECT BENEFICIARY_ID, WHO_INDEX,
           ROW_NUMBER() OVER (PARTITION BY BENEFICIARY_ID ORDER BY CAPTURE_DATE DESC) as rn
    FROM NUTRITION_DATA 
    WHERE SITE = :selected_site AND FLAGGED = 0 AND DUPLICATE = 'False'
),
site_totals AS (
    SELECT COUNT(DISTINCT BENEFICIARY_ID) as total
    FROM NUTRITION_DATA 
    WHERE SITE = :selected_site AND FLAGGED = 0 AND DUPLICATE = 'False'
)
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
UNION ALL
SELECT 
    'Target' as period,
    CAST(total * 0.025 AS INTEGER) as at_risk,
    CAST(total * 0.025 AS INTEGER) as stunted,
    CAST(total * 0.0015 AS INTEGER) as severely_stunted
FROM site_totals;

-- Chart 3: Current Status Distribution
WITH latest_measurements AS (
    SELECT BENEFICIARY_ID, WHO_INDEX,
           ROW_NUMBER() OVER (PARTITION BY BENEFICIARY_ID ORDER BY CAPTURE_DATE DESC) as rn
    FROM NUTRITION_DATA 
    WHERE SITE = :selected_site AND FLAGGED = 0 AND DUPLICATE = 'False'
)
SELECT 
    CASE 
        WHEN WHO_INDEX >= -1 THEN 'Normal'
        WHEN WHO_INDEX BETWEEN -2 AND -1 THEN 'At Risk'
        WHEN WHO_INDEX BETWEEN -3 AND -2 THEN 'Stunted'
        WHEN WHO_INDEX < -3 THEN 'Severely Stunted'
    END as status,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) as percentage
FROM latest_measurements
WHERE rn = 1
GROUP BY status
ORDER BY 
    CASE status
        WHEN 'Normal' THEN 1
        WHEN 'At Risk' THEN 2
        WHEN 'Stunted' THEN 3
        WHEN 'Severely Stunted' THEN 4
    END;
```

### Component Specifications
- `create_temporal_chart(data)` - Multi-line chart for outcomes over time
- `create_site_category_chart(data)` - Grouped bar chart for site categories
- `create_status_distribution_chart(data)` - Bar chart for current status
- `add_dual_axes(fig)` - Add dual Y-axes for different metrics

---

## Story 2.3: Location Page - Comparison Charts (Charts 4-6)

### User Story
As a program manager, I want to compare the selected site's performance against all other sites so that I can identify best practices and areas needing attention.

### Acceptance Criteria
- [ ] **Chart 4**: Z-Score Comparison Across Locations (Horizontal Bar Chart)
  - Show all sites with selected site highlighted
  - Sort by children count in descending order
  - Use different colors for selected vs other sites
- [ ] **Chart 5**: Stunting Rate Comparison (Horizontal Bar Chart)
  - Compare stunting rates across all sites
  - Highlight selected site with different color
  - Sort by stunting rate (ascending - lower is better)
- [ ] **Chart 6**: Measurement Volume Over Time (Area Chart)
  - Quarterly measurement count for selected site
  - Show measurement activity patterns
  - Use area chart with gradient fill
- [ ] Add filtering and interactivity between charts
- [ ] Implement chart export functionality

### Technical Implementation Notes
- Highlight selected site in comparison charts
- Use consistent sorting and color schemes
- Implement area chart with proper gradient styling
- Add tooltips with detailed site information
- Ensure charts are responsive and readable

### SQL Query Examples
```sql
-- Chart 4: Z-Score Comparison Across Locations
SELECT 
    SITE,
    COUNT(DISTINCT BENEFICIARY_ID) as children_count,
    ROUND(AVG(WHO_INDEX), 2) as avg_z_score,
    CASE WHEN SITE = :selected_site THEN 1 ELSE 0 END as is_current
FROM NUTRITION_DATA 
WHERE FLAGGED = 0 AND DUPLICATE = 'False'
GROUP BY SITE
ORDER BY children_count DESC;

-- Chart 5: Stunting Rate Comparison
SELECT 
    SITE,
    COUNT(DISTINCT BENEFICIARY_ID) as children_count,
    ROUND(SUM(CASE WHEN WHO_INDEX < -2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as stunting_rate,
    CASE WHEN SITE = :selected_site THEN 1 ELSE 0 END as is_current
FROM NUTRITION_DATA 
WHERE FLAGGED = 0 AND DUPLICATE = 'False'
GROUP BY SITE
ORDER BY stunting_rate ASC;

-- Chart 6: Measurement Volume Over Time
SELECT 
    DATE_TRUNC('quarter', CAPTURE_DATE) as quarter,
    COUNT(*) as measurement_count
FROM NUTRITION_DATA 
WHERE SITE = :selected_site
    AND FLAGGED = 0 AND DUPLICATE = 'False'
    AND CAPTURE_DATE >= DATEADD(year, -5, CURRENT_DATE())
GROUP BY DATE_TRUNC('quarter', CAPTURE_DATE)
ORDER BY quarter;
```

### Component Specifications
- `create_z_score_comparison_chart(data, selected_site)` - Horizontal bar chart with highlighting
- `create_stunting_comparison_chart(data, selected_site)` - Stunting rate comparison
- `create_volume_chart(data)` - Area chart for measurement volume
- `highlight_selected_site(fig, selected_site)` - Highlight selected site in charts

---

## Epic Success Criteria
- [ ] Location dropdown populates correctly with all sites
- [ ] Site summary card displays accurate information
- [ ] All 4 ranking cards show correct rankings
- [ ] All 6 charts render correctly with proper data
- [ ] Selected site is highlighted in comparison charts
- [ ] Charts are interactive and responsive
- [ ] AI interpretation buttons are present (functionality in Epic 4)
- [ ] Page loads within 2 seconds after site selection

## Dependencies
- Epic 0 (Project Setup) must be completed
- Epic 1 (Overview Page) for chart styling consistency
- Snowflake database with NUTRITION_DATA table

## Risks & Mitigations
- **Risk**: Large number of sites causing performance issues
  - **Mitigation**: Implement pagination or filtering for site lists
- **Risk**: Complex ranking calculations causing slow queries
  - **Mitigation**: Use window functions and optimize queries
- **Risk**: Site selection state not persisting
  - **Mitigation**: Implement robust session state management
