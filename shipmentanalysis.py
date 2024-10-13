import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "group_project.csv"
df = pd.read_csv("C:\\Users\\235556\\OneDrive\\Desktop\\New folder\\group project.csv")

# Take a sample of 3001 records with random state 55045
sample_df = df.sample(n=3001, random_state=55045)

# Streamlit App Title
st.title("Interactive Shipment Analysis Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")
selected_shipping_method = st.sidebar.multiselect("Select Shipping Method:", options=sample_df['Shipping_Method'].unique(), default=sample_df['Shipping_Method'].unique())
selected_import_export = st.sidebar.multiselect("Select Import/Export:", options=sample_df['Import_Export'].unique(), default=sample_df['Import_Export'].unique())
selected_category = st.sidebar.multiselect("Select Product Category:", options=sample_df['Category'].unique(), default=sample_df['Category'].unique())

# Apply filters
filtered_df = sample_df[(sample_df['Shipping_Method'].isin(selected_shipping_method)) &
                        (sample_df['Import_Export'].isin(selected_import_export)) &
                        (sample_df['Category'].isin(selected_category))]

# Country-wise Import/Export Analysis
st.header("Top 5 Countries by Number of Products Imported and Exported")
import_data = filtered_df[filtered_df['Import_Export'] == 'Import']['Country'].value_counts().nlargest(5)
export_data = filtered_df[filtered_df['Import_Export'] == 'Export']['Country'].value_counts().nlargest(5)

fig, ax = plt.subplots(figsize=(14, 8))
ax.bar(import_data.index, import_data.values, alpha=0.6, label='Import', color='blue')
ax.bar(export_data.index, export_data.values, alpha=0.6, label='Export', color='green')
plt.xticks(rotation=90)
plt.xlabel('Country')
plt.ylabel('Number of Products')
plt.title('Top 5 Countries by Number of Products Imported and Exported')
plt.legend()
st.pyplot(fig)

# Payment Terms Across Product Categories
st.header("Payment Terms Across Product Categories")
payment_terms_category = filtered_df.groupby(['Category', 'Payment_Terms']).size().unstack(fill_value=0)
fig2, ax2 = plt.subplots(figsize=(14, 8))
payment_terms_category.plot(kind='bar', stacked=True, ax=ax2)
plt.xlabel('Product Category')
plt.ylabel('Number of Transactions')
plt.title('Payment Terms Across Product Categories')
plt.xticks(rotation=45)
plt.legend(title='Payment Terms')
st.pyplot(fig2)

# Quantity and Weight Distribution Across Shipping Methods
st.header("Quantity and Weight Distribution Across Shipping Methods")
fig3, ax3 = plt.subplots(1, 2, figsize=(18, 6))
sns.boxplot(x='Shipping_Method', y='Quantity', data=filtered_df, ax=ax3[0], showmeans=True, meanprops={"marker": "o", "markerfacecolor": "red", "markeredgecolor": "red"})
ax3[0].set_title('Quantity Distribution Across Shipping Methods')
ax3[0].set_xlabel('Shipping Method')
ax3[0].set_ylabel('Quantity')

sns.boxplot(x='Shipping_Method', y='Weight', data=filtered_df, ax=ax3[1], showmeans=True, meanprops={"marker": "o", "markerfacecolor": "red", "markeredgecolor": "red"})
ax3[1].set_title('Weight Distribution Across Shipping Methods')
ax3[1].set_xlabel('Shipping Method')
ax3[1].set_ylabel('Weight')

st.pyplot(fig3)

# Monthly Demand for Product Categories (Sunburst Chart)
st.header("Monthly Demand for Product Categories")
filtered_df['Date'] = pd.to_datetime(filtered_df['Date'], format='%d-%m-%Y')
filtered_df['Month'] = filtered_df['Date'].dt.month_name()
monthly_category_trade_volume = filtered_df.groupby(['Month', 'Category'])['Quantity'].sum().reset_index()
fig4 = px.sunburst(monthly_category_trade_volume, path=['Month', 'Category'], values='Quantity', title='Monthly Demand for Product Categories')
st.plotly_chart(fig4)

# Monthly Export Value (Sunburst Chart)
st.header("Monthly Export Value")
export_data = filtered_df[filtered_df['Import_Export'] == 'Export']
monthly_export_value = export_data.groupby(['Month'])['Value'].sum().reset_index()
fig5 = px.sunburst(monthly_export_value, path=['Month'], values='Value', title='Monthly Export Value')
st.plotly_chart(fig5)

# Product Category Trends Over Time
st.header("Product Category Trends Over Time")
monthly_category_trends = filtered_df.groupby(['Month', 'Category'])['Quantity'].sum().reset_index()
fig7 = px.line(monthly_category_trends, x='Month', y='Quantity', color='Category', title='Product Category Trends Over Time')
st.plotly_chart(fig7)

# Interactive Map for Trade Volume
st.header("Interactive Map for Trade Volume")
country_trade_volume = filtered_df.groupby('Country').agg({'Quantity': 'sum', 'Value': 'sum'}).reset_index()
fig6 = px.choropleth(country_trade_volume, locations='Country', locationmode='country names', color='Quantity',
                     hover_name='Country', hover_data=['Value'], title='Trade Volume by Country',
                     color_continuous_scale=px.colors.sequential.Plasma)
st.plotly_chart(fig6)

# Conclusion
st.write("""
This interactive dashboard provides insights into various aspects of the shipment data:
- The number of products imported and exported by each country.
- Payment terms used across different product categories.
- Quantity and weight distribution across shipping methods.
- Monthly demand for product categories and export values.
- Product category trends over time.
- Trade volume by country using an interactive map.
Use the filters on the sidebar to explore the data further.
""")