import ray
from .utils import Config

config = Config("conf/ray.example.json")

address = ":".join([config.get("RAY_IP"), config.get("RAY_PORT")])
ray.init(redis_address=address)
