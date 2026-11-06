# Lab 1: Semantic Web Technologies — RDF and SPARQL

An RDF graph for the "emo rap" domain built with Python and RDFLib, queried with SPARQL and linked to Wikidata.

Course: Principles and Methods of Data Linking in Semantic Web Applications, Igor Sikorsky Kyiv Polytechnic Institute.

## What it does

1. Builds an RDF graph from hand-written data: 6 artists, 3 producers, 8 albums, 14 tracks, 5 labels, 5 cities, 2 genres, 2 collectives.
2. Saves the graph as Turtle, RDF/XML and JSON-LD, reads a manually edited Turtle file and saves it as N-Triples.
3. Prints graph triples and all triples connected to one entity (Lil Peep).
4. Runs 7 SPARQL queries (FILTER, ORDER BY, COUNT/AVG/MIN/MAX, OPTIONAL, property paths, a 4-hop path).
5. Links own resources to Wikidata with `owl:sameAs` and queries the merged graph.
6. Shows wrong and corrected examples.
7. Draws the graph and saves it as a PNG.

## Graph model

| Class | Description | Superclass |
| --- | --- | --- |
| `ex:Artist` | a performer | `foaf:Person` |
| `ex:Producer` | a music producer | `foaf:Person` |
| `ex:Collective` | an artist collective | `foaf:Group` |
| `ex:Album` | an album | `schema:MusicAlbum` |
| `ex:Track` | a track | `schema:MusicRecording` |
| `ex:Label` | a record label | `schema:Organization` |
| `ex:City` | a city | `schema:City` |
| `ex:Genre` | a music genre | — |

| Relation | From → to |
| --- | --- |
| `ex:performedBy` | Track → Artist |
| `ex:featuring` | Track → Artist (`rdfs:subPropertyOf ex:performedBy`) |
| `ex:onAlbum` | Track → Album |
| `ex:producedBy` | Track → Producer |
| `ex:releasedBy` | Album → Label |
| `ex:bornIn` | Artist → City |
| `ex:hasGenre` | Artist / Album → Genre |
| `ex:basedIn` | Collective → City |
| `foaf:member` | Collective → Artist |
| `dcterms:creator` | Album → Artist |

Literal properties: `foaf:name`, `dcterms:title`, `rdfs:label`, `schema:birthDate`, `schema:datePublished` (`xsd:date`).

Reused vocabularies: FOAF, Dublin Core (`dcterms`), Schema.org, RDFS, OWL.

Resource URIs look like `http://example.org/emorap/LilPeep`. The `example.org` domain is reserved for examples, so the URIs are identifiers only and do not open in a browser.

## Project structure

| File | Purpose |
| --- | --- |
| `build_graph.py` | builds and serializes the graph (steps 2, 3) |
| `graph_ops.py` | reads the edited Turtle file, prints triples (step 3) |
| `queries.py` | SPARQL queries to the local graph (step 4) |
| `wikidata_link.py` | `owl:sameAs` links and Wikidata data (step 5) |
| `error_example.py` | wrong and corrected examples |
| `visualize.py` | graph drawing with NetworkX and Matplotlib |

## Requirements

- Python 3.10+
- packages from `requirements.txt`: `rdflib`, `SPARQLWrapper`, `networkx`, `matplotlib`
- internet connection for `wikidata_link.py`

## Run

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux / macOS
pip install -r requirements.txt

python build_graph.py
python graph_ops.py
python visualize.py
python queries.py
python wikidata_link.py
python error_example.py
```

`visualize.py` opens a Matplotlib window with the graph. Close it to let the program finish.

## Output

| File | Content |
| --- | --- |
| `emo_rap.ttl` | the graph in Turtle (186 triples) |
| `emo_rap.rdf` | the graph in RDF/XML |
| `emo_rap.jsonld` | the graph in JSON-LD |
| `emo_rap_edited.ttl` | the graph after manual edits: added tracks Wishing Well and Righteous (194 triples) |
| `emo_rap_edited.nt` | the edited graph in N-Triples |
| `emo_rap_linked.ttl` | the graph with `owl:sameAs` links to Wikidata |
| `graph.png` | visualization of the graph |
| `output/*.txt` | console output of the scripts |

## SPARQL queries

| # | Question | Demonstrates |
| --- | --- | --- |
| 1 | Which tracks did Juice WRLD perform and on which albums? | relations between types, property path |
| 2 | Which albums were released in 2018 or later? | FILTER by date, ORDER BY |
| 3 | Which artist has the most tracks? | COUNT, GROUP BY, ORDER BY DESC |
| 4 | On which labels were tracks by GothBoiClique members released? | 4-hop path |
| 5 | Which artists were born after 1997 and where? | FILTER with YEAR() |
| 6 | Release statistics per label | COUNT, AVG, MIN, MAX |
| 7 | Who recorded tracks together and who produced them? | OPTIONAL |

## Wikidata links

| Own resource | Wikidata |
| --- | --- |
| `ex:LilPeep` | `wd:Q29388200` |
| `ex:XXXTentacion` | `wd:Q28561969` |
| `ex:JuiceWRLD` | `wd:Q52151598` |
| `ex:TrippieRedd` | `wd:Q40890697` |
| `ex:GothBoiClique` | `wd:Q78248638` |
| `ex:CWWYS1` | `wd:Q39048820` |
| `ex:Album17` | `wd:Q37800287` |

`owl:sameAs` is used because both URIs identify the same real-world entity. The IDs were found by searching Wikidata by `rdfs:label` and checked against the `owl:sameAs` links in DBpedia.

From Wikidata the script fetches the birth name (`wdt:P1477`), place of birth (`wdt:P19`) and start of career (`wdt:P2031`), then runs a query over the merged graph.

## Wrong and corrected examples

1. Turtle with a missing dot at the end of a triple → `BadSyntax`, fixed by adding `.`.
2. SPARQL with the direction of `ex:performedBy` reversed → 0 results, fixed by swapping subject and object.
3. Typo in a prefix (`fooaf:`) → `Unknown namespace prefix`, fixed.

## AI usage
Claude was used to search for and select data.