# Sales Intelligence System

# Project Overview
An end-to-end business analytics project that analyzes retail sales data, 
builds a 90-day sales forecast, and generates executive summaries 
using Claude API. Managed using Agile methodology in Jira.

# Tech Stack
| Tool | Purpose |
|------|---------|
| Python (pandas, numpy) | Data cleaning & analysis |
| Plotly | Interactive dashboards |
| Claude API (Anthropic) | Executive summaries |
| Jira | Agile project management|
| GitHub | Version control |

# Key Findings
- Total Revenue analysed: $2.3M across 4 years
- Identified Technology as highest revenue category (36% of sales)
- Forecast shows 12% projected growth in Q1 next period
- Central region has lowest profit margin and it is flagged for review

# AI Aspect in the project
Used Claude API to automatically generate natural language executive summaries from key metrics


# How to Run
```bash
git clone https://github.com/shrajna15/Sales-Intelligence-Project
cd sales-intelligence-project
pip install -r requirements.txt
# Add your ANTHROPIC_API_KEY to a .env file
jupyter notebook notebooks/analysis.ipynb
```
