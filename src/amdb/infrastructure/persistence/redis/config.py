from dataclasses import dataclass

import toml


@dataclass(frozen=True, slots=True)
class RedisConfig:
    url: str


def load_redis_config_from_toml(path: str) -> RedisConfig:
    toml_as_dict = toml.load(path)
    redis_section_as_dict = toml_as_dict["redis"]
    return RedisConfig(url=redis_section_as_dict["url"])
