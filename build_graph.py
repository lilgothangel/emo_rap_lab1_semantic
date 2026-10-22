from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, FOAF, XSD, DCTERMS

EX = Namespace("http://example.org/emorap/")
SCHEMA = Namespace("https://schema.org/")

g = Graph()
g.bind("ex", EX)
g.bind("foaf", FOAF)
g.bind("schema", SCHEMA)
g.bind("dcterms", DCTERMS)

# класи
g.add((EX.Artist, RDFS.subClassOf, FOAF.Person))
g.add((EX.Producer, RDFS.subClassOf, FOAF.Person))
g.add((EX.Collective, RDFS.subClassOf, FOAF.Group))
g.add((EX.Album, RDFS.subClassOf, SCHEMA.MusicAlbum))
g.add((EX.Track, RDFS.subClassOf, SCHEMA.MusicRecording))
g.add((EX.Label, RDFS.subClassOf, SCHEMA.Organization))
g.add((EX.City, RDFS.subClassOf, SCHEMA.City))
g.add((EX.Genre, RDF.type, RDFS.Class))

# властивості
g.add((EX.performedBy, RDFS.domain, EX.Track))
g.add((EX.performedBy, RDFS.range, EX.Artist))
g.add((EX.featuring, RDFS.subPropertyOf, EX.performedBy))
g.add((EX.onAlbum, RDFS.domain, EX.Track))
g.add((EX.onAlbum, RDFS.range, EX.Album))
g.add((EX.producedBy, RDFS.range, EX.Producer))
g.add((EX.releasedBy, RDFS.range, EX.Label))
g.add((EX.bornIn, RDFS.range, EX.City))


def add_named(uri, cls, name):
    g.add((uri, RDF.type, cls))
    g.add((uri, RDFS.label, Literal(name)))


cities = {
    "Allentown": "Allentown",
    "Plantation": "Plantation",
    "Chicago": "Chicago",
    "Canton": "Canton",
    "LosAngeles": "Los Angeles",
}
for key, name in cities.items():
    add_named(EX[key], EX.City, name)

for key, name in {"EmoRap": "Emo rap", "CloudRap": "Cloud rap"}.items():
    add_named(EX[key], EX.Genre, name)

labels = {
    "AWAL": "AWAL",
    "Columbia": "Columbia Records",
    "Empire": "Empire Distribution",
    "Interscope": "Interscope Records",
    "TenThousand": "TenThousand Projects",
}
for key, name in labels.items():
    add_named(EX[key], EX.Label, name)

# key: (ім'я, дата народження, місто, жанри)
artists = {
    "LilPeep": ("Lil Peep", "1996-11-01", "Allentown", ["EmoRap", "CloudRap"]),
    "XXXTentacion": ("XXXTentacion", "1998-01-23", "Plantation", ["EmoRap"]),
    "JuiceWRLD": ("Juice WRLD", "1998-12-02", "Chicago", ["EmoRap"]),
    "TrippieRedd": ("Trippie Redd", "1999-06-18", "Canton", ["EmoRap"]),
    "LilTracy": ("Lil Tracy", None, None, ["CloudRap"]),
    "WiccaPhase": ("Wicca Phase Springs Eternal", None, None, ["CloudRap"]),
}
for key, (name, bd, city, genres) in artists.items():
    a = EX[key]
    g.add((a, RDF.type, EX.Artist))
    g.add((a, FOAF.name, Literal(name)))
    if bd:
        g.add((a, SCHEMA.birthDate, Literal(bd, datatype=XSD.date)))
    if city:
        g.add((a, EX.bornIn, EX[city]))
    for gen in genres:
        g.add((a, EX.hasGenre, EX[gen]))

for key, name in {"NickMira": "Nick Mira", "Potsu": "Potsu", "Smokeasac": "Smokeasac"}.items():
    g.add((EX[key], RDF.type, EX.Producer))
    g.add((EX[key], FOAF.name, Literal(name)))

g.add((EX.GothBoiClique, RDF.type, EX.Collective))
g.add((EX.GothBoiClique, FOAF.name, Literal("GothBoiClique")))
g.add((EX.GothBoiClique, EX.basedIn, EX.LosAngeles))
for m in ["LilPeep", "LilTracy", "WiccaPhase"]:
    g.add((EX.GothBoiClique, FOAF.member, EX[m]))

