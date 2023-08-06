import numpy as np

from pixel_clusterizer import clusterizer

hits = np.ones(shape=(3, ), dtype=clusterizer.hit_data_type)  # Create some data with std. hit data type

cr = clusterizer.HitClusterizer()  # Initialize clusterizer

hits_clustered, cluster = cr.cluster_hits(hits)  # Cluster hits  # add hits to clusterizer

print (cluster)  # Print cluster

print (hits_clustered)  # Print hits + cluster info