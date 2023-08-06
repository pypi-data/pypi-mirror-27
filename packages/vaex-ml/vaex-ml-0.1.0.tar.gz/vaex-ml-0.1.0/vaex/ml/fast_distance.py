import numpy as np

#pythran export distances(float64 [][][], float64 [][], float64 [][][], float64 [], float64 [][])
def distances(centroids, counts, sumpos, inertia, done, blocks):
    N = blocks[0].shape[0]
    runs = sumpos.shape[0]
    clusters = sumpos.shape[1]
    dimensions = sumpos.shape[2]
    for j in range(N):
        for run in range(runs):
                best_distance = 1e100
                best_class = 10000
                for cluster in range(clusters):
                    distance = 0
                    for d in range(dimensions):
                        distance += (centroids[run,cluster,d] - blocks[d,j])**2
                    if distance < best_distance:
                        best_class = cluster
                        best_distance = distance
                cls = best_class #classes[j]
                inertia[run] += best_distance
                for d in range(dimensions):
                     sumpos[run,cls,d] += blocks[d,j]
                counts[run,cls] += 1
