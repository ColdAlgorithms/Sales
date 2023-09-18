import pandas as pd

# Automation Variables
filename = "x-distributor-sales-transactions.xlsx"
product_name = "STOCK NAME"
quantity = "QUANTITY"
amount = "NET PRICE"

# Distributor Report
df = pd.read_excel(filename)
df = df[df['TRANSACTION TYPE'] == 'SELL ']
products = df[product_name].unique()

# Indomie Report
summary = pd.DataFrame(columns=['Product Name', 'Product Group', 'Quantity', 'Amount'])
summary['Product Name'] = products

index = 0
for i in products:
    try:
            if "dark cohocolate" in i.lower():
                summary.loc(0)[index][1] = "Dark Chocolate"
            elif "milk chocolate":
                summary.loc(0)[index][1] = "Milk Chocolate"
            else:
                summary.loc(0)[index][1] = "White Chocolate"
    except AttributeError:
            pass
    summary.loc(0)[index][2] = df[df[product_name] == i][quantity].sum()
    summary.loc(0)[index][3] = df[df[product_name] == i][amount].sum()
    index += 1
    
summary.to_excel(f"{filename[:-5]}-summary.xlsx", index=False)
