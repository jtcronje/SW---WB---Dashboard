# Epic 3: Child Analysis Page Implementation

## Epic Description
Build the Child Analysis page that enables detailed tracking of individual child growth trajectories. This page allows site coordinators and program staff to monitor individual children's progress and identify those requiring additional support.

## Epic Goals
- Enable child selection through location and search filters
- Display comprehensive child profile information
- Show individual growth trajectories and progress metrics
- Provide detailed measurement history
- Support AI-powered progress summaries

---

## Story 3.1: Child Page - Selection & Profile

### User Story
As a site coordinator, I want to search for and select a specific child so that I can view their detailed profile and growth information.

### Acceptance Criteria
- [ ] Create location dropdown that filters available children
- [ ] Create child search input with debouncing (search across names and ID)
- [ ] Create child dropdown populated by search results
  - Query: `SELECT BENEFICIARY_ID, FIRST_NAMES, LAST_NAME WHERE SITE = :selected_site`
  - Display format: "FirstName LastName (ID: 12345)"
- [ ] Implement child profile hero card showing:
  - Child name, ID, age (calculated from measurements)
  - Household name, site name
  - Latest z-score and status badge
  - Total number of measurements
- [ ] Add session state for selected child
- [ ] Implement search debouncing to avoid excessive queries

### Technical Implementation Notes
- Use Streamlit text_input for search with on_change callback
- Implement debouncing using session state and time delays
- Calculate child age from first measurement date
- Create status badge component with color coding
- Handle cases where child has no measurements

### SQL Query Examples
```sql
-- Get children for selected site with search
SELECT 
    BENEFICIARY_ID,
    FIRST_NAMES,
    LAST_NAME,
    COUNT(*) as measurement_count
FROM NUTRITION_DATA 
WHERE SITE = :selected_site
    AND FLAGGED = 0 AND DUPLICATE = 'False'
    AND (
        LOWER(FIRST_NAMES) LIKE LOWER('%' || :search_term || '%')
        OR LOWER(LAST_NAME) LIKE LOWER('%' || :search_term || '%')
        OR CAST(BENEFICIARY_ID AS VARCHAR) LIKE '%' || :search_term || '%'
    )
GROUP BY BENEFICIARY_ID, FIRST_NAMES, LAST_NAME
ORDER BY FIRST_NAMES, LAST_NAME;

-- Child profile information
SELECT 
    BENEFICIARY_ID,
    FIRST_NAMES,
    LAST_NAME,
    HOUSEHOLD,
    SITE,
    COUNT(*) as total_measurements,
    MIN(CAPTURE_DATE) as first_measurement_date,
    MAX(CAPTURE_DATE) as last_measurement_date,
    ROUND(DATEDIFF(day, MIN(CAPTURE_DATE), MAX(CAPTURE_DATE)) / 365.25, 1) as age_years,
    FIRST_VALUE(WHO_INDEX) OVER (ORDER BY CAPTURE_DATE DESC) as latest_z_score,
    FIRST_VALUE(WHO_INDEX) OVER (ORDER BY CAPTURE_DATE DESC) as latest_status
FROM NUTRITION_DATA 
WHERE BENEFICIARY_ID = :selected_beneficiary_id
    AND FLAGGED = 0 AND DUPLICATE = 'False'
GROUP BY BENEFICIARY_ID, FIRST_NAMES, LAST_NAME, HOUSEHOLD, SITE;
```

### Component Specifications
- `location_selector()` - Dropdown for site selection
- `child_search_input()` - Search input with debouncing
- `child_selector(children_data)` - Dropdown for child selection
- `child_profile_card(child_data)` - Hero card with child information
- `status_badge(z_score)` - Status badge with color coding

---

## Story 3.2: Child Page - Progress Metrics & Charts

### User Story
As a site coordinator, I want to see key progress metrics and growth charts for the selected child so that I can track their development and identify any concerns.

### Acceptance Criteria
- [ ] Create 4 progress metric cards:
  - **Height Gain**: MAX - MIN of ANSWER (in cm)
  - **Z-Score Improvement**: Last - First WHO_INDEX
  - **Average Z-Score**: Average WHO_INDEX across all measurements
  - **Monitoring Period**: Months between first and last measurement
- [ ] Implement alert banners based on status changes:
  - Success: Child moved from stunted to normal
  - Warning: Child improved but still at risk
  - Info: Child requires continued monitoring
- [ ] **Chart 1**: Height Growth Trajectory (Line Chart)
  - Query all measurements for selected child ordered by CAPTURE_DATE
  - Plot ANSWER (height) over time with markers
  - Add trend line and confidence intervals
