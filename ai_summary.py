
# Claude AI to write a business summary from data

import anthropic
import pandas as pd
import os
from dotenv import load_dotenv   # Reads our secret .env file

# Load the API key from .env file
load_dotenv()

# PART 1: Load data and calculate key metrics

# Load the cleaned data in analysis.py
df = pd.read_csv('outputs/cleaned_superstore.csv')

# Convert date column back to date format
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Year'] = df['Order Date'].dt.year

# Calculate key business metrics
total_sales     = df['Sales'].sum()
total_profit    = df['Profit'].sum()
profit_margin   = (total_profit / total_sales) * 100
total_orders    = df['Order ID'].nunique()
avg_order_value = total_sales / total_orders

# Category breakdown
category_sales  = df.groupby('Category')['Sales'].sum()
best_category   = category_sales.idxmax()
worst_category  = category_sales.idxmin()

# Regional breakdown
region_profit   = df.groupby('Region')['Profit'].sum()
best_region     = region_profit.idxmax()
worst_region    = region_profit.idxmin()

# Monthly trend
monthly_sales   = df.groupby(df['Order Date'].dt.to_period('M'))['Sales'].sum()
best_month      = str(monthly_sales.idxmax())

# Year on year
yoy = df.groupby('Year')['Sales'].sum()
latest_year     = yoy.index.max()
prev_year       = latest_year - 1
if prev_year in yoy.index:
    growth = ((yoy[latest_year] - yoy[prev_year]) / yoy[prev_year]) * 100
else:
    growth = 0

# Print what we found
print("Key Metrics Calculated:")
print(f"  Total Sales:        ${total_sales:,.0f}")
print(f"  Total Profit:       ${total_profit:,.0f}")
print(f"  Profit Margin:      {profit_margin:.1f}%")
print(f"  Total Orders:       {total_orders:,}")
print(f"  Avg Order Value:    ${avg_order_value:,.0f}")
print(f"  Best Category:      {best_category}")
print(f"  Worst Category:     {worst_category}")
print(f"  Best Region:        {best_region}")
print(f"  Weakest Region:     {worst_region}")
print(f"  Peak Sales Month:   {best_month}")
print(f"  YoY Growth ({latest_year}):  {growth:.1f}%")


# PART 2: Send metrics to Claude AI for a written summary

# Connect to the Claude API using secret key
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Write instructions for Claude by the name "prompt"
prompt = f"""
You are a business analyst presenting quarterly results to a board of directors.

Here are the key metrics from a US retail company's full sales dataset:

- Total Revenue: ${total_sales:,.0f}
- Total Profit: ${total_profit:,.0f}
- Profit Margin: {profit_margin:.1f}%
- Total Orders Processed: {total_orders:,}
- Average Order Value: ${avg_order_value:,.0f}
- Best Performing Category: {best_category}
- Underperforming Category: {worst_category}
- Most Profitable Region: {best_region}
- Lowest Profit Region: {worst_region}
- Peak Sales Month: {best_month}
- Year-on-Year Revenue Growth: {growth:.1f}%

Write a professional executive summary (5–6 sentences) that covers:
1. Overall business performance and revenue health
2. What is working well (highlight strengths)
3. One specific area of concern with supporting data
4. One clear, actionable strategic recommendation

Write in a confident, professional tone suitable for a board presentation.
Use actual numbers from the data. Do not use bullet points — write in flowing paragraphs.
"""

print("\n🤖 Sending data to Claude AI...")
print("⏳ Generating executive summary...\n")

# Make the API call to Claude
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=600,
    messages=[{"role": "user", "content": prompt}]
)

# Extract the text response
ai_summary = message.content[0].text

# Display it
print("=" * 65)
print("         📝 AI-GENERATED EXECUTIVE SUMMARY")
print("=" * 65)
print(ai_summary)
print("=" * 65)

# PART 3: Save the summary to a file

output_text = f""" SUMMARY — AI Generated via Claude API
{'=' * 65}

KEY METRICS
-----------
Total Revenue:     ${total_sales:,.0f}
Total Profit:      ${total_profit:,.0f}
Profit Margin:     {profit_margin:.1f}%
Total Orders:      {total_orders:,}
Best Category:     {best_category}
Best Region:       {best_region}
Weakest Region:    {worst_region}
Peak Month:        {best_month}
YoY Growth:        {growth:.1f}%

 SUMMARY
-----------------
{ai_summary}
"""

with open('outputs/executive_summary.txt', 'w') as f:
    f.write(output_text)

print("\Summary saved to: outputs/executive_summary.txt")