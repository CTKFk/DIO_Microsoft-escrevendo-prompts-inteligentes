import pandas as pd

def load_and_combine_data(file_paths):
    """Carrega e combina múltiplos arquivos CSV em um único DataFrame."""
    dataframes = [pd.read_csv(path, encoding='utf-8', low_memory=False) for path in file_paths]
    return pd.concat(dataframes, ignore_index=True)

def get_top_selling_products(df, top_n=5):
    """Retorna os produtos mais e menos vendidos."""
    sales_summary = df.groupby("product_sold")["quantity"].sum().reset_index()
    sales_summary = sales_summary.sort_values(by="quantity", ascending=False)
    return sales_summary.head(top_n), sales_summary.tail(top_n)

def get_fastest_selling_products(df, top_n=5):
    """Retorna os produtos vendidos no menor espaço de tempo."""
    df["date"] = pd.to_datetime(df["date"], errors='coerce')
    sales_time = df.groupby("product_sold").agg(
        first_sale=("date", "min"),
        last_sale=("date", "max"),
        total_quantity=("quantity", "sum")
    ).reset_index()
    sales_time["days_selling"] = (sales_time["last_sale"] - sales_time["first_sale"]).dt.days + 1
    sales_time["days_selling"].replace(0, 1, inplace=True)
    sales_time["sales_per_day"] = sales_time["total_quantity"] / sales_time["days_selling"]
    return sales_time.sort_values(by="sales_per_day", ascending=False).head(top_n)

def main():
    file_paths = [
        "Meganium_Sales_Data_-_Etsy.csv",
        "Updated_Anbernic_Sales_Data.csv",
        "Meganium_Sales_Data.csv"
    ]
    df = load_and_combine_data(file_paths)
    
    top_selling, low_selling = get_top_selling_products(df)
    fastest_selling = get_fastest_selling_products(df)
    
    print("Top 5 Produtos Mais Vendidos:\n", top_selling)
    print("\nTop 5 Produtos Menos Vendidos:\n", low_selling)
    print("\nTop 5 Produtos Vendidos Mais Rápido:\n", fastest_selling)

if __name__ == "__main__":
    main()
