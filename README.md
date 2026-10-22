# Лабораторна робота №1 — RDF та SPARQL (emo rap)

Предметна область: емо-реп (Lil Peep, XXXTentacion, Juice WRLD, Trippie Redd, GothBoiClique).
Дані зібрані вручну, факти звірені з Wikipedia / DBpedia.

## Запуск

```
pip install -r requirements.txt
python build_graph.py     # будує граф -> emo_rap.ttl, emo_rap.rdf, emo_rap.jsonld
python graph_ops.py       # читання, ручні зміни (emo_rap_edited.ttl), вивід трійок
python visualize.py       # graph.png
python queries.py         # SPARQL-запити
python wikidata_link.py   # owl:sameAs + дані з Wikidata (потрібен інтернет)
python error_example.py   # помилкові та виправлені приклади
```

## Файли
- `emo_rap.ttl` — згенерований граф
- `emo_rap_edited.ttl` — той самий граф, відредагований вручну (додано треки Wishing Well і Righteous)
- `emo_rap_linked.ttl` — граф після зв'язування з Wikidata
- `output/` — вивід скриптів у консоль (для звіту)
- `graph.png` — візуалізація графу

## Використання AI
Claude використовувався для пошуку та підбору даних
