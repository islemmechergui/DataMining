import pandas as pd

def creer_variables_rfm(df):
    reference_date = df['InvoiceDate'].max()
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (reference_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'TotalAmount': 'sum'
    }).rename(columns={'InvoiceDate': 'Recency', 'InvoiceNo': 'Frequency', 'TotalAmount': 'Monetary'})

    return rfm


if __name__ == "__main__":
    df = pd.read_csv("cleaned_data.csv", parse_dates=['InvoiceDate'])  # Charger les données nettoyées
    rfm = creer_variables_rfm(df)
    rfm.to_csv("rfm_data.csv")  # Sauvegarde des données RFM
    print("Données RFM sauvegardées dans 'rfm_data.csv'.")
    print(rfm.head())  # Affiche les premières lignes des données RFM
