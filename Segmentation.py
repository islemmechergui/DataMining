import pandas as pd

# Regrouper les clients par cluster et calculer les moyennes RFM
cluster_summary = rfm.groupby('Cluster').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': 'mean'
}).round(2).reset_index()

# Ajouter une colonne de profil (facultatif)
def profiler(row):
    if row['Recency'] < 30 and row['Frequency'] > 10 and row['Monetary'] > 300:
        return 'Fidèle et actif'
    elif row['Recency'] > 150 and row['Frequency'] < 2:
        return 'Client perdu'
    else:
        return 'Acheteur occasionnel'

cluster_summary['Profil client'] = cluster_summary.apply(profiler, axis=1)

# Afficher ou sauvegarder
print(cluster_summary)
