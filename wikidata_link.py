from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import OWL, FOAF, RDFS, DCTERMS
from SPARQLWrapper import SPARQLWrapper, JSON, TURTLE

EX = Namespace("http://example.org/emorap/")
WD = Namespace("http://www.wikidata.org/entity/")
WDT = Namespace("http://www.wikidata.org/prop/direct/")

AGENT = "kpi-semantic-web-lab/1.0 (student lab)"
sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent=AGENT)

# 1. шукаємо артистів у Wikidata за англійською назвою (Q5 = людина)
find_query = """
    SELECT ?item ?name ?desc
    WHERE {
        VALUES ?name { "Lil Peep"@en "XXXTentacion"@en "Juice WRLD"@en "Trippie Redd"@en }
        ?item rdfs:label ?name ;
              wdt:P31 wd:Q5 .
        OPTIONAL { ?item schema:description ?desc . FILTER(LANG(?desc) = "en") }
    }
"""
sparql.setQuery(find_query)
sparql.setReturnFormat(JSON)
res = sparql.query().convert()

print("--- знайдено у Wikidata ---")
for b in res["results"]["bindings"]:
    print(b["name"]["value"], "|", b["item"]["value"], "|", b.get("desc", {}).get("value", ""))

# 2. зв'язуємо свої ресурси з Wikidata через owl:sameAs
# (Q-id перевірені також через DBpedia, там є такі ж owl:sameAs)
links = {
    EX.LilPeep: WD.Q29388200,
    EX.XXXTentacion: WD.Q28561969,
    EX.JuiceWRLD: WD.Q52151598,
    EX.TrippieRedd: WD.Q40890697,
    EX.GothBoiClique: WD.Q78248638,
    EX.CWWYS1: WD.Q39048820,
    EX.Album17: WD.Q37800287,
}

g = Graph()
g.parse("emo_rap_edited.ttl")
g.bind("owl", OWL)
g.bind("wd", WD)
g.bind("wdt", WDT)

for ours, wd in links.items():
    g.add((ours, OWL.sameAs, wd))
    print(ours, "owl:sameAs", wd)

# 3. тягнемо з Wikidata справжнє ім'я, місце народження і рік початку кар'єри
values = " ".join(f"wd:{u.split('/')[-1]}" for u in links.values())
construct_query = f"""
    CONSTRUCT {{
        ?p wdt:P1477 ?birthName .
        ?p wdt:P19 ?place .
        ?place rdfs:label ?placeName .
        ?p wdt:P2031 ?start .
    }}
    WHERE {{
        VALUES ?p {{ {values} }}
        ?p wdt:P31 wd:Q5 .
        OPTIONAL {{ ?p wdt:P1477 ?birthName . }}
        OPTIONAL {{
            ?p wdt:P19 ?place .
            ?place rdfs:label ?placeName .
            FILTER(LANG(?placeName) = "en")
        }}
        OPTIONAL {{ ?p wdt:P2031 ?start . }}
    }}
"""
sparql.setQuery(construct_query)
sparql.setReturnFormat(TURTLE)
data = sparql.query().convert()

wd_graph = Graph()
wd_graph.parse(data=data.decode("utf-8") if isinstance(data, bytes) else data, format="turtle")
print("\nтрійок з Wikidata:", len(wd_graph))
wd_graph.serialize("wikidata_part.ttl", format="turtle")

g += wd_graph
g.serialize("emo_rap_linked.ttl", format="turtle")
print("всього трійок після об'єднання:", len(g))

# 4. запит по власному + зовнішньому графу
q = """
    SELECT ?name ?ourCity ?birthName ?wdCity ?start
    WHERE {
        ?a a ex:Artist ;
           foaf:name ?name ;
           owl:sameAs ?wd .
        OPTIONAL { ?a ex:bornIn/rdfs:label ?ourCity . }
        OPTIONAL { ?wd wdt:P1477 ?birthName . }
        OPTIONAL { ?wd wdt:P19/rdfs:label ?wdCity . }
        OPTIONAL { ?wd wdt:P2031 ?start . }
    }
    ORDER BY ?name
"""
print("\nname | наше місто | справжнє ім'я (Wikidata) | місце народження (Wikidata) | початок кар'єри")
for row in g.query(q, initNs={"ex": EX, "foaf": FOAF, "owl": OWL, "wdt": WDT, "rdfs": RDFS}):
    print(" | ".join(str(x) for x in row))

# альбоми: наш лейбл + назва з Wikidata
q2 = """
    SELECT ?title ?label ?wd
    WHERE {
        ?al a ex:Album ;
            dcterms:title ?title ;
            ex:releasedBy/rdfs:label ?label ;
            owl:sameAs ?wd .
    }
"""
print("\nальбоми з посиланням на Wikidata:")
for row in g.query(q2, initNs={"ex": EX, "owl": OWL, "rdfs": RDFS, "dcterms": DCTERMS}):
    print(" | ".join(str(x) for x in row))
