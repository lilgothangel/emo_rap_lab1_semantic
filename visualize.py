import networkx as nx
import matplotlib.pyplot as plt
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, RDFS

EX = Namespace("http://example.org/emorap/")

g = Graph()
g.parse("emo_rap_edited.ttl")

colors = {
    EX.Artist: "#e05a5a",
    EX.Producer: "#f0a030",
    EX.Album: "#5a8fe0",
    EX.Track: "#9ccbf0",
    EX.Label: "#7cc47c",
    EX.City: "#b08fd8",
    EX.Genre: "#cccccc",
    EX.Collective: "#e0e050",
}


def short(u):
    return g.namespace_manager.normalizeUri(u).split(":")[-1]


G = nx.DiGraph()
for s, p, o in g:
    # тільки зв'язки між сутностями, без rdf:type, літералів і схеми
    if not isinstance(o, URIRef) or p in (RDF.type, RDFS.subClassOf, RDFS.domain, RDFS.range, RDFS.subPropertyOf):
        continue
    G.add_edge(short(s), short(o), label=short(p))

node_colors = []
for n in G.nodes:
    t = g.value(EX[n], RDF.type)
    node_colors.append(colors.get(t, "white"))

plt.figure(figsize=(22, 16))
pos = nx.spring_layout(G, k=2.2, seed=42, iterations=500)
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1600, edgecolors="black")
nx.draw_networkx_labels(G, pos, font_size=8)
nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=12, edge_color="gray", node_size=1600)
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, "label"), font_size=6)

for cls, c in colors.items():
    plt.scatter([], [], color=c, label=short(cls), s=150, edgecolors="black")
plt.legend(loc="upper left", fontsize=12)
plt.title("Emo rap RDF graph", fontsize=18)
plt.axis("off")
plt.tight_layout()
plt.savefig("graph.png", dpi=120)
print("вузлів:", G.number_of_nodes(), "ребер:", G.number_of_edges())
plt.show()
