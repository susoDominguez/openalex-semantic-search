#!/usr/bin/env bash
cd /Users/w1214757/Dev/openalex-semantic-search
source .venv/bin/activate
export OMP_NUM_THREADS=1
ulimit -n 2048
export HF_HUB_OFFLINE=1 #model is cached now; skip the HuggingFace netweork checks
export OPENALEX_SEARCH_API_KEYS="$(cat ~/.climate-search-key)"
exec openalex_semantic_search serve --generation indexes/climate-health --host 127.0.0.1 --port 8100