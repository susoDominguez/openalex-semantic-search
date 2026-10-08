import gzip, json, sys, requests

FILTER="primary_topic.id:T11244|T10190,has_abstract:true,type:article,publication_year:>2015"
params = {
    "filter": FILTER,
    "per-page": 200,
    "cursor": "*",
    "select": "id,title,display_name,abstract_inverted_index,authorships,primary_topic,open_access,primary_location,publication_year,publication_date,doi,cited_by_count,type",
}
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20_000

n = 0
with gzip.open(sys.argv[1], "wt", encoding="utf-8") as out:
    while params["cursor"] and n < limit:
        r = requests.get("https://api.openalex.org/works", params=params, timeout=60)
        r.raise_for_status()
        body = r.json()
        for work in body["results"]:
            out.write(json.dumps(work) + "\n")
            n += 1
        params["cursor"] = body["meta"].get("next_cursor")
        print(n, end="\r")
print(f"\n{n} works")

