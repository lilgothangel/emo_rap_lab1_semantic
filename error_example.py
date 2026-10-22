from rdflib import Graph, Namespace
from rdflib.namespace import FOAF, DCTERMS

EX = Namespace("http://example.org/emorap/")

# ---- помилка 1: синтаксис Turtle ----
bad_ttl = """
@prefix ex: <http://example.org/emorap/> .
@prefix dcterms: <http://purl.org/dc/terms/> .

ex:LucidDreams a ex:Track ;
    dcterms:title "Lucid Dreams" ;
    ex:performedBy ex:JuiceWRLD
ex:Robbery a ex:Track .
"""
# забули крапку після ex:JuiceWRLD

good_ttl = bad_ttl.replace("ex:performedBy ex:JuiceWRLD\n", "ex:performedBy ex:JuiceWRLD .\n")

g = Graph()
try:
    g.parse(data=bad_ttl, format="turtle")
except Exception as e:
    print("ПОМИЛКА 1:", type(e).__name__, "-", str(e).splitlines()[0])

g = Graph()
g.parse(data=good_ttl, format="turtle")
print("виправлено, трійок:", len(g))

# ---- помилка 2: неправильний напрямок зв'язку в SPARQL ----
graph = Graph()
graph.parse("emo_rap_edited.ttl")
ns = {"ex": EX, "foaf": FOAF, "dcterms": DCTERMS}

# хочемо треки Lil Peep, але переплутали суб'єкт і об'єкт у ex:performedBy
bad_q = """
    SELECT ?title WHERE {
        ?a foaf:name "Lil Peep" .
        ?a ex:performedBy ?t .
        ?t dcterms:title ?title .
    }
"""
res = list(graph.query(bad_q, initNs=ns))
print("\nПОМИЛКА 2: результатів:", len(res), "(трек -> артист, а не навпаки)")

good_q = """
    SELECT ?title WHERE {
        ?a foaf:name "Lil Peep" .
        ?t ex:performedBy ?a .
        ?t dcterms:title ?title .
    }
"""
res = list(graph.query(good_q, initNs=ns))
print("виправлено, результатів:", len(res))
for r in res:
    print(" ", r.title)

# ---- помилка 3: опечатка в префіксі (fooaf не оголошений) ----
try:
    graph.query("SELECT ?n WHERE { ?a fooaf:name ?n }")
except Exception as e:
    print("\nПОМИЛКА 3:", type(e).__name__, "-", str(e)[:80])

res = graph.query("""
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    SELECT (COUNT(?n) AS ?cnt) WHERE { ?a foaf:name ?n }
""")
print("виправлено, імен у графі:", list(res)[0][0])
