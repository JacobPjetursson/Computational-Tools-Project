from random import uniform
from math import sqrt

class KMeans:

    def __init__(self, k, i, d):
        self.k = k
        self.maxIterations = i
        self.d = d
        self.centroids = []
        self.labels = {}

    def calculateCentroids(self, data):
        centroids = []
        for i in range(self.k) :
            center = []
            for j in range(self.d) :
                center.append(uniform(0, 1))
            centroids.append(center)
        n = len(data)
        for i in range(self.maxIterations) :
            labels = {}
            for j in range(n) :
                minRange = 2**31
                label = 0
                for k in range(self.k) :
                    dist = self.calculateDistance(centroids[k],data[j])
                    if dist < minRange :
                        minRange = dist
                        label = k
                if label in labels :
                    labels[label].append(j)
                else :
                    labels[label] = [j]
            newCentroids = self.calculateNewCentroids(labels, data, centroids)
            if newCentroids == centroids :
                break
            else :
                centroids = newCentroids
        self.centroids = centroids
        self.labels = labels


    def calculateDistance(self, center, point):
        dist = 0
        for i in range(self.d) :
            dist += (center[i] - point[i])**2
        return sqrt(dist)

    def calculateNewCentroids(self, labels, data, centroids):
        centroid = []
        for label in range(self.k) :
            center = [0]*self.d
            if not label in labels :
                centroid.append(centroids[label])
                continue
            for i in range(len(labels[label])) :
                for j in range(self.d) :
                    point = (labels[label])[i]
                    center[j] += (data[point])[j]
            size = float(len(labels[label]))
            center = [i/size for i in center]
            centroid.append(center)
        return centroid

