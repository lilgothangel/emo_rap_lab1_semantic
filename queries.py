from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, FOAF, XSD, DCTERMS

EX = Namespace("http://example.org/emorap/")
SCHEMA = Namespace("https://schema.org/")

graph = Graph()
graph.parse("emo_rap_edited.ttl")

ns = {"ex": EX, "schema": SCHEMA, "foaf": FOAF, "dcterms": DCTERMS, "rdfs": RDFS, "xsd": XSD}


def run(title, q):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
    res = graph.query(q, initNs=ns)
    print(" | ".join(str(v) for v in res.vars))
    for row in res:
        print(" | ".join(str(x) for x in row))


# 1. Які треки виконав Juice WRLD і на яких альбомах?
q1 = """
    SELECT ?track ?album
    WHERE {
        ?a foaf:name "Juice WRLD" .
        ?t ex:performedBy ?a ;
           dcterms:title ?track ;
           ex:onAlbum/dcterms:title ?album .
    }
    ORDER BY ?album ?track
"""
run("1. Треки Juice WRLD", q1)

# 2. Які альбоми вийшли після 2018 року? (FILTER + ORDER BY)
q2 = """
    SELECT ?title ?artist ?date
    WHERE {
        ?al a ex:Album ;
            dcterms:title ?title ;
            dcterms:creator/foaf:name ?artist ;
            schema:datePublished ?date .
        FILTER (?date >= "2018-01-01"^^xsd:date)
    }
    ORDER BY ?date
"""
run("2. Альбоми з 2018 року", q2)

# 3. У кого з артистів найбільше треків у графі? (COUNT, фіти теж рахуються)
q3 = """
    SELECT ?name (COUNT(DISTINCT ?t) AS ?tracks)
    WHERE {
        ?t ex:performedBy|ex:featuring ?a .
        ?a foaf:name ?name .
    }
    GROUP BY ?name
    ORDER BY DESC(?tracks)
"""
run("3. Кількість треків у кожного артиста", q3)

# 4. На яких лейблах виходили треки учасників GothBoiClique?
# колектив -> учасник -> трек -> альбом -> лейбл (4 зв'язки)
q4 = """
    SELECT DISTINCT ?member ?track ?album ?label
    WHERE {
        ?c foaf:name "GothBoiClique" ;
           foaf:member ?m .
        ?m foaf:name ?member .
        ?t ex:performedBy|ex:featuring ?m ;
           dcterms:title ?track ;
           ex:onAlbum ?al .
        ?al dcterms:title ?album ;
            ex:releasedBy/rdfs:label ?label .
    }
    ORDER BY ?member ?track
"""
run("4. Лейбли треків учасників GothBoiClique", q4)

# 5. Хто з артистів народився після 1997 року і де?
q5 = """
    SELECT ?name ?bd ?city
    WHERE {
        ?a a ex:Artist ;
           foaf:name ?name ;
           schema:birthDate ?bd ;
           ex:bornIn/rdfs:label ?city .
        FILTER (YEAR(?bd) > 1997)
    }
    ORDER BY DESC(?bd)
"""
run("5. Артисти, народжені після 1997", q5)

# 6. Середній, перший і останній рік релізів по лейблах
q6 = """
    SELECT ?label (COUNT(?al) AS ?albums) (AVG(YEAR(?d)) AS ?avgYear)
           (MIN(?d) AS ?first) (MAX(?d) AS ?last)
    WHERE {
        ?al ex:releasedBy/rdfs:label ?label ;
            schema:datePublished ?d .
    }
    GROUP BY ?label
    ORDER BY DESC(?albums)
"""
run("6. Статистика по лейблах", q6)

# 7. Хто з ким записував фіти і хто продюсував трек
q7 = """
    SELECT ?main ?feat ?track ?producer
    WHERE {
        ?t ex:performedBy/foaf:name ?main ;
           ex:featuring/foaf:name ?feat ;
           dcterms:title ?track .
        OPTIONAL { ?t ex:producedBy/foaf:name ?producer . }
    }
"""
run("7. Спільні треки", q7)
