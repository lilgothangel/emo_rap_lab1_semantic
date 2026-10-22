from rdflib import Graph, Namespace
from rdflib.namespace import RDF, DCTERMS

EX = Namespace("http://example.org/emorap/")

g = Graph()
g.parse("emo_rap.ttl", format="turtle")
print("оригінальний граф:", len(g), "трійок")

# файл emo_rap_edited.ttl відредагований руками (додано 2 треки Juice WRLD)
g2 = Graph()
g2.parse("emo_rap_edited.ttl", format="turtle")
print("після ручних змін:", len(g2), "трійок")
print("нові трійки:")
for s, p, o in g2 - g:
    print(" ", s.n3(g2.namespace_manager), p.n3(g2.namespace_manager), o.n3(g2.namespace_manager))

g2.serialize("emo_rap_edited.nt", format="nt", encoding="utf-8")


def short(x):
    return x.n3(g2.namespace_manager)


print("\n--- всі треки (вибрані трійки) ---")
for t in g2.subjects(RDF.type, EX.Track):
    print(short(t), "->", g2.value(t, DCTERMS.title))

print("\n--- всі трійки графу ---")
for s, p, o in sorted(g2):
    print(short(s), short(p), short(o))

# трійки, де Lil Peep суб'єкт або об'єкт
print("\n--- Lil Peep як суб'єкт ---")
for p, o in g2.predicate_objects(EX.LilPeep):
    print(short(p), short(o))

print("\n--- Lil Peep як об'єкт ---")
for s, p in g2.subject_predicates(EX.LilPeep):
    print(short(s), short(p))
