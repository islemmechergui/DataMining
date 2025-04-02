import pandas as pd
import ast
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


print("Chargement des règles d'association")
rules = pd.read_csv("association_rules_results.csv")
print(rules.head())
print(rules.dtypes)

# Convertir les chaînes en listes
def safe_frozenset_conversion(value):
    if isinstance(value, str) and value.startswith("frozenset"):
        return eval(value)
    return value

rules['antecedents'] = rules['antecedents'].apply(safe_frozenset_conversion)
rules['consequents'] = rules['consequents'].apply(safe_frozenset_conversion)

# générer des recommandations marketing
def recommandations_business(rules):
    recommandations = []
    for _, rule in rules.iterrows():
        antecedents = rule['antecedents']
        consequents = rule['consequents']
        recommandations.append(f"Les clients qui achètent {antecedents} devraient être incités à acheter"f" {consequents} (Lift: {rule['lift']:.2f})")
    return recommandations

# Génération des recommandations
print("Génération des recommandations business")
tips = recommandations_business(rules)
for tip in tips[:5]:  # Afficher les 5 premières recommandations
    print(tip)

# Sauvegarde des recommandations
with open("business_recommendations.txt", "w") as f:
    for tip in tips:
        f.write(tip + "\n")

print("Recommandations business sauvegardées dans 'business_recommendations.txt'")


print("Segmentation des clients")
customer_segments = {
    "Clients réguliers": "Programmes de fidélité et recommandations personnalisées",
    "Acheteurs occasionnels": "Promotions attractives pour encourager l'achat",
    "Grands acheteurs": "Offres premium et services exclusifs"
}
print(customer_segments)

# Aménagement du catalogue produit
print("Analyse des produits les moins vendus")
low_sales_products = rules[rules['support'] < 0.01]
if not low_sales_products.empty:
    print("Produits à faible support:")
    print(low_sales_products[['antecedents', 'consequents', 'support']])
    print("Actions possibles: Retrait du catalogue, Packs promotionnels, Marketing ciblé")

print("Recommandations pour améliorer la fidélisation client")

# Création d'un dictionnaire amélioré avec des recommandations plus spécifiques
fidelisation_strategies = {
    "Personnalisation des recommandations": "Utiliser les historiques d'achats et préférences pour suggérer des produits adaptés.",
    "Offres basées sur la fréquence d'achat": "Réductions exclusives pour les clients ayant acheté au moins 5 fois en 6 mois.",
    "Programme VIP": "Créer des niveaux de fidélité (Silver, Gold, Platinum) avec des récompenses croissantes.",
    "Service client amélioré": "Assistance prioritaire et retours gratuits pour les clients fidèles.",
    "Rappels personnalisés": "Envoyer des emails et notifications push sur les offres et nouveaux produits adaptés."
}

# Affichage des recommandations
for strategie, description in fidelisation_strategies.items():
    print(f"- {strategie}: {description}")

# Sauvegarde dans un fichier texte pour une meilleure traçabilité
with open("fidelisation_recommendations.txt", "w") as f:
    for strategie, description in fidelisation_strategies.items():
        f.write(f"{strategie}: {description}\n")

print("Les recommandations de fidélisation ont été enregistrées dans 'fidelisation_recommendations.txt'")

#heatmap (un plus)
data = pd.DataFrame([
    ["ALARM CLOCK BAKELIKE CHOCOLATE", "ALARM CLOCK BAKELIKE GREEN", 15.32],
    ["ALARM CLOCK BAKELIKE CHOCOLATE", "ALARM CLOCK BAKELIKE RED", 14.83],
    ["ALARM CLOCK BAKELIKE IVORY", "ALARM CLOCK BAKELIKE GREEN", 13.80]
],
    columns=["Antecedent", "Consequent", "Lift"])


df = pd.DataFrame(data)

# Pivot pour créer une matrice et remplacer NaN par 0
lift_matrix = df.pivot(index="Antecedent", columns="Consequent", values="Lift").fillna(0)

# Création de la heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(lift_matrix, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, cbar=True)

# Titres et labels
plt.title("Heatmap des Lifts entre Produits", fontsize=14, fontweight='bold')
plt.xlabel("Produits Conséquents", fontsize=12)
plt.ylabel("Produits Antécédents", fontsize=12)

# Affichage de la heatmap
plt.show()