- [ ] **Chart 2**: Z-Score Progression (Area Chart with Reference Lines)
  - Plot WHO_INDEX over time
  - Add reference lines at -3, -2, and 0 (WHO thresholds)
  - Use area chart with gradient fill
- [ ] Add AI interpretation buttons for both charts

### Technical Implementation Notes
- Calculate progress metrics using window functions
- Implement alert logic based on status changes
- Use Plotly for interactive charts with proper styling
- Add reference lines for WHO standards
- Implement trend analysis for growth patterns

### SQL Query Examples
```sql
-- Progress metrics
SELECT 
    MAX(ANSWER) - MIN(ANSWER) as height_gain_cm,
    FIRST_VALUE(WHO_INDEX) OVER (ORDER BY CAPTURE_DATE DESC) - 
    FIRST_VALUE(WHO_INDEX) OVER (ORDER BY CAPTURE_DATE) as z_score_improvement,
    ROUND(AVG(WHO_INDEX), 2) as avg_z_score,
    ROUND(DATEDIFF(month, MIN(CAPTURE_DATE), MAX(CAPTURE_DATE)), 1) as monitoring_months
FROM NUTRITION_DATA 
WHERE BENEFICIARY_ID = :selected_beneficiary_id
    AND FLAGGED = 0 AND DUPLICATE = 'False';

-- Height growth trajectory
SELECT 
    CAPTURE_DATE,
    ANSWER as height_cm,
    WHO_INDEX,
    ROUND(DATEDIFF(day, 
        (SELECT MIN(CAPTURE_DATE) FROM NUTRITION_DATA WHERE BENEFICIARY_ID = :selected_beneficiary_id), 
        CAPTURE_DATE) / 365.25, 1) as age_years
FROM NUTRITION_DATA 
WHERE BENEFICIARY_ID = :selected_beneficiary_id
    AND FLAGGED = 0 AND DUPLICATE = 'False'
ORDER BY CAPTURE_DATE;

-- Status change detection
WITH first_last_status AS (
    SELECT 
        FIRST_VALUE(WHO_INDEX) OVER (ORDER BY CAPTURE_DATE) as first_z_score,
        FIRST_VALUE(WHO_INDEX) OVER (ORDER BY CAPTURE_DATE DESC) as last_z_score,
        CASE 
            WHEN FIRST_VALUE(WHO_INDEX) OVER (ORDER BY CAPTURE_DATE) >= -1 THEN 'Normal'
            WHEN FIRST_VALUE(WHO_INDEX) OVER (ORDER BY CAPTURE_DATE) BETWEEN -2 AND -1 THEN 'At Risk'
            WHEN FIRST_VALUE(WHO_INDEX) OVER (ORDER BY CAPTURE_DATE) BETWEEN -3 AND -2 THEN 'Stunted'
            ELSE 'Severely Stunted'
        END as first_status,
        CASE 
            WHEN FIRST_VALUE(WHO_INDEX) OVER (ORDER BY CAPTURE_DATE DESC) >= -1 THEN 'Normal'
            WHEN FIRST_VALUE(WHO_INDEX) OVER (ORDER BY CAPTURE_DATE DESC) BETWEEN -2 AND -1 THEN 'At Risk'
            WHEN FIRST_VALUE(WHO_INDEX) OVER (ORDER BY CAPTURE_DATE DESC) BETWEEN -3 AND -2 THEN 'Stunted'
            ELSE 'Severely Stunted'
        END as last_status
    FROM NUTRITION_DATA 
    WHERE BENEFICIARY_ID = :selected_beneficiary_id
        AND FLAGGED = 0 AND DUPLICATE = 'False'
    LIMIT 1
)
SELECT first_status, last_status,
    CASE 
        WHEN first_status != 'Normal' AND last_status = 'Normal' THEN 'SUCCESS'
        WHEN first_status = 'Stunted' AND last_status = 'At Risk' THEN 'WARNING'
        WHEN last_status IN ('Stunted', 'Severely Stunted') THEN 'INFO'
        ELSE 'NORMAL'
    END as alert_type
FROM first_last_status;
```

### Component Specifications
- `progress_metric_card(title, value, subtitle)` - Progress metric display
- `alert_banner(alert_type, title, message)` - Alert banner component
- `create_growth_chart(data)` - Line chart for height trajectory
- `create_z_score_chart(data)` - Area chart with reference lines
- `add_who_reference_lines(fig)` - Add WHO standard reference lines

---

