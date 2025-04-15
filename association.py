
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.frequent_patterns import apriori, association_rules
from Prétraitement_données import Pretraitement_donnees  # Importer la fonction de nettoyage
from Calcul_RFM import creer_variables_rfm  # Importer la fonction de calcul RFM

# Chargement et nettoyage des données
file_name = "Online Retail.xlsx"
print("Nettoyage des données")
df = Pretraitement_donnees(file_name)  # Utiliser la fonction de prétraitement

# Préparation des données pour les règles d'association
print("Préparation des transactions pour l'algorithme Apriori")
basket = df.groupby(['InvoiceNo', 'Description'])['Quantity'].sum().unstack().fillna(0)
basket = (basket > 0)  # Conversion en matrice binaire

# Application de l'algorithme Apriori
print("Application de l'algorithme Apriori")
frequent_itemsets = apriori(basket, min_support=0.01, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

# Filtrer les règles avec un lift élevé
strong_rules = rules[(rules['lift'] > 1.2) & (rules['confidence'] > 0.5)]

# Affichage des règles d'association
print("Règles d'association fortes :")
print(strong_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

# Visualisation des règles les plus fortes
plt.figure(figsize=(10, 6))
sns.scatterplot(x=strong_rules['support'], y=strong_rules['confidence'],
                size=strong_rules['lift'], hue=strong_rules['lift'],
                palette='coolwarm', alpha=0.7)
plt.xlabel("Support")
plt.ylabel("Confiance")
plt.title("Règles d'association - Support vs Confiance")
plt.legend(title="Lift")
plt.show()

# Sauvegarde des résultats des règles
rules_output_path = "association_rules_results.csv"
strong_rules.to_csv(rules_output_path, index=False)

# Charger les règles d'association sauvegardées pour analyse
print("Chargement des règles d'association...")
rules = pd.read_csv(rules_output_path)

# Proposer des stratégies de cross-selling basées sur les résultats
print("Analyse des stratégies de cross-selling")
cross_selling_recommendations = strong_rules[['antecedents', 'consequents', 'lift']]

# Affichage des recommandations
print("\nRecommandations de Cross-Selling :")
for index, row in cross_selling_recommendations.iterrows():
    antecedent_items = ', '.join(row['antecedents'])  # Convertir frozenset en liste lisible
    consequent_items = ', '.join(row['consequents'])  # Convertir frozenset en liste lisible
    print(f"Si un client achète [{antecedent_items}], recommandez [{consequent_items}] (Lift: {row['lift']:.2f})")



# Sauvegarde des recommandations
cross_selling_recommendations.loc[:,'antecedents'] = cross_selling_recommendations['antecedents'].apply(lambda x: ', '.join(x))
cross_selling_recommendations.loc[:,'consequents'] = cross_selling_recommendations['consequents'].apply(lambda x: ', '.join(x))


cross_selling_recommendations.to_csv("/Users/assiasannen/projetDataMining/cross_selling_recommendations.csv", index=False)
print("\nRecommandations de cross-selling sauvegardées dans 'cross_selling_recommendations.csv'")
# Calcul des variables RFM pour analyse plus poussée
print("Calcul des variables RFM...")
rfm_data = creer_variables_rfm(df)  # Calcul des variables RFM
rfm_data.to_csv("rfm_data.csv", index=False)  # Sauvegarde des données RFM
print("Données RFM sauvegardées dans 'rfm_data.csv'.")
