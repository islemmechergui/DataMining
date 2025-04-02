import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.frequent_patterns import apriori, association_rules


print("")
df = pd.read_excel("Online Retail.xlsx")

# Nettoyage
print("Nettoyage des données")
df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
df = df.dropna(subset=['CustomerID'])
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

# Préparation des transactions pour Apriori
print("Préparation des transactions pour l'algorithme Apriori")
basket = df.groupby(['InvoiceNo', 'Description'])['Quantity'].sum().unstack().fillna(0)

basket = (basket > 0)


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
plt.figure(figsize=(10,6))
sns.scatterplot(x=strong_rules['support'], y=strong_rules['confidence'],
                size=strong_rules['lift'], hue=strong_rules['lift'],
                palette='coolwarm', alpha=0.7)
plt.xlabel("Support")
plt.ylabel("Confiance")
plt.title("Règles d'association - Support vs Confiance")
plt.legend(title="Lift")
plt.show()

# résultats
strong_rules.to_csv("/Users/assiasannen/projetDataMining/association_rules_results.csv", index=False)



# Charger les règles d'association sauvegardées
print("Chargement des règles d'association...")
rules = pd.read_csv("association_rules_results.csv")

# Proposer des stratégies de cross-selling basées sur les résultats
print("Analyse des stratégies de cross-selling")
cross_selling_recommendations = strong_rules[['antecedents', 'consequents', 'lift']]

# Afficher quelques recommandations
print("\n Recommandations de Cross-Selling :")
for index, row in cross_selling_recommendations.iterrows():
    antecedent_items = ', '.join(row['antecedents'])  # Convertir frozenset en liste lisible
    consequent_items = ', '.join(row['consequents'])  # Convertir frozenset en liste lisible
    print(f" Si un client achète [{antecedent_items}], recommandez [{consequent_items}] (Lift: {row['lift']:.2f})")

# Sauvegarde des recommandations avec un format lisible
cross_selling_recommendations['antecedents'] = cross_selling_recommendations['antecedents'].apply(lambda x: ', '.join(x))
cross_selling_recommendations['consequents'] = cross_selling_recommendations['consequents'].apply(lambda x: ', '.join(x))

cross_selling_recommendations.to_csv("/Users/assiasannen/projetDataMining/cross_selling_recommendations.csv", index=False)
print("\nRecommandations de cross-selling sauvegardées dans 'cross_selling_recommendations.csv'")