## Story 3.3: Child Page - Measurement History & AI Summary

### User Story
As a site coordinator, I want to see a detailed history of all measurements for the selected child and get an AI-generated progress summary so that I can understand the child's development pattern and get insights for care planning.

### Acceptance Criteria
- [ ] Create measurement history table with columns:
  - Date, Age (calculated), Height (ANSWER), Z-Score (WHO_INDEX), Status, Change from previous
  - Use window functions to calculate changes between measurements
  - Add color coding for positive/negative changes
- [ ] Add CSV export button for measurement history
- [ ] Create "Generate AI Progress Summary" button (placeholder for Epic 4)
- [ ] Style table with alternating rows and status badges
- [ ] Implement sorting and filtering for the table
- [ ] Add pagination for large measurement histories

### Technical Implementation Notes
- Use Streamlit dataframe with custom styling
- Implement window functions for change calculations
- Add color coding for status and changes
- Create export functionality using pandas
- Implement table pagination for performance

### SQL Query Examples
```sql
-- Measurement history with changes
WITH measurements_with_change AS (
    SELECT 
        CAPTURE_DATE,
        ANSWER as height_cm,
        WHO_INDEX,
        ROUND(DATEDIFF(day, 
            (SELECT MIN(CAPTURE_DATE) FROM NUTRITION_DATA WHERE BENEFICIARY_ID = :selected_beneficiary_id), 
            CAPTURE_DATE) / 365.25, 1) as age_years,
        LAG(ANSWER) OVER (ORDER BY CAPTURE_DATE) as prev_height,
        LAG(WHO_INDEX) OVER (ORDER BY CAPTURE_DATE) as prev_z_score,
        ROW_NUMBER() OVER (ORDER BY CAPTURE_DATE) as row_num
    FROM NUTRITION_DATA 
    WHERE BENEFICIARY_ID = :selected_beneficiary_id
        AND FLAGGED = 0 AND DUPLICATE = 'False'
)
SELECT 
    TO_CHAR(CAPTURE_DATE, 'YYYY-MM-DD') as date,
    age_years,
    height_cm,
    ROUND(WHO_INDEX, 2) as z_score,
    CASE 
        WHEN WHO_INDEX >= -1 THEN 'Normal'
        WHEN WHO_INDEX BETWEEN -2 AND -1 THEN 'At Risk'
        WHEN WHO_INDEX BETWEEN -3 AND -2 THEN 'Stunted'
        WHEN WHO_INDEX < -3 THEN 'Severely Stunted'
    END as status,
    CASE 
        WHEN row_num = 1 THEN 'First measurement'
        ELSE CONCAT(
            '+', 
            ROUND(height_cm - prev_height, 1), 
            ' cm | ',
            CASE WHEN WHO_INDEX >= prev_z_score THEN '+' ELSE '' END,
            ROUND(WHO_INDEX - prev_z_score, 2),
            ' z'
        )
    END as change
FROM measurements_with_change
ORDER BY CAPTURE_DATE;
```

### Component Specifications
- `measurement_history_table(data)` - Styled dataframe with custom formatting
- `export_csv_button(data, filename)` - CSV export functionality
- `ai_summary_button(child_data)` - AI progress summary button (placeholder)
- `status_badge(status)` - Color-coded status badge
- `change_indicator(change_value)` - Visual indicator for changes

---

## Epic Success Criteria
- [ ] Location and child dropdowns work correctly
- [ ] Search functionality filters children properly
- [ ] Child profile displays accurate information
- [ ] All 4 progress metric cards show correct values
- [ ] Alert banners display based on status changes
- [ ] Growth charts render correctly with proper data
- [ ] Z-score chart shows WHO reference lines
- [ ] Measurement history table is complete and sortable
- [ ] CSV export functionality works
- [ ] AI summary button is present (functionality in Epic 4)
- [ ] Page loads within 2 seconds after child selection

## Dependencies
- Epic 0 (Project Setup) must be completed
- Epic 1 (Overview Page) for chart styling consistency
- Epic 2 (Location Page) for site selection functionality
- Snowflake database with NUTRITION_DATA table

## Risks & Mitigations
- **Risk**: Children with many measurements causing slow queries
  - **Mitigation**: Implement pagination and query optimization
- **Risk**: Search functionality causing performance issues
  - **Mitigation**: Implement debouncing and limit search results
- **Risk**: Complex window function calculations
  - **Mitigation**: Test queries with large datasets and optimize
- **Risk**: Age calculation accuracy
  - **Mitigation**: Use proper date arithmetic and handle edge cases
