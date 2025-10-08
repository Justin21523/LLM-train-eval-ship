import os


def print_cache_paths() -> None:
    print(f"[CACHE] MODEL_STORE_ROOT={os.getenv('MODEL_STORE_ROOT')}")
    print(f"[CACHE] HF_HOME={os.getenv('HF_HOME')}")
    print(f"[CACHE] TRANSFORMERS_CACHE={os.getenv('TRANSFORMERS_CACHE')}")
    print(f"[CACHE] HF_HUB_CACHE={os.getenv('HF_HUB_CACHE')}")
