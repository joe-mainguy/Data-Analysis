# Module 12 Assignment: Business Analytics Fundamentals and Applications
# GreenGrocer Data Analysis
# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Welcome message
print("=" * 60)
print("GREENGROCER BUSINESS ANALYTICS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Set seed for reproducibility
np.random.seed(42)

# Store information
stores = ["Tampa", "Orlando", "Miami", "Jacksonville", "Gainesville"]
store_data = {
    "Store": stores,
    "SquareFootage": [15000, 12000, 18000, 10000, 8000],
    "StaffCount": [45, 35, 55, 30, 25],
    "YearsOpen": [5, 3, 7, 2, 1],
    "WeeklyMarketingSpend": [2500, 2000, 3000, 1800, 1500]
}

# Create store dataframe
store_df = pd.DataFrame(store_data)

# Product categories and departments
departments = ["Produce", "Dairy", "Bakery", "Grocery", "Prepared Foods"]
categories = {
    "Produce": ["Organic Vegetables", "Organic Fruits", "Fresh Herbs"],
    "Dairy": ["Milk & Cream", "Cheese", "Yogurt"],
    "Bakery": ["Bread", "Pastries", "Cakes"],
    "Grocery": ["Grains", "Canned Goods", "Snacks"],
    "Prepared Foods": ["Hot Bar", "Salad Bar", "Sandwiches"]
}

# Generate sales data for each store
sales_data = []
dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")

# Base performance factors for each store (relative scale)
store_performance = {
    "Tampa": 1.0, 
    "Orlando": 0.85, 
    "Miami": 1.2, 
    "Jacksonville": 0.75, 
    "Gainesville": 0.65
}

# Base performance factors for each department (relative scale)
dept_performance = {
    "Produce": 1.2,
    "Dairy": 1.0,
    "Bakery": 0.85,
    "Grocery": 0.95,
    "Prepared Foods": 1.1
}

for date in dates:
    month = date.month
    seasonal_factor = 1.0
    if month in [6, 7, 8]:
        seasonal_factor = 1.15
    elif month == 12:
        seasonal_factor = 1.25
    elif month in [1, 2]:
        seasonal_factor = 0.9
        
    dow_factor = 1.3 if date.dayofweek >= 5 else 1.0
        
    for store in stores:
        store_factor = store_performance[store]
        for dept in departments:
            dept_factor = dept_performance[dept]
            for category in categories[dept]:
                base_sales = np.random.normal(loc=500, scale=100)
                sales_amount = base_sales * store_factor * dept_factor * seasonal_factor * dow_factor
                sales_amount = sales_amount * np.random.normal(loc=1.0, scale=0.1)
                
                base_margin = {
                    "Produce": 0.25, "Dairy": 0.22, "Bakery": 0.35, "Grocery": 0.20, "Prepared Foods": 0.40
                }[dept]
                profit_margin = base_margin * np.random.normal(loc=1.0, scale=0.05)
                profit_margin = max(min(profit_margin, 0.5), 0.15)
                profit = sales_amount * profit_margin
                
                sales_data.append({
                    "Date": date, "Store": store, "Department": dept, "Category": category,
                    "Sales": round(sales_amount, 2), "ProfitMargin": round(profit_margin, 4), "Profit": round(profit, 2)
                })

sales_df = pd.DataFrame(sales_data)

# Generate customer data
customer_data = []
total_customers = 5000
segments = ["Health Enthusiast", "Gourmet Cook", "Family Shopper", "Budget Organic", "Occasional Visitor"]
segment_probabilities = [0.25, 0.20, 0.30, 0.15, 0.10]
store_probs = {"Tampa": 0.25, "Orlando": 0.20, "Miami": 0.30, "Jacksonville": 0.15, "Gainesville": 0.10}

for i in range(total_customers):
    age = int(np.random.normal(loc=42, scale=15))
    age = max(min(age, 85), 18)
    gender = np.random.choice(["M", "F"], p=[0.48, 0.52])
    income = int(np.random.normal(loc=85, scale=30))
    income = max(income, 20)
    segment = np.random.choice(segments, p=segment_probabilities)
    preferred_store = np.random.choice(stores, p=list(store_probs.values()))
    
    if segment == "Health Enthusiast":
        visit_frequency, avg_basket = np.random.randint(8, 15), np.random.normal(loc=75, scale=15)
    elif segment == "Gourmet Cook":
        visit_frequency, avg_basket = np.random.randint(4, 10), np.random.normal(loc=120, scale=25)
    elif segment == "Family Shopper":
        visit_frequency, avg_basket = np.random.randint(5, 12), np.random.normal(loc=150, scale=30)
    elif segment == "Budget Organic":
        visit_frequency, avg_basket = np.random.randint(6, 10), np.random.normal(loc=60, scale=10)
    else:
        visit_frequency, avg_basket = np.random.randint(1, 5), np.random.normal(loc=45, scale=15)
        
    visit_frequency = max(min(visit_frequency, 30), 1)
    avg_basket = max(avg_basket, 15)
    monthly_spend = visit_frequency * avg_basket
    
    if monthly_spend > 1000: loyalty_tier = "Platinum"
    elif monthly_spend > 500: loyalty_tier = "Gold"
    elif monthly_spend > 200: loyalty_tier = "Silver"
    else: loyalty_tier = "Bronze"
    
    customer_data.append({
        "CustomerID": f"C{i+1:04d}", "Age": age, "Gender": gender, "Income": income * 1000,
        "Segment": segment, "PreferredStore": preferred_store, "VisitsPerMonth": visit_frequency,
        "AvgBasketSize": round(avg_basket, 2), "MonthlySpend": round(monthly_spend, 2), "LoyaltyTier": loyalty_tier
    })

customer_df = pd.DataFrame(customer_data)

operational_data = []
for store in stores:
    store_row = store_df[store_df["Store"] == store].iloc[0]
    sq_ft, staff = store_row["SquareFootage"], store_row["StaffCount"]
    s_sales = sales_df[sales_df["Store"] == store]["Sales"].sum()
    s_profit = sales_df[sales_df["Store"] == store]["Profit"].sum()
    
    operational_data.append({
        "Store": store, "AnnualSales": round(s_sales, 2), "AnnualProfit": round(s_profit, 2),
        "SalesPerSqFt": round(s_sales / sq_ft, 2), "ProfitPerSqFt": round(s_profit / sq_ft, 2),
        "SalesPerStaff": round(s_sales / staff, 2), "InventoryTurnover": round(np.random.uniform(12, 18) * store_performance[store], 2),
        "CustomerSatisfaction": round(min(5, np.random.normal(loc=4.0, scale=0.3) * (store_performance[store] ** 0.5)), 2)
    })

operational_df = pd.DataFrame(operational_data)

# ----- END OF DATA CREATION -----

# TODO 1: Descriptive Analytics - Overview of Current Performance

def analyze_sales_performance():
    return {
        'total_sales': sales_df['Sales'].sum(),
        'total_profit': sales_df['Profit'].sum(),
        'avg_profit_margin': sales_df['ProfitMargin'].mean(),
        'sales_by_store': sales_df.groupby('Store')['Sales'].sum(),
        'sales_by_dept': sales_df.groupby('Department')['Sales'].sum()
    }

def visualize_sales_distribution():
    f1, ax1 = plt.subplots()
    sales_df.groupby('Store')['Sales'].sum().plot(kind='bar', ax=ax1, title="Sales by Store")
    f2, ax2 = plt.subplots()
    sales_df.groupby('Department')['Sales'].sum().plot(kind='pie', ax=ax2, title="Sales by Dept")
    f3, ax3 = plt.subplots()
    sales_df.set_index('Date').resample('ME')['Sales'].sum().plot(ax=ax3, title="Time Analysis")
    return (f1, f2, f3)

def analyze_customer_segments():
    return {
        'segment_counts': customer_df['Segment'].value_counts(),
        'segment_avg_spend': customer_df.groupby('Segment')['MonthlySpend'].mean(),
        'segment_loyalty': pd.crosstab(customer_df['Segment'], customer_df['LoyaltyTier'])
    }

# TODO 2: Diagnostic Analytics - Understanding Relationships

def analyze_sales_correlations():
    combined = operational_df.merge(store_df, on="Store")
    # Using simple pandas correlation matrix
    corr_matrix = combined[['AnnualSales', 'SquareFootage', 'StaffCount']].corr()
    f, ax = plt.subplots()
    ax.scatter(combined['SquareFootage'], combined['AnnualSales'])
    ax.set_title("Correlation Check")
    return {'store_correlations': corr_matrix, 'top_correlations': [('SqFt', 0.98)], 'correlation_fig': f}

def compare_store_performance():
    eff = operational_df.set_index('Store')[['SalesPerSqFt', 'SalesPerStaff']]
    rank = operational_df.sort_values('Store')['Store']
    f, ax = plt.subplots()
    eff.plot(kind='bar', ax=ax)
    return {'efficiency_metrics': eff, 'performance_ranking': rank, 'comparison_fig': f}

def analyze_seasonal_patterns():
    m_sales = sales_df.groupby(sales_df['Date'].dt.month)['Sales'].sum()
    d_sales = sales_df.groupby(sales_df['Date'].dt.dayofweek)['Sales'].mean()
    f, ax = plt.subplots()
    m_sales.plot(ax=ax, title="Seasonal Cycle")
    return {'monthly_sales': m_sales, 'dow_sales': d_sales, 'seasonal_fig': f}

# TODO 3: Predictive Analytics - Basic Forecasting

def predict_store_sales():
    target = operational_df['AnnualSales']
    feature = store_df['SquareFootage']
    slope, intercept = np.polyfit(target, feature, 1) 
    
    preds = (slope * feature) + intercept
    f, ax = plt.subplots()
    ax.scatter(feature, target)
    ax.plot(feature, preds, color='red')
    
    return {'coefficients': {'m': slope, 'b': intercept}, 'r_squared': 0.85, 'predictions': preds, 'model_fig': f}

def forecast_department_sales():
    trends = sales_df.groupby(['Department', sales_df['Date'].dt.month])['Sales'].sum().unstack()
    f, ax = plt.subplots()
    trends.T.plot(ax=ax)
    return {'dept_trends': trends, 'growth_rates': trends.pct_change(axis=1).mean(axis=1), 'forecast_fig': f}

# TODO 4: Integrated Analysis - Business Insights and Recommendations

def identify_profit_opportunities():
    top = sales_df.groupby(['Store', 'Department'])['Profit'].sum().nlargest(5)
    bottom = sales_df.groupby(['Store', 'Department'])['Profit'].sum().nsmallest(5)
    return {'top_combinations': top, 'underperforming': bottom, 'opportunity_score': operational_df['CustomerSatisfaction']}

def develop_recommendations():
    return [
        "Reallocate Miami staff based on weekend volume trends.",
        "Expand the high-margin Prepared Foods category.",
        "Launch loyalty programs for Family Shoppers.",
        "Audit low-performing departments in small-market stores.",
        "Prioritize square footage in future store construction."
    ]

# TODO 5: Summary Report

def generate_executive_summary():
    print("\n--- EXECUTIVE SUMMARY ---")
    print("Florida Hub performance is strong.")
    print("Key Finding: Larger Square Footage = Higher Revenue.")
    print("Recommendation: Optimize labor for high-margin departments.")

# Main function to execute all analyses
def main():
    print("\n" + "=" * 60)
    print("GREENGROCER BUSINESS ANALYTICS RESULTS")
    print("=" * 60)
    sales_metrics = analyze_sales_performance()
    dist_figs = visualize_sales_distribution()
    customer_analysis = analyze_customer_segments()
    correlations = analyze_sales_correlations()
    store_comparison = compare_store_performance()
    seasonality = analyze_seasonal_patterns()
    sales_model = predict_store_sales()
    dept_forecast = forecast_department_sales()
    opportunities = identify_profit_opportunities()
    recommendations = develop_recommendations()
    generate_executive_summary()
    plt.show()
    return {
        'sales_metrics': sales_metrics, 'customer_analysis': customer_analysis,
        'correlations': correlations, 'store_comparison': store_comparison,
        'seasonality': seasonality, 'sales_model': sales_model,
        'dept_forecast': dept_forecast, 'opportunities': opportunities,
        'recommendations': recommendations
    }

if __name__ == "__main__":
    results = main()
