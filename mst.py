import numpy as np
import os
import tempfile
from scipy.spatial.distance import pdist, squareform


def minimum_spanning_tree(X):
    """X are edge weights of fully connected graph"""
    dists = squareform(pdist(X))
    dists_copy = dists.copy()
    n_vertices = dists.shape[0]
    spanning_edges = []

    # initialize with node 0:
    visited_vertices = [0]
    num_visited = 1
    # exclude self connections:
    diag_indices = np.arange(n_vertices)
    dists[diag_indices, diag_indices] = np.inf

    while num_visited != n_vertices:
        new_edge = np.argmin(dists[visited_vertices], axis=None)
        # 2d encoding of new_edge from flat, get correct indices
        new_edge = divmod(new_edge, n_vertices)
        new_edge = [visited_vertices[new_edge[0]], new_edge[1]]
        # add edge to tree
        spanning_edges.append(new_edge)
        visited_vertices.append(new_edge[1])
        # remove all edges inside current tree
        dists[visited_vertices, new_edge[1]] = np.inf
        dists[new_edge[1], visited_vertices] = np.inf
        num_visited += 1
    edges = np.vstack(spanning_edges)
    weights = dists_copy[edges[:, 0], edges[:, 1]]
    return np.hstack([edges, weights[:, np.newaxis]])


def test_mst():
    from scipy.spatial.distance import pdist, squareform
    import matplotlib.pyplot as plt
    P = np.random.uniform(size=(50, 2))

    X = squareform(pdist(P))
    edge_list = minimum_spanning_tree(X)
    plt.scatter(P[:, 0], P[:, 1])

    for edge in edge_list:
        i, j = edge
        plt.plot([P[i, 0], P[j, 0]], [P[i, 1], P[j, 1]], c='r')
    plt.show()


def mst_dual_boruvka(X):
    datafile = tempfile.NamedTemporaryFile(suffix='.txt')
    outfile = tempfile.NamedTemporaryFile(suffix='.csv')
    np.savetxt(datafile.name, X.astype(np.float32))
    os.system("emst "
            "--input_file %s -o %s" % (datafile.name, outfile.name))
    edges = np.loadtxt(outfile.name, delimiter=',')
    return np.atleast_2d(edges)


mst = minimum_spanning_tree
