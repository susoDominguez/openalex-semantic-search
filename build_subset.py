import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
import gzip, json, sys
from pathlib import Path
from openalex_semantic_search.builder import build_generation
from openalex_semantic_search.config import Stage
from openalex_semantic_search.embeddings import SentenceTransformerEmbedder
from openalex_semantic_search.records import parse_work

src, out = Path(sys.argv[1]), Path(sys.argv[2])
with gzip.open(src, "rt", encoding="utf-8") as f:
    papers = [p for line in f if (p := parse_work(json.loads(line)))]
n = len(papers)
lists = max(16, min(131_072, int(4 * n ** 0.5)))
stage = Stage("climate-health", n, lists, max(8, lists // 8))
m = build_generation(papers, stage=stage, output=out, embedder=SentenceTransformerEmbedder())
print(f"Built {m['records']:,} records into {out}")