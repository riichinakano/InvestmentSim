# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Investment Portfolio Simulator (資産運用シミュレーター)** - A Streamlit-based life plan integrated investment simulator with NISA support, lifecycle event planning, and multi-scenario comparison capabilities.

**Current Version:** 2.0 (Phase 1 & Phase 2 Complete)

## Quick Start

### Running the Application

```bash
# Activate virtual environment (if using)
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

# Run the application
streamlit run app.py
```

The app will be available at http://localhost:8501

### Dependencies

```bash
pip install streamlit plotly pandas openpyxl
```

Required packages:
- streamlit >= 1.28.0
- plotly >= 5.17.0 (interactive graphs)
- pandas >= 2.0.0
- openpyxl >= 3.1.0 (Excel export)
- SQLite3 (Python standard library - no install needed)

## Architecture

### Core Files

- **app.py** - Main Streamlit application with all UI logic
- **database.py** - SQLite database management for simulation persistence
- **simulations.db** - SQLite database (auto-created, **do NOT commit to git**)

### Key Design Patterns

**Multi-language Support:**
- All UI strings are in `TRANSLATIONS` dictionary at the top of app.py
- Add new strings to both "English" and "日本語" sections
- Access via `t["key_name"]` where `t = TRANSLATIONS[st.session_state.language]`

**Session State Management:**
- `st.session_state.language` - Current UI language
- `st.session_state.life_events` - List of registered life events
- `st.session_state.current_simulation_id` - Currently loaded simulation ID
- `st.session_state.current_simulation_name` - Currently loaded simulation name
- Loaded parameters stored as `st.session_state.loaded_{param_name}`

**Decimal Precision:**
- All financial calculations use `Decimal` type (not float) for precision
- Convert inputs: `Decimal(str(value))`
- Round results: `.quantize(Decimal('1'), rounding=ROUND_HALF_UP)`

### Three-Tab Structure

1. **Tab 1 (資産運用シミュレーション):** Basic investment simulation with NISA tracking
2. **Tab 2 (ライフプラン表):** Family composition + life events + integrated simulation
3. **Tab 3 (シナリオ比較):** Compare up to 3 saved scenarios side-by-side

### Simulation Logic Flow

**Basic Investment (`simulate_investment_with_nisa`):**
1. NISA contribution (track 18M JPY limit)
2. Apply expected return to risk assets
3. Year-end rebalancing to target risk ratio
4. Return DataFrame + NISA limit year

**Integrated Life Plan (`simulate_integrated_lifeplan`):**
1. NISA contribution
2. Apply expected return
3. Process life event withdrawal (safe assets → risk assets if needed)
4. Rebalance to target ratio
5. Record final asset state only (simplified from v1.3+)

### Database Schema

**simulations table:**
- Investment parameters (initial_amount, nisa_contribution, risk_return, etc.)
- Family composition (husband_age, wife_age, child1-3_age)
- Metadata (name, language, timestamps)

**life_events table:**
- Foreign key to simulations.id (CASCADE delete)
- year, event_name, amount

## Important Constraints

### Functional Limits
- Family: Max 5 members (couple + 3 children)
- Events: 1 event per year
- Simulation: 1-50 years
- NISA limit: 18,000,000 JPY

### Calculation Assumptions
- Returns: Fixed annual rate (no variance)
- Inflation: Not considered
- Taxes: Not considered (NISA assumption)

## Common Modifications

### Adding New Translation Strings

Add to both language sections in `TRANSLATIONS` dictionary:

```python
"English": {
    "new_key": "English text",
    # ...
},
"日本語": {
    "new_key": "日本語テキスト",
    # ...
}
```

### Adding Database Fields

1. Update schema in `database.py` `init_db()` method
2. Update `save_simulation()` and `load_simulation()` methods
3. Update parameter collection in app.py save handlers
4. Increment database version if needed

### Modifying Simulation Logic

**CRITICAL:** When changing calculation logic:
- Update both `simulate_investment_with_nisa` AND `simulate_integrated_lifeplan`
- Maintain `Decimal` precision throughout
- Update `requirements_design_document.md` section 5 (Business Logic)
- Test with edge cases (0 values, NISA limit crossing, asset depletion)

## Export Functionality

**CSV Export:**
- UTF-8 with BOM (Excel compatibility for Japanese characters)
- Filename pattern: `{base_name}_YYYYMMDD_HHMMSS.csv`

**Excel Export:**
- Uses openpyxl engine
- Auto-adjusts column widths
- Applies number formatting

## Phase 2 Features

**Database Operations:**
- `db.save_simulation()` - New save or overwrite
- `db.load_simulation()` - Restore all parameters + events
- `db.list_simulations()` - Get all saved simulations
- `db.delete_simulation()` - Remove simulation and events (CASCADE)

**Scenario Comparison:**
- Runs full simulation for each selected scenario
- Handles both basic and integrated simulations
- Compares total asset progression over time

## Reference Documentation

- **requirements_design_document.md** - Complete specification (v2.0)
  - Phase 1: Core features ✅
  - Phase 2: Database + comparison ✅
  - Phase 3: Future enhancements
- **README.md** - User-facing documentation

## Data Files to Exclude from Git

```
simulations.db
*.db-journal
*.db-wal
.venv/
__pycache__/
*.pyc
```
