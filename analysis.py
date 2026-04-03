# SALES INTELLIGENCE PROJECT 
# --- Import libraries---
import pandas as pd               # For working with data (like Excel in Python)
import matplotlib.pyplot as plt   # For drawing charts
import seaborn as sns             # For prettier chart styles
import os                         # For file/folder operations

# PART 1: Load the data
# Read the CSV file into a dataframe (think of it as a table)
df = pd.read_csv('data/superstore.csv', encoding='latin-1')

print("✅ Data loaded!")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
print("\nColumn names:")
print(df.columns.tolist())
print("\nFirst 3 rows:")
print(df.head(3))

# PART 2: Clean the data
# Convert date columns from plain text to proper date format
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date']  = pd.to_datetime(df['Ship Date'])

# Extract useful time parts from the order date
df['Year']       = df['Order Date'].dt.year
df['Month']      = df['Order Date'].dt.month
df['Month-Year'] = df['Order Date'].dt.to_period('M')

# Remove duplicate orders (same Order ID appearing twice)
df = df.drop_duplicates(subset='Order ID')

print("\n✅ Data cleaned!")
print(f"Final shape: {df.shape[0]} rows, {df.shape[1]} columns")

# PART 3: Analyse the data
# Key business numbers
total_sales    = df['Sales'].sum()
total_profit   = df['Profit'].sum()
profit_margin  = (total_profit / total_sales) * 100

print(f"\n💰 Total Sales:    ${total_sales:,.2f}")
print(f"📈 Total Profit:   ${total_profit:,.2f}")
print(f"📊 Profit Margin:  {profit_margin:.1f}%")

# Sales by Category (Technology, Furniture, Office Supplies)
category_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
print("\n🛍️ Sales by Category:")
print(category_sales)

# Sales and Profit by Region
region_data = df.groupby('Region')[['Sales', 'Profit']].sum()
print("\n🗺️ Sales & Profit by Region:")
print(region_data)

# Monthly sales over time
monthly_sales = df.groupby('Month-Year')['Sales'].sum().reset_index()
monthly_sales['Month-Year'] = monthly_sales['Month-Year'].astype(str)

# Best and worst performers
best_category  = category_sales.idxmax()
worst_region   = region_data['Profit'].idxmin()
best_month     = monthly_sales.loc[monthly_sales['Sales'].idxmax(), 'Month-Year']

print(f"\n🏆 Best Category:   {best_category}")
print(f"⚠️  Worst Region:    {worst_region}")
print(f"📅 Best Sales Month: {best_month}")

# PART 4: Save charts as images
# Make sure the outputs folder exists
os.makedirs('outputs', exist_ok=True)

# Set a clean visual style for all charts
sns.set_theme(style='whitegrid')

# --- Chart 1: Sales by Category ---
plt.figure(figsize=(8, 5))
sns.barplot(x=category_sales.index,
            y=category_sales.values,
            palette='Blues_d')
plt.title('Total Sales by Category', fontsize=14, fontweight='bold')
plt.ylabel('Sales ($)')
plt.xlabel('Category')
plt.tight_layout()
plt.savefig('outputs/chart1_category_sales.png', dpi=150)
plt.show()
print("✅ Chart 1 saved: chart1_category_sales.png")

# --- Chart 2: Monthly Sales Trend ---
plt.figure(figsize=(14, 5))
plt.plot(monthly_sales['Month-Year'],
         monthly_sales['Sales'],
         marker='o',
         color='steelblue',
         linewidth=2)
plt.title('Monthly Sales Trend (All Years)', fontsize=14, fontweight='bold')
plt.ylabel('Sales ($)')
plt.xlabel('Month')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('outputs/chart2_monthly_trend.png', dpi=150)
plt.show()
print("✅ Chart 2 saved: chart2_monthly_trend.png")

# --- Chart 3: Profit by Region ---
plt.figure(figsize=(8, 5))
region_data['Profit'].sort_values().plot(kind='barh',
                                          color='teal',
                                          edgecolor='white')
plt.title('Total Profit by Region', fontsize=14, fontweight='bold')
plt.xlabel('Profit ($)')
plt.tight_layout()
plt.savefig('outputs/chart3_region_profit.png', dpi=150)
plt.show()
print("✅ Chart 3 saved: chart3_region_profit.png")

# --- Chart 4: Sales vs Profit by Category (bubble-style) ---
plt.figure(figsize=(8, 5))
cat_data = df.groupby('Category')[['Sales', 'Profit']].sum()
plt.scatter(cat_data['Sales'],
            cat_data['Profit'],
            s=500,
            alpha=0.7,
            color=['steelblue', 'teal', 'orange'])
for i, txt in enumerate(cat_data.index):
    plt.annotate(txt,
                 (cat_data['Sales'].iloc[i], cat_data['Profit'].iloc[i]),
                 textcoords="offset points",
                 xytext=(10, 5),
                 fontsize=10)
plt.title('Sales vs Profit by Category', fontsize=14, fontweight='bold')
plt.xlabel('Sales ($)')
plt.ylabel('Profit ($)')
plt.tight_layout()
plt.savefig('outputs/chart4_sales_vs_profit.png', dpi=150)
plt.show()
print("✅ Chart 4 saved: chart4_sales_vs_profit.png")


# PART 5: Save cleaned data for Looker Studio

df.to_csv('outputs/cleaned_superstore.csv', index=False)
print("\n✅ Cleaned data saved to: outputs/cleaned_superstore.csv")
print("👉 You'll upload this file to Google Looker Studio next!")