g.add((EX.MembersOnly, RDF.type, EX.Collective))
g.add((EX.MembersOnly, FOAF.name, Literal("Members Only")))
g.add((EX.MembersOnly, FOAF.member, EX.XXXTentacion))

# key: (назва, артист, дата виходу, лейбл)
albums = {
    "CWWYS1": ("Come Over When You're Sober, Pt. 1", "LilPeep", "2017-08-15", "AWAL"),
    "CWWYS2": ("Come Over When You're Sober, Pt. 2", "LilPeep", "2018-11-09", "Columbia"),
    "Album17": ("17", "XXXTentacion", "2017-08-25", "Empire"),
    "AlbumQuestion": ("?", "XXXTentacion", "2018-03-16", "Empire"),
    "GoodbyeGoodRiddance": ("Goodbye & Good Riddance", "JuiceWRLD", "2018-05-23", "Interscope"),
    "DeathRaceForLove": ("Death Race for Love", "JuiceWRLD", "2019-03-08", "Interscope"),
    "LegendsNeverDie": ("Legends Never Die", "JuiceWRLD", "2020-07-10", "Interscope"),
    "LifesATrip": ("Life's a Trip", "TrippieRedd", "2018-08-10", "TenThousand"),
}
for key, (title, artist, date, label) in albums.items():
    al = EX[key]
    g.add((al, RDF.type, EX.Album))
    g.add((al, DCTERMS.title, Literal(title)))
    g.add((al, DCTERMS.creator, EX[artist]))
    g.add((al, SCHEMA.datePublished, Literal(date, datatype=XSD.date)))
    g.add((al, EX.releasedBy, EX[label]))
    g.add((al, EX.hasGenre, EX.EmoRap))

# key: (назва, артист, альбом, продюсер, фіт)
tracks = {
    "AwfulThings": ("Awful Things", "LilPeep", "CWWYS1", "Smokeasac", "LilTracy"),
    "SaveThatShit": ("Save That Shit", "LilPeep", "CWWYS1", "Smokeasac", None),
    "BenzTruck": ("Benz Truck", "LilPeep", "CWWYS1", None, None),
    "FallingDown": ("Falling Down", "LilPeep", "CWWYS2", None, "XXXTentacion"),
    "JocelynFlores": ("Jocelyn Flores", "XXXTentacion", "Album17", "Potsu", None),
    "Revenge": ("Revenge", "XXXTentacion", "Album17", None, None),
    "SAD": ("SAD!", "XXXTentacion", "AlbumQuestion", None, None),
    "Changes": ("Changes", "XXXTentacion", "AlbumQuestion", None, None),
    "LucidDreams": ("Lucid Dreams", "JuiceWRLD", "GoodbyeGoodRiddance", "NickMira", None),
    "AllGirls": ("All Girls Are the Same", "JuiceWRLD", "GoodbyeGoodRiddance", "NickMira", None),
    "Robbery": ("Robbery", "JuiceWRLD", "DeathRaceForLove", "NickMira", None),
    "TakingAWalk": ("Taking a Walk", "TrippieRedd", "LifesATrip", None, None),
}
for key, (title, artist, album, prod, feat) in tracks.items():
    t = EX[key]
    g.add((t, RDF.type, EX.Track))
    g.add((t, DCTERMS.title, Literal(title)))
    g.add((t, EX.performedBy, EX[artist]))
    g.add((t, EX.onAlbum, EX[album]))
    if prod:
        g.add((t, EX.producedBy, EX[prod]))
    if feat:
        g.add((t, EX.featuring, EX[feat]))

if __name__ == "__main__":
    print("трійок у графі:", len(g))
    print("типів сутностей:", len(set(g.objects(None, RDF.type)) - {RDFS.Class}))
    g.serialize("emo_rap.ttl", format="turtle")
    g.serialize("emo_rap.rdf", format="xml")
    g.serialize("emo_rap.jsonld", format="json-ld")
    print("збережено: emo_rap.ttl, emo_rap.rdf, emo_rap.jsonld")
