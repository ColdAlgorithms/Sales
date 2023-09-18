# import libraries
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# read feather file
sales_df = pd.read_feather("sales-data.feather")
# add period columns to sales dataframe in order to prepare for monthly analysis 
sales_df['datetime'] = [datetime.strptime(str(i),"%Y%m%d") for i in sales_df['sales_date_id']]
sales_df['period'] = [i.strftime("%Y-%m") for i in sales_df['datetime']]

# create a monthly sales dataframe with columns: date, sales amount, number of sales and number of customers with sales
monthly_sales = pd.DataFrame(columns=['period', 'sales_amount', 'sales_count', 'customer_count', 'sales_amount_per_customer', 'sales_amount_per_sale', 'sales_count_per_customer'])
# calculate monthly sales amount, number of sales and number of customers with sales
monthly_sales['sales_amount'] = sales_df.groupby('period')['amount'].sum()
monthly_sales['sales_count'] = sales_df.groupby('period')['id'].count()
monthly_sales['customer_count'] = sales_df.groupby('period')['customer_id'].nunique()
# calculate sales amount per customer, sales amount per sale and sales count per customer
monthly_sales['sales_amount_per_customer'] = monthly_sales['sales_amount'] / monthly_sales['customer_count']
monthly_sales['sales_amount_per_sale'] = monthly_sales['sales_amount'] / monthly_sales['sales_count']
monthly_sales['sales_count_per_customer'] = monthly_sales['sales_count'] / monthly_sales['customer_count']
# copy index to the period column and reset index
monthly_sales['period'] = [i for i in monthly_sales.index]
monthly_sales.reset_index(drop=True, inplace=True)

fig, axs = plt.subplots(2, 3, figsize=(12, 6))

# Plot 1: Sales Amount Per Mount
axs[0, 0].plot(monthly_sales['period'], monthly_sales['sales_amount']/1000000, marker='o', linestyle='-', color='b')
axs[0, 0].set_title('Ciro')
axs[0, 0].set_xlabel('Dönem')
axs[0, 0].set_ylabel('Satışlar (mn TL)')

# Plot 2: Number of Sales Per Month
axs[0, 1].plot(monthly_sales['period'], monthly_sales['sales_count'], marker='o', linestyle='-', color='g')
axs[0, 1].set_title('Satış Adedi')
axs[0, 1].set_xlabel('Dönem')
axs[0, 1].set_ylabel('Satış Adedi')

# Plot 3: Number of Customers With Sales Per Month
axs[0, 2].plot(monthly_sales['period'], monthly_sales['customer_count'], marker='o', linestyle='-', color='r')
axs[0, 2].set_title('Satış Yapılan Müşteri Adedi')
axs[0, 2].set_xlabel('Dönem')
axs[0, 2].set_ylabel('Müşteri Adedi')

# Plot 4: Sales Amount Per Sale
axs[1, 0].plot(monthly_sales['period'], monthly_sales['sales_amount_per_sale'], marker='o', linestyle='-', color='y')
axs[1, 0].set_title('Satış Başına Düşen Satış Tutarı')
axs[1, 0].set_xlabel('Period')
axs[1, 0].set_ylabel('Tutar (TL)')

# Plot 5: Sales Amount Per Customer
axs[1, 1].plot(monthly_sales['period'], monthly_sales['sales_amount_per_customer'], marker='o', linestyle='-', color='m')
axs[1, 1].set_title('Müşteri Başına Aylık Satış Tutarı')
axs[1, 1].set_xlabel('Dönem')
axs[1, 1].set_ylabel('Tutar (TL)')

# Plot 6: Number of Sales Per Customer
axs[1, 2].plot(monthly_sales['period'], monthly_sales['sales_count_per_customer'], marker='o', linestyle='-', color='c')
axs[1, 2].set_title('Müşteri Başına Aylık Satış Adedi')
axs[1, 2].set_xlabel('Dönem')
axs[1, 2].set_ylabel('Satış Adedi')

# Rotate period labels on x-axis for better visibility
for ax in axs.flat:
    ax.tick_params(axis='x', rotation=45)
# Set title of the figure
fig.suptitle('Dönemsel Satış Performansı', fontsize=18)
# Adjust spacing between subplots
plt.tight_layout()
# Display the plots
plt.show()
