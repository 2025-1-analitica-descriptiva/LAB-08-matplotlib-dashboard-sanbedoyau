import pandas as pd
import matplotlib.pyplot as plt
import os
from glob import glob

def pregunta_01():
    def create_ouptput_directory(output_directory: str):
        if os.path.exists(output_directory):
            for file in glob(f'{output_directory}/*'):
                os.remove(file)
            os.rmdir(output_directory)
        os.makedirs(output_directory)

    in_path = 'files/input'
    out_path = 'docs'
    df = pd.read_csv(f'{in_path}/shipping-data.csv')

    def create_for_shipping_per_warehouse(DataFrame: pd.DataFrame):
        plt.figure()
        counts = DataFrame.Warehouse_block.value_counts()
        counts.plot.bar(title='Shipping per Warehouse',
                        xlabel='Warehouse block',
                        ylabel='Record count',
                        color='tab:blue',
                        fontsize=8)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.savefig(f'{out_path}/shipping_per_warehouse.png')

    def create_for_mode_of_shipment(DataFrame: pd.DataFrame):
        plt.figure()
        counts = DataFrame.Mode_of_Shipment.value_counts()
        counts.plot.pie(title='Mode of Shipment',
                        wedgeprops=dict(width=0.35),
                        ylabel='',
                        colors=['tab:blue', 'tab:orange', 'tab:green'])
        plt.savefig(f'{out_path}/mode_of_shipment.png')

    def create_for_average_customer_rating(DataFrame: pd.DataFrame):
        plt.figure()
        df = DataFrame.copy()
        df = (df[['Mode_of_Shipment', 'Customer_rating']]
              .groupby('Mode_of_Shipment').describe())
        df.columns = df.columns.droplevel()
        df = df[['mean', 'min', 'max']]
        plt.barh(y=df.index.values,
                 width=df['max'].values - 1,
                 left=df['min'].values,
                 height=0.9,
                 color='lightgray',
                 alpha=0.8)
        colors = ['tab:green' if value >= 3 else 'tab:orange'
                  for value in df['mean'].values]
        plt.barh(y=df.index.values,
                 width=df['mean'].values - 1,
                 left=df['min'].values,
                 height=0.5,
                 color=colors,
                 alpha=1)
        plt.title('Average Customer Rating')
        plt.gca().spines['left'].set_color('gray')
        plt.gca().spines['bottom'].set_color('gray')
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.savefig(f'{out_path}/average_customer_rating.png')

    def create_for_weight_distribution(DataFrame: pd.DataFrame):
        plt.figure()
        DataFrame.Weight_in_gms.plot.hist(
            title='Shipped weight distribution',
            color='tab:orange',
            edgecolor='white'
        )
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.savefig(f'{out_path}/weight_distribution.png')

    html = '''<!DOCTYPE html>
<html>
    <head>
        <title>Dashboard</title>
    </head>
    <body>
        <h1>Shipping Dashboard</h1>
        <div style = "width: 45%; float: left">
            <img src = "shipping_per_warehouse.png" alt = "Fig 1">
            <img src = "mode_of_shipment.png" alt = "Fig 2">
        </div>
        <div style = "width: 45%; float: left">
            <img src = "average_customer_rating.png" alt = "Fig 3">
            <img src = "weight_distribution.png" alt = "Fig 4">
        </div>
    </body>
</html>'''

    create_ouptput_directory(f'{out_path}')
    create_for_shipping_per_warehouse(df)
    create_for_mode_of_shipment(df)
    create_for_average_customer_rating(df)
    create_for_weight_distribution(df)

    with open(f'{out_path}/index.html', 'w') as file:
        file.write(html)