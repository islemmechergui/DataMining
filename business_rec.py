import pandas as pd
import matplotlib.pyplot as plt

# Chargement des règles d'association
print("\nChargement des règles d'association...")
try:
    rules = pd.read_csv("association_rules_results.csv")  # adapte le chemin si besoin
    print(f"{len(rules)} règles chargées avec succès.")
except FileNotFoundError:
    print(" Le fichier 'regles_association.csv' est introuvable. Vérifie le chemin.")
    rules = pd.DataFrame()  # crée un DataFrame vide pour éviter une erreur

# Conversion sécurisée des colonnes de chaînes en frozensets
def safe_frozenset_conversion(value):
    if isinstance(value, str) and value.startswith("frozenset"):
        return eval(value)
    return value

rules['antecedents'] = rules['antecedents'].apply(safe_frozenset_conversion)
rules['consequents'] = rules['consequents'].apply(safe_frozenset_conversion)

# Génération de recommandations business à partir des règles
def recommandations_business(rules):
    recommandations = []
    for _, rule in rules.iterrows():
        antecedents = rule['antecedents']
        consequents = rule['consequents']
        recommandations.append(
            f"Les clients qui achètent {antecedents} devraient être incités à acheter {consequents} (Lift: {rule['lift']:.2f})"
        )
    return recommandations

print("\nGénération des recommandations business")
tips = recommandations_business(rules)
for tip in tips[:5]:  # Afficher les 5 premières
    print(tip)

# Sauvegarde des recommandations
with open("business_recommendations.txt", "w") as f:
    for tip in tips:
        f.write(tip + "\n")

print("Recommandations business sauvegardées dans 'business_recommendations.txt'")

# 1. Chargement des résultats de segmentation
print("Chargement de la segmentation client...")
seg_df = pd.read_csv("segmentation_results.csv")

# Nettoyage des colonnes
seg_df.columns = seg_df.columns.str.strip()

# Vérification du nom des colonnes
print("Colonnes disponibles :", seg_df.columns.tolist())

# 2. Définir les profils clients en fonction des clusters  Cluster_KMeans et Cluster_CAH
cluster_profiles_kmeans = {
    0: "Clients fidèles",
    1: "Clients à potentiel",
    2: "Clients inactifs"
}

cluster_profiles_cah = {
    0: "Clients hautement engagés",
    1: "Clients moyens",
    2: "Clients faibles"
}

# 3. Stratégies marketing ciblées pour chaque profil
marketing_strategies = {
    "Clients fidèles": "Proposez des avantages exclusifs, avant-premières, et programmes de fidélité.",
    "Clients à potentiel": "Mettez en avant des offres limitées dans le temps et recommandations personnalisées.",
    "Clients inactifs": "Envoyez des emails de réactivation avec réductions ciblées et nouveaux produits.",
    "Clients hautement engagés": "Proposez des produits premium, VIP et service client prioritaire.",
    "Clients moyens": "Offres ciblées en fonction des tendances de consommation.",
    "Clients faibles": "Incitations à l'achat via promotions ou gamification."
}

# 4. Attribution des profils et stratégies pour K-means et CAH
seg_df['Profil_KMeans'] = seg_df['Cluster_KMeans'].map(cluster_profiles_kmeans)
seg_df['Profil_CAH'] = seg_df['Cluster_CAH'].map(cluster_profiles_cah)

seg_df['Stratégie marketing'] = seg_df['Profil_KMeans'].map(marketing_strategies)
seg_df['Stratégie marketing_CAH'] = seg_df['Profil_CAH'].map(marketing_strategies)

# 5. Affichage des recommandations
print("\nExtrait des recommandations :")
print(seg_df[['CustomerID', 'Profil_KMeans', 'Stratégie marketing', 'Profil_CAH', 'Stratégie marketing_CAH']].head())

# 6. Sauvegarde des recommandations dans un nouveau CSV
seg_df.to_csv("recommandations_clients.csv", index=False)
print("\nFichier 'recommandations_clients.csv' sauvegardé avec succès.")

# 7. Visualisation des segments (camembert)
segment_counts_kmeans = seg_df['Profil_KMeans'].value_counts()
segment_counts_cah = seg_df['Profil_CAH'].value_counts()

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.pie(segment_counts_kmeans, labels=segment_counts_kmeans.index, autopct='%1.1f%%', startangle=140, colors=["#66b3ff", "#99ff99", "#ffcc99"])
plt.title("Répartition des segments clients (K-means)")
plt.axis('equal')

plt.subplot(1, 2, 2)
plt.pie(segment_counts_cah, labels=segment_counts_cah.index, autopct='%1.1f%%', startangle=140, colors=["#ff9999", "#66b3ff", "#99ff99"])
plt.title("Répartition des segments clients (CAH)")
plt.axis('equal')

plt.tight_layout()
plt.show()

# Analyse des produits les moins vendus
print("\nAnalyse des produits les moins vendus")

if not rules.empty:
    low_sales_products = rules[rules['support'] < 0.01]
    if not low_sales_products.empty:
        print("Produits à faible support :")
        print(low_sales_products[['antecedents', 'consequents', 'support']])
        print("Actions possibles : Retrait du catalogue, packs promotionnels, marketing ciblé")
    else:
        print("Aucun produit avec un support < 0.01")
else:
    print("Aucune règle d'association disponible.")

# Recommandations pour améliorer la fidélisation client
print("\nRecommandations pour améliorer la fidélisation client")

fidelisation_strategies = {
    "Personnalisation des recommandations": "Utiliser les historiques d'achats et préférences pour suggérer des produits adaptés.",
    "Offres basées sur la fréquence d'achat": "Réductions exclusives pour les clients ayant acheté au moins 5 fois en 6 mois.",
    "Programme VIP": "Créer des niveaux de fidélité (Silver, Gold, Platinum) avec des récompenses croissantes.",
    "Service client amélioré": "Assistance prioritaire et retours gratuits pour les clients fidèles.",
    "Rappels personnalisés": "Envoyer des emails et notifications push sur les offres et nouveaux produits adaptés."
}

for strategie, description in fidelisation_strategies.items():
    print(f"- {strategie}: {description}")

# Sauvegarde des recommandations de fidélisation
with open("fidelisation_recommendations.txt", "w") as f:
    for strategie, description in fidelisation_strategies.items():
        f.write(f"{strategie}: {description}\n")

print("Les recommandations de fidélisation ont été enregistrées dans 'fidelisation_recommendations.txt'")


