# Epic 4: AI Integration & Final Styling

## Epic Description
Implement OpenAI GPT-4o integration for AI-powered chart interpretations and complete the final styling and polish for the Child Nutrition Dashboard. This epic adds intelligent insights to all visualizations and ensures a professional, responsive user experience.

## Epic Goals
- Integrate OpenAI GPT-4o API for chart interpretations
- Create reusable AI interpretation components
- Implement comprehensive styling and responsive design
- Add final polish and performance optimizations
- Ensure accessibility and user experience standards

---

## Story 4.1: OpenAI Integration Setup

### User Story
As a developer, I want to set up OpenAI GPT-4o integration so that the dashboard can provide intelligent insights for all charts and visualizations.

### Acceptance Criteria
- [ ] Create `utils/ai_service.py` module with OpenAI GPT-4o client
- [ ] Implement `generate_interpretation()` function with:
  - System prompt for nutrition data analysis
  - Context-aware prompts for each chart type
  - Error handling and retry logic
  - Rate limiting checks
- [ ] Add OpenAI API key to secrets configuration
- [ ] Create chart-specific prompt templates for each visualization
- [ ] Implement response caching to reduce API costs
- [ ] Add comprehensive error handling for API failures

### Technical Implementation Notes
- Use OpenAI Python client library
- Implement proper API key management through Streamlit secrets
- Create system prompts tailored for child nutrition data analysis
- Add retry logic with exponential backoff
- Implement session state caching for interpretations
- Handle rate limits and API errors gracefully

### SQL Query Examples
N/A - This story focuses on API integration

### Component Specifications
- `get_openai_client()` - Initialize OpenAI client
- `generate_interpretation(prompt, chart_type)` - Generate AI interpretation
- `create_chart_prompt(chart_data, chart_type)` - Create chart-specific prompts
- `cache_interpretation(key, interpretation)` - Cache interpretation results
- `handle_api_errors(error)` - Error handling for API failures

---

## Story 4.2: AI Interpretation Components

### User Story
As a user, I want to click AI interpretation buttons on charts to get intelligent insights so that I can better understand the data and make informed decisions.

### Acceptance Criteria
- [ ] Create reusable `AIInterpretationButton` component
- [ ] Implement interpretation caching in session state
- [ ] Add loading spinners during API calls
- [ ] Style interpretation display boxes with gradient borders
- [ ] Connect AI buttons to all charts on Overview, Location, and Child pages:
  - Overview: 6 charts (stunting progress, temporal trends, etc.)
  - Location: 6 charts (site-specific and comparison charts)
  - Child: 2 charts (growth trajectory, z-score progression)
- [ ] Create chart-specific prompt templates for each visualization
- [ ] Add interpretation export functionality

### Technical Implementation Notes
- Create consistent AI button styling across all pages
- Implement loading states with Streamlit spinners
- Use session state to cache interpretations per chart
- Create chart-specific prompts with data context
- Add interpretation display with proper formatting
- Implement error handling for failed interpretations

### SQL Query Examples
N/A - This story focuses on UI components

### Component Specifications
- `ai_interpretation_button(chart_id, chart_title, chart_data)` - Reusable AI button
- `display_interpretation(interpretation)` - Styled interpretation display
- `loading_spinner()` - Loading state component
- `interpretation_cache()` - Session state caching
- `chart_prompt_templates()` - Chart-specific prompt templates

---

## Story 4.3: Final Styling & Polish

### User Story
As a user, I want the dashboard to have professional styling, responsive design, and smooth interactions so that I can use it effectively on any device.

### Acceptance Criteria
- [ ] Create `utils/styling.py` with custom CSS
- [ ] Implement color palette from PRD:
  - Status colors: Normal (Green), At Risk (Orange), Stunted (Coral), Severely Stunted (Red)
  - Primary colors: Blue (#4299E1), Purple (#9F7AEA)
  - Gradients for hero cards and buttons
- [ ] Add custom fonts and typography
- [ ] Create status badge component with color coding
- [ ] Implement responsive design adjustments:
  - Desktop (>1024px): Full layouts
  - Tablet (768-1024px): Adapted layouts
  - Mobile (<768px): Simplified layouts
- [ ] Add loading states and skeleton screens
- [ ] Implement accessibility features (WCAG 2.1 AA)
- [ ] Final testing and bug fixes across all pages

### Technical Implementation Notes
- Use Streamlit's custom CSS capabilities
- Implement responsive breakpoints
- Add proper color contrast ratios
- Create reusable component library
- Implement keyboard navigation
- Add screen reader support
- Test across multiple devices and browsers

### SQL Query Examples
N/A - This story focuses on styling and UX

### Component Specifications
- `apply_custom_css()` - Apply global custom styles
- `status_badge(status, size)` - Color-coded status badges
- `metric_card(title, value, icon, color)` - Styled metric cards
- `hero_card(title, subtitle, gradient)` - Gradient hero cards
- `responsive_container()` - Responsive layout wrapper
- `loading_skeleton()` - Loading state placeholders

---

## Epic Success Criteria
- [ ] OpenAI API integration works reliably
- [ ] AI interpretation buttons are present on all charts
- [ ] Interpretations are relevant and helpful
- [ ] Caching reduces API costs and improves performance
- [ ] Dashboard has professional, consistent styling
- [ ] Responsive design works on all device sizes
- [ ] Accessibility standards are met
- [ ] Loading states provide good user feedback
- [ ] All pages load within performance targets
- [ ] No critical bugs or errors

## Dependencies
- Epic 0 (Project Setup) must be completed
- Epic 1 (Overview Page) for chart integration
- Epic 2 (Location Page) for chart integration
- Epic 3 (Child Page) for chart integration
- OpenAI API key and account setup

## Risks & Mitigations
- **Risk**: OpenAI API rate limits or costs
  - **Mitigation**: Implement caching and rate limiting
- **Risk**: API responses not relevant to nutrition data
  - **Mitigation**: Create detailed, context-specific prompts
- **Risk**: Responsive design issues on mobile
  - **Mitigation**: Test on multiple devices and implement mobile-first design
- **Risk**: Performance issues with custom styling
  - **Mitigation**: Optimize CSS and use efficient selectors
- **Risk**: Accessibility compliance issues
  - **Mitigation**: Follow WCAG guidelines and test with screen readers

## Implementation Notes
- OpenAI API key should be stored in Streamlit secrets
- Implement proper error handling for API failures
- Use consistent prompt templates for similar chart types
- Cache interpretations to reduce API calls and costs
- Test AI responses for accuracy and relevance
- Ensure styling works across all major browsers
- Implement proper loading states for better UX
