import timeit
import networkx
import matplotlib.pyplot as plt
from operator import itemgetter

# Graphs ####################################################
# A number of graphs, defined using dictionaries, to be used for testing
#############################################################

# graph351 from pg 1109 of (Cormen)
# optimal cover: {b,d,e}
graph351 = {'A': ['B'], 
            'B': ['C', 'A'], 
            'C': ['B','D', 'E'],
            'D': ['C', 'E', 'F', 'G'],
            'E': ['C', 'D', 'F'], 
            'F': ['D', 'E'],
            'G': ['D']}

graphConnected = {'A': ['B', 'C', 'D', 'E', 'F', 'G'],
                  'B': ['A', 'C', 'D', 'E', 'F', 'G'],
                  'C': ['A', 'B', 'D', 'E', 'F', 'G'],
                  'D': ['A', 'C', 'B', 'E', 'F', 'G'],
                  'E': ['A', 'C', 'D', 'B', 'F', 'G'],
                  'F': ['A', 'C', 'D', 'E', 'B', 'G'],
                  'G': ['A', 'C', 'D', 'E', 'F', 'B']}

graphBipartite = {'A': ['F', 'G'],
                  'B': ['F'],
                  'C': ['H', 'G'],
                  'D': ['H', 'J'],
                  'E': ['I', 'J'],
                  'F': ['A', 'B'],
                  'G': ['A', 'C'],
                  'H': ['C', 'D'],
                  'I': ['E'],
                  'J': ['D', 'E']}

graphBig = {'A': ['B', 'E', 'D'],
            'B': ['A', 'E', 'F', 'C'],
            'C': ['B', 'F'],
            'D': ['A', 'E', 'H', 'G'],
            'G': ['D', 'H', 'K', 'J'],
            'J': ['G', 'K', 'N', 'M'],
            'M': ['J', 'N', 'Q', 'P'],
            'P': ['M', 'Q', 'T', 'S'],
            'F': ['E', 'B', 'C', 'I'],
            'I': ['H', 'E', 'F', 'L'],
            'L': ['K', 'H', 'I', 'O'],
            'O': ['N', 'K', 'L', 'R'],
            'R': ['Q', 'N', 'O', 'U'],
            'E': ['D', 'A', 'B', 'F', 'I', 'H'],
            'H': ['G', 'D', 'E', 'I', 'L', 'K'],
            'K': ['J', 'G', 'H', 'L', 'O', 'N'],
            'N': ['M', 'J', 'K', 'O', 'R', 'Q'],
            'Q': ['P', 'M', 'N', 'R', 'U', 'T'],
            'T': ['S', 'P', 'Q', 'U'],
            'S': ['P', 'T'],
            'U': ['T', 'Q', 'R']}


# Functions #################################################

def vertex_cover_degrees(graph, res):
    edges = generate_edges(graph)
    degrees = count_degrees(edges, list(dict(graph).keys()))
    degrees_sorted = sorted(degrees.items(), key=itemgetter(1), reverse=True)
    cover_ = []
    for v in degrees_sorted:
        cover_.append(v[0])
        if verify_vertex_cover(cover_, edges):
            res.append(cover_)
            return

# vertex_cover_brute checks all possible sets of vertices of size k for a valid cover
def vertex_cover_brute(graph, res):
    vertices = list(dict(graph).keys())
    k = len(vertices)
    # generate all edges present in graph
    edges = generate_edges(graph)
    for i in range(1, k):
        # generate all subset of size i from set vertices
        subsets_ = gen_subsets(vertices, i)
        for s in subsets_:
            # check if subset s is a cover for graph
            if verify_vertex_cover(s, edges) == True:
                # since subsets are generated in  increasing size, the first
                # subset that is cover can be returned as the minimal one
                res.append(s)
                return
    # no cover was found so return set of all edges as minimal cover
    #res.append(vertices)

# vertex_cover_approx
# Generates an approximately optimal vertex cover for a given graph using the APPROX-VERTEX-COVER algorithm
# found in (Cormen)
def vertex_cover_approx(graph, size_, res):
    # generate all edges present in graph
    edges = generate_edges(graph)
    s = 0
    cover_ = []
    for edge in edges:
        if edge[0] not in cover_ and edge[1] not in cover_:
            cover_.append(edge[0])
            cover_.append(edge[1])
            s += 2
    size_.append(s)
    res.append(cover_)


