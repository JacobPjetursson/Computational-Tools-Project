# Procedure: Load model and centroids.
# Infer vector on input article (consider faking it by loading in example_wiki wiki)
# Find nearest centroid(s)
# Load in bloom filter corresponding to index of that centroid
# Run filter.classify

import os.path
import sys

import numpy as np
from gensim.corpora.wikicorpus import tokenize
from scipy.spatial.distance import euclidean

import BloomFilter
import load_model

# PREFERENCES
amount_of_centroids = 5
allowed_percent = 0
full_wiki = False
try:
    mode = sys.argv[1]
    if mode == "full":
        full_wiki = True
    elif mode == "simple":
        full_wiki = False
    else:
        raise Exception
except:
    print("Errors in script arguments.\nUsage: 'python check_plagiarism <mode>', where mode=\"simple\" or mode=\"full\"")
    exit(1)


def check_plagiarism(filepath):
    with open(filepath, "r", encoding='utf-8') as f:
        article = f.read()
    article_title = filepath
    print("Testing article: %s" % article_title)
    article_tokens = tokenize(article)

    # Get vector
    vector = model.infer_vector(article_tokens)

    # Get array of distances to each centroid
    distances = []
    for centroid in centroids:
        dist = euclidean(centroid, vector)
        distances.append(dist)

    # Get index for required filter
    filter_indices = np.argsort(distances)[:amount_of_centroids]
    print("Numbers for closest clusters: %s" % filter_indices)

    # Load in filter
    filter_hits = []
    titles = []
    amount = []
    sentences = BloomFilter.prepare_sentences(article)
    for idx in filter_indices:
        fileName = './filters%s/%s.bits' % (suffix, idx)
        bloom_filter = BloomFilter.loadFilter(fileName)

        plagiarism_percent = bloom_filter.classify(sentences)
        filter_hits.append(plagiarism_percent)
        # Get wiki titles for corresponding cluster
        with open("cluster_sample%s.txt" % suffix) as f:
            for i, line in enumerate(f):
                if i == idx:
                    title_amount, samples = line.split(": ", maxsplit=1)
                    titles.append(list(eval(samples)))
                    amount.append(title_amount)
                    break

    plagiarism_detected = False
    for i in range(len(filter_hits)):
        plagiarism_percent = filter_hits[i]
        wiki_titles = titles[i]
        title_amount = amount[i]
        if i == 0:
            if plagiarism_percent > allowed_percent:
                plagiarism_detected = True
                print("Plagiarism detected in closest cluster. %s percent of the text was caught as plagiarism" % plagiarism_percent)
            print("The closest cluster contained %s articles. Below is a sample of size 30:\n%s\n" % (title_amount, wiki_titles[:30]))

        elif plagiarism_percent > allowed_percent:
            plagiarism_detected = True
            if i == 1: nearStr = "2nd"
            elif i == 2: nearStr = "3rd"
            elif i ==3: nearStr = "4th"
            else: nearStr = "5th"
            print("Plagiarism detected in %s nearest cluster. %s percent of the text was caught as plagiarism" %
                  (nearStr, plagiarism_percent))
            print("Cluster contained %s articles. Below is a sample of size 30:\n%s\n" % (title_amount, wiki_titles[:30]))
    if not plagiarism_detected:
        print("No plagiarism detected.")

if full_wiki:
    model_path = "doc2vec.model"
    suffix = "_full"
else:
    model_path = "simple.model"
    suffix = "_simple"

model = load_model.load_model(model_path)
with open("centroids%s.txt" % suffix, "r") as f:
    centroids = [list(eval(line)) for line in f]

while True:
    filepath = input("Enter a file path: ")
    if not os.path.isfile(filepath):
        print("File does not exist, please try again")
    else:
        check_plagiarism(filepath)
