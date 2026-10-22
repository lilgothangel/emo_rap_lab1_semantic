import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, FOAF, DCTERMS

EX = Namespace("http://example.org/emorap/")

g = Graph()
g.parse("emo_rap_edited.ttl")

node_colors = {
    EX.Label: "#7cc47c",
    EX.Album: "#5a8fe0",
    EX.Producer: "#f0a030",
    EX.Track: "#9ccbf0",
    EX.Artist: "#e05a5a",
    EX.Collective: "#e0e050",
    EX.City: "#b08fd8",
    EX.Genre: "#cccccc",
}

# колір ребра = тип зв'язку (замість підписів на кожному ребрі)
edge_colors = {
    EX.performedBy: "#d62728",
    EX.featuring: "#ff7f0e",
    EX.onAlbum: "#1f77b4",
    EX.producedBy: "#e6a000",
    EX.releasedBy: "#2ca02c",
    EX.bornIn: "#9467bd",
    EX.hasGenre: "#888888",
    FOAF.member: "#bcbd22",
    EX.basedIn: "#8c564b",
}

# колонки: x для кожного типу
columns = {
    EX.Label: 0, EX.Album: 1, EX.Producer: 1, EX.Track: 2,
    EX.Artist: 3, EX.Collective: 4, EX.City: 4, EX.Genre: 4,
}

artist_order = ["LilPeep", "LilTracy", "WiccaPhase", "XXXTentacion", "JuiceWRLD", "TrippieRedd"]


def name(u):
    for p in (FOAF.name, DCTERMS.title, RDFS.label):
        v = g.value(u, p)
        if v:
            return str(v)
    return u.split("/")[-1]


def artist_idx(u):
    return artist_order.index(u.split("/")[-1])


def nodes_of(cls):
    return list(g.subjects(RDF.type, cls))


# сортуємо вузли, щоб ребра менше перетинались
artists = sorted(nodes_of(EX.Artist), key=artist_idx)
albums = sorted(nodes_of(EX.Album), key=lambda a: (artist_idx(g.value(a, DCTERMS.creator)), str(g.value(a, EX.releasedBy))))
tracks = sorted(nodes_of(EX.Track), key=lambda t: albums.index(g.value(t, EX.onAlbum)))
labels = sorted(nodes_of(EX.Label), key=lambda l: min(albums.index(a) for a in g.subjects(EX.releasedBy, l)))
producers = sorted(nodes_of(EX.Producer), key=lambda p: min(tracks.index(t) for t in g.subjects(EX.producedBy, p)))
collectives = nodes_of(EX.Collective)
cities = sorted(nodes_of(EX.City), key=lambda c: min([artist_idx(a) for a in g.subjects(EX.bornIn, c)] or [0]))
genres = nodes_of(EX.Genre)

col_nodes = {
    0: labels,
    1: albums + producers,
    2: tracks,
    3: artists,
    4: collectives + cities + genres,
}

pos = {}
for x, nodes in col_nodes.items():
    n = len(nodes)
    for i, u in enumerate(nodes):
        pos[u] = (x * 3, 1 - i / max(n - 1, 1))  # рівномірно по висоті

G = nx.DiGraph()
for s, p, o in g:
    # creator і жанр альбомів не малюємо - вони дублюють зв'язки через треки
    if p in edge_colors and s in pos and o in pos:
        if p == EX.hasGenre and (s, RDF.type, EX.Album) in g:
            continue
        G.add_edge(s, o, color=edge_colors[p])

plt.figure(figsize=(20, 14))
nx.draw_networkx_edges(
    G, pos, edge_color=[d["color"] for _, _, d in G.edges(data=True)],
    arrows=True, arrowsize=10, width=1.3, alpha=0.8,
    connectionstyle="arc3,rad=0.05", node_size=2500,
)
for u, (x, y) in pos.items():
    cls = g.value(u, RDF.type)
    plt.text(x, y, name(u), ha="center", va="center", fontsize=9,
             bbox=dict(boxstyle="round,pad=0.4", fc=node_colors[cls], ec="black"))

titles = ["Label", "Album / Producer", "Track", "Artist", "Collective / City / Genre"]
for i, t in enumerate(titles):
    plt.text(i * 3, 1.07, t, ha="center", fontsize=13, fontweight="bold")

legend = [Line2D([0], [0], color=c, lw=3, label=p.split("/")[-1].split("#")[-1]) for p, c in edge_colors.items()]
plt.legend(handles=legend, loc="lower center", ncol=9, fontsize=11, bbox_to_anchor=(0.5, -0.06))
plt.title("Emo rap RDF graph", fontsize=18, pad=30)
plt.xlim(-1.5, 13.5)
plt.ylim(-0.08, 1.1)
plt.axis("off")
plt.tight_layout()
plt.savefig("graph.png", dpi=130, bbox_inches="tight")
print("вузлів:", len(pos), "ребер:", G.number_of_edges())
plt.show()