# gen_subsets(set,k)
# Generates all subsets of size k for the set given
# The subsets are generated in increasing size
def gen_subsets(set_, k):
    curr_subset = []
    res = []
    generate_subsets(set_, curr_subset, res, k, 0)
    return res

def generate_subsets(set_, curr_subset, subsets_, k, next_index):
    if len(curr_subset) == int(k):
        subsets_.append(curr_subset)
        return
    if next_index + 1 <= len(set_):
        curr_subset_exclude = curr_subset.copy()
        curr_subset.append(set_[next_index])
        generate_subsets(set_, curr_subset, subsets_, k, next_index+1)
        generate_subsets(set_, curr_subset_exclude, subsets_, k, next_index+1)


# verifies that cover is indeed a vertex cover
# does not check if cover only has vertices from graph
def verify_vertex_cover(cover, edges):
    # check that atleast one vertice from each edge appears in cover
    for edge in edges:
        in_cover = False;
        for vertex in cover:
            if edge[0] == vertex or edge[1] == vertex: 
                    in_cover = True;
        # stop processing as soon as one edge found not in cover
        if in_cover == False:
            return False
    # return true if all edges have atleast one endpoint in cover
    return True


def generate_edges(graph):
    edges = []
    for node in graph: 
        for neighbour in graph[node]:
            if (node,neighbour) and (neighbour, node) not in edges:
                edges.append((node,neighbour))
    return edges


def count_degrees(edges, vertices):
    degrees = {}
    for v in vertices:
        degrees[v] = 0
    for edge in edges:
        degrees[edge[0]] = degrees[edge[0]] + 1
        degrees[edge[1]] = degrees[edge[1]] + 1
    return degrees


def plot_graph(graph, name):
    g = networkx.Graph()
    for k, vs in dict(graph).items():
        for v in vs:
            g.add_edge(k, v)
    networkx.draw_networkx(g, pos=networkx.circular_layout(g))
    plt.show()


# Experiments ####################################################

col_labels = ['Graph', 'Algorithm', 'Running Time (ms)', 'Approximation Ratio', 'Cover']
table_data = []
graph351_data_b = ['Graph351', 'Brute Force']
graph351_data_a = ['Graph351', 'Approximation']
graph351_data_d = ['Graph351', 'Degree Heuristic']
graphBig_data_b = ['GraphBig', 'Brute Force']
graphBig_data_a = ['GraphBig', 'Approximation']
graphBig_data_d = ['GraphBig', 'Degree Heuristic']
graphBipartite_data_b = ['GraphBipartite', 'Brute Force']
graphBipartite_data_a = ['GraphBipartite', 'Approximation']
graphBipartite_data_d = ['GraphBipartite', 'Degree Heuristic']
graphConnected_data_b = ['GraphConnected', 'Brute Force']
graphConnected_data_a = ['GraphConnected', 'Approximation']
graphConnected_data_d = ['GraphConnected', 'Degree Heuristic']

cover = []
time = timeit.timeit('vertex_cover_brute(graph351, cover)', number=1, globals=globals())
graph351_data_b.append("{0:.3f}".format(time*1000))
graph351_data_b.append(1.0)
graph351_data_b.append(cover[0])

coverConnected = []
time = timeit.timeit('vertex_cover_brute(graphConnected, coverConnected)', number=1, globals=globals())
graphConnected_data_b.append("{0:.3f}".format(time*1000))
graphConnected_data_b.append(1.0)
graphConnected_data_b.append(coverConnected[0])

coverBipartite = []
time = timeit.timeit('vertex_cover_brute(graphBipartite, coverBipartite)', number=1, globals=globals())
graphBipartite_data_b.append("{0:.3f}".format(time*1000))
graphBipartite_data_b.append(1.0)
graphBipartite_data_b.append(coverBipartite[0])

coverBig = []
time = timeit.timeit('vertex_cover_brute(graphBig, coverBig)', number=1, globals=globals())
graphBig_data_b.append("{0:.3f}".format(time*1000))
graphBig_data_b.append(1.0)
graphBig_data_b.append(coverBig[0])

