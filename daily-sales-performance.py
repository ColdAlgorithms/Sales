# import libraries
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# read feather file
sales_df = pd.read_feather("sales-data.feather")

# overview the data set
print("\033[1mOverview Sales Data Set\033[0m")
print("\n")
sales_df.info()
print("\n")
sales_df.describe()

# create a daily sales dataframe with columns: date, sales amount, number of sales and number of customers with sales 
daily_sales = pd.DataFrame(columns=['datetime', 'sales_amount', 'sales_count', 'customer_count'])
daily_sales['sales_amount'] = sales_df.groupby('sales_date_id')['amount'].sum()
daily_sales['sales_count'] = sales_df.groupby('sales_date_id')['id'].count()
daily_sales['customer_count'] = sales_df.groupby('sales_date_id')['customer_id'].nunique()
daily_sales['datetime'] = [datetime.strptime(str(i),"%Y%m%d") for i in daily_sales.index]
daily_sales.reset_index(drop=True, inplace=True)

# create graphics and define graphic sizes
fig, axs = plt.subplots(3, 1, figsize=(12, 8))

#give graphic title and axis names
subtitles = ['Satış Tutarı', 'Satış Adedi', 'Satış Yapılan Müşteri Adedi']
[axs[i].set_title(subtitles[i]) for i in range(3)]
#set labels of first graphic
axs[0].set_xlabel('Tarih')
axs[0].set_ylabel('Şatışlar (mn TL)')
# draw sales trend by day
axs[0].plot(daily_sales['datetime'], daily_sales['sales_amount'], color='red')
#set labels of second graphic
axs[1].set_xlabel('Tarih')
axs[1].set_ylabel('Satış Adedi')
# draw sales count by day
axs[1].bar(daily_sales['datetime'], daily_sales['sales_count'], color='green')
#set labels of third graphic
axs[2].set_xlabel('Tarih')
axs[2].set_ylabel('Müşteri Adedi')
# draw customer count by day
axs[2].bar(daily_sales['datetime'], daily_sales['customer_count'], color='blue')

fig.suptitle('Günlük Satış Performansı', fontsize=18)
# give grid to graphics
[i.grid(True) for i in axs]
#optimise graphics' layout
plt.tight_layout()
#display the graphic
plt.show()
