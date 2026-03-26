from functools import lru_cache
from importlib import resources

import yaml


@lru_cache(maxsize=1)
def load_data_config():
    with resources.files(__name__).joinpath("data_config.yaml").open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)