time = 0.0
size = []
cover_approx = []
time = timeit.timeit('vertex_cover_approx(graph351, size, cover_approx)', number=1, globals=globals())
ratio = size[0]/3
graph351_data_a.append("{0:.3f}".format(time*1000))
graph351_data_a.append("{0:.3f}".format(ratio))
graph351_data_a.append(cover_approx[0])

time = 0.0
size = []
cover_approx = []
time = timeit.timeit('vertex_cover_approx(graphBipartite, size, cover_approx)', number=1, globals=globals())
ratio = size[0]/5
graphBipartite_data_a.append("{0:.3f}".format(time*1000))
graphBipartite_data_a.append("{0:.3f}".format(ratio))
graphBipartite_data_a.append(cover_approx[0])

time = 0.0
size = []
cover_approx = []
time = timeit.timeit('vertex_cover_approx(graphConnected, size, cover_approx)', number=1, globals=globals())
ratio = size[0]/6
graphConnected_data_a.append("{0:.3f}".format(time*1000))
graphConnected_data_a.append("{0:.3f}".format(ratio))
graphConnected_data_a.append(cover_approx[0])


time = 0.0
size = []
cover_approx = []
time = timeit.timeit('vertex_cover_approx(graphBig, size, cover_approx)', number=1, globals=globals())
ratio = size[0]/13
graphBig_data_a.append("{0:.3f}".format(time*1000))
graphBig_data_a.append("{0:.3f}".format(ratio))
graphBig_data_a.append(cover_approx[0])

cover_degree = []
time = timeit.timeit('vertex_cover_degrees(graph351, cover_degree)', number=1, globals=globals())
ratio = len(cover_degree[0])/3
graph351_data_d.append("{0:.3f}".format(time*1000))
graph351_data_d.append("{0:.3f}".format(ratio))
graph351_data_d.append(cover_degree[0])

cover_degree = []
time = timeit.timeit('vertex_cover_degrees(graphConnected, cover_degree)', number=1, globals=globals())
ratio = len(cover_degree[0])/6
graphConnected_data_d.append("{0:.3f}".format(time*1000))
graphConnected_data_d.append("{0:.3f}".format(ratio))
graphConnected_data_d.append(cover_degree[0])

cover_degree = []
time = timeit.timeit('vertex_cover_degrees(graphBipartite, cover_degree)', number=1, globals=globals())
ratio = len(cover_degree[0])/5
graphBipartite_data_d.append("{0:.3f}".format(time*1000))
graphBipartite_data_d.append("{0:.3f}".format(ratio))
graphBipartite_data_d.append(cover_degree[0])

cover_degree = []
time = timeit.timeit('vertex_cover_degrees(graphBig, cover_degree)', number=1, globals=globals())
ratio = len(cover_degree[0])/13
graphBig_data_d.append("{0:.3f}".format(time*1000))
graphBig_data_d.append("{0:.3f}".format(ratio))
graphBig_data_d.append(cover_degree[0])

table_data.append(graph351_data_b)
table_data.append(graph351_data_a)
table_data.append(graph351_data_d)
table_data.append(graphConnected_data_b)
table_data.append(graphConnected_data_a)
table_data.append(graphConnected_data_d)
table_data.append(graphBipartite_data_b)
table_data.append(graphBipartite_data_a)
table_data.append(graphBipartite_data_d)
table_data.append(graphBig_data_b)
table_data.append(graphBig_data_a)
table_data.append(graphBig_data_d)

fig = plt.figure(dpi=160)
ax = fig.add_subplot(111)
ax.set_title("Results")

table = ax.table(cellText=table_data,
                  colLabels=col_labels,
                  loc='center')
table.auto_set_font_size(False)
table.set_fontsize(8)
table.auto_set_column_width([0,1,2,3,4])
ax.axis('off')
plt.show()

'''
plot_graph(graph351, "plots/Graph351")
plot_graph(graphConnected, "plots/GraphConnected")
plot_graph(graphBipartite, "plots/GraphBipartite")
plot_graph(graphBig, "plots/GraphBig")
'''
