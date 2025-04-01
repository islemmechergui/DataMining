import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt

def segmenter_kmeans(rfm):
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm)

    inertia = []
    for k in range(2, 10):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(rfm_scaled)
        inertia.append(kmeans.inertia_)

    plt.figure(figsize=(8,5))
    plt.plot(range(2, 10), inertia, marker='o')
    plt.title("Méthode du coude")
    plt.xlabel("Nombre de clusters")
    plt.ylabel("Inertie")
    plt.show()

    kmeans = KMeans(n_clusters=4, random_state=42)
    rfm['Cluster_KMeans'] = kmeans.fit_predict(rfm_scaled)
    return rfm

def segmenter_cah(rfm):
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm)

    plt.figure(figsize=(10, 5))
    linkage_matrix = linkage(rfm_scaled, method='ward')
    dendrogram(linkage_matrix)
    plt.title("Dendrogramme de la CAH")
    plt.show()

    cah = AgglomerativeClustering(n_clusters=4)
    rfm['Cluster_CAH'] = cah.fit_predict(rfm_scaled)
    return rfm

if __name__ == "__main__":
    rfm = pd.read_csv("rfm_data.csv")  # Charger les données RFM
    rfm = segmenter_kmeans(rfm)
    rfm = segmenter_cah(rfm)
    rfm.to_csv("segmentation_results.csv")  # Sauvegarde des clusters
    print("Segmentation terminée et résultats sauvegardés dans 'segmentation_results.csv'.")
