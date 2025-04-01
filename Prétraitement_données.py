import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns


def Pretraitement_donnees(file_name):
    # Charger le dataset depuis le même répertoire que le script
    df = pd.read_excel(file_name)

    # Supprimer les annulations (factures commençant par 'C')
    df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]

    # Supprimer les valeurs manquantes dans CustomerID
    df = df.dropna(subset=['CustomerID'])

    # Supprimer les transactions avec quantités ou prix unitaires négatifs
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

    # Création de la colonne 'TotalAmount'
    df['TotalAmount'] = df['Quantity'] * df['UnitPrice']

    return df


# Charger le dataset et exécuter le script
if __name__ == "__main__":
    file_name = "Online Retail.xlsx"  # Définition du fichier source
    df = pd.read_excel(file_name)

    # Afficher les informations sur la base de données
    print("\nInformations sur la base de données:")
    print(df.info())

    # Afficher le nombre de lignes avant nettoyage
    print(f"\nNombre de lignes avant nettoyage: {df.shape[0]}")

    # Afficher un aperçu des premières lignes
    print(df.head())

    # Afficher des statistiques générales
    print("\nStatistiques avant nettoyage:")
    print(df.describe())

    # Nettoyage des données
    df = Pretraitement_donnees(file_name)
    df.to_csv("cleaned_data.csv", index=False)  # Sauvegarde des données nettoyées

    # Afficher les informations après nettoyage
    print("\nInformations après nettoyage:")
    print(df.info())

    # Afficher le nombre de lignes après nettoyage
    print(f"\nNombre de lignes après nettoyage: {df.shape[0]}")

    # Afficher un aperçu des premières lignes après nettoyage
    print(df.head())

    # Analyse exploratoire
    print("\nStatistiques après nettoyage:")
    print(df.describe())

    # Visualisation avec Seaborn
    sns.pairplot(df[['Quantity', 'UnitPrice', 'TotalAmount']])
    plt.show()
