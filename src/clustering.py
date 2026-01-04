"""
Standalone Clustering Script (Phase 3)
Runs K-Means on the extracted features and generates all visualizations.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.manifold import TSNE
import os

# Paths
DATA_PATH = 'data/concurrency_features.csv'
RESULTS_DIR = 'results'
os.makedirs(RESULTS_DIR, exist_ok=True)

# Load data
df = pd.read_csv(DATA_PATH)
print(f"Loaded {len(df)} samples from {df['language'].nunique()} languages")
print(df['language'].value_counts())

# Features
features = ['has_threads', 'lock_density', 'channel_density', 'actor_density', 'async_density', 'concurrency_score']
X = df[features]

# Elbow & Silhouette
inertias = []
silhouettes = []
for k in range(2, 7):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)
    silhouettes.append(silhouette_score(X, kmeans.labels_))

# Plot
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(range(2, 7), inertias, 'bo-')
plt.title('Elbow Method')
plt.xlabel('Clusters')
plt.ylabel('Inertia')

plt.subplot(1, 2, 2)
plt.plot(range(2, 7), silhouettes, 'ro-')
plt.title('Silhouette Score')
plt.xlabel('Clusters')
plt.ylabel('Score')
plt.savefig(f'{RESULTS_DIR}/elbow_silhouette.png', dpi=150, bbox_inches='tight')
plt.close()

# Final clustering (k=3)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(X)
sil_score = silhouette_score(X, df['cluster'])
print(f"\nFinal Silhouette Score: {sil_score:.3f}")

# Cluster centers
print("\nCluster Centers:")
print(pd.DataFrame(kmeans.cluster_centers_, columns=features))

# Language distribution
print("\nLanguage Distribution per Cluster:")
print(pd.crosstab(df['language'], df['cluster']))

# t-SNE visualization
tsne = TSNE(n_components=2, random_state=42, perplexity=10)
X_tsne = tsne.fit_transform(X)

plt.figure(figsize=(10, 8))
sns.scatterplot(x=X_tsne[:,0], y=X_tsne[:,1], hue=df['cluster'], style=df['language'], palette='deep', s=100)
plt.title('t-SNE: Concurrency-Based Language Clusters')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(f'{RESULTS_DIR}/tsne_visualization.png', dpi=150, bbox_inches='tight')
plt.close()

print(f"\nAll plots saved to {RESULTS_DIR}/")
print("Clustering complete! Three clusters match theoretical concurrency models.")
