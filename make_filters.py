import glob
import os
import time

from sklearn.cluster import KMeans

import BloomFilter
import load_model
import load_wiki

# PREFERENCES
full_wiki = False

if full_wiki:
    model_path = "doc2vec.model"
    wiki_path = r"C:\Users\jacob\Desktop/wiki/*/*"
    suffix = "_full"
else:
    model_path = "simple.model"
    wiki_path = "/Users/Jacob/Desktop/example_wiki/*/*"
    suffix = "_simple"

vectors = load_model.get_model_vectors(model_path)
doctags = list(vectors.doctags.keys())  # This is correct order
clusters = {}

# Run KMeans
startTime = time.time()
kmeans = KMeans(200, init='k-means++', random_state=0, max_iter=100, verbose=False)
X = kmeans.fit(vectors.doctag_syn0)
labels = kmeans.labels_.tolist()
centroids = kmeans.cluster_centers_.tolist()
print("seconds spent on kmeans: %s seconds" % (time.time() - startTime))

# Set titles for each cluster
for i in range(len(labels)):
    label = labels[i]
    wiki_title = doctags[i]
    if label in clusters:
        clusters[label].append(wiki_title)
    else:
        clusters[label] = [wiki_title]
print("Loading in wiki articles")
startTime = time.time()
# Load in wiki articles
article_dict = load_wiki.load_wiki_files(wiki_path)
print("seconds spent on loading wiki: %s seconds" % (time.time() - startTime))
# Remove previous centroid file and filters_full, if exists
try:
    os.remove("centroids%s.txt" % suffix)
except:
    pass
try:
    filters = glob.glob("./filters%s/*" % suffix)
    for filt in filters:
        os.remove(filt)
except:
    pass
try:
    os.remove("cluster_sample%s.txt" % suffix)
except:
    pass

# For every cluster, make a bloom filter. Save filter and centroid to disk
startTime = time.time()
clusterSize = [] # Debugging
for clusterNo in sorted(clusters.keys()):
    wiki_titles = clusters[clusterNo]
    clusterSize.append(len(wiki_titles))
    all_sentences = []
    sentence_amount = 0
    for title in wiki_titles:
        if title in article_dict:
            sentences = BloomFilter.prepare_sentences(article_dict[title])
            sentence_amount += len(sentences)
            all_sentences.append(sentences)
    filter = BloomFilter.BloomFilter(m=sentence_amount)
    for sentences in all_sentences:
        filter.train(sentences)
    fileName = 'filters%s/%s.bits' % (suffix, clusterNo)
    filter.saveFilter(fileName)
    # centroid
    centroid = centroids[clusterNo]
    with open('centroids%s.txt' % suffix, 'a') as f:
        f.write("%s\n" % centroid)
    # Save 100 wiki titles from each cluster (showcase)
    with open("cluster_sample%s.txt" % suffix, "a") as f:
        f.write("%s: %s\n" % (len(wiki_titles), [title.encode("utf-8") for title in wiki_titles[:100]]))

print("Size of clusters: %s" % clusterSize)
print("seconds spent on making filters: %s seconds" % (time.time() - startTime))
