import redis
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

redis_client = redis.from_url(os.getenv("REDIS_URL"